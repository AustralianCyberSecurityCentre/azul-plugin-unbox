"""Unbox template."""

import contextlib
import os
import tempfile
from typing import Any, Type

from azul_runner import (
    FV,
    BinaryPlugin,
    Feature,
    FeatureType,
    Job,
    State,
    add_settings,
    cmdline_run,
    settings,
)

from azul_plugin_unbox import file_filter
from azul_plugin_unbox.multi_unbox import (
    arj,
    cabinet,
    chm,
    pdf,
    rar,
    sevenzip,
    unix_archive,
    upx,
)
from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

from .unbox.box import box as boxes
from .unbox.box_base import Box
from .unbox.box_child import BoxChild

SETTINGS_PASSWORD_KEY = "passwords"  # nosec B105


class BadMultiUnboxConfigError(Exception):
    """Exception raised when multiplugins have metatypes that don't match to an OUTPUT_FEATURE anywhere."""

    pass


class AzulPluginUnbox(BinaryPlugin):
    """Multiplugin that manages the unboxing of multiple file types."""

    CONTACT = "ASD's ACSC"
    VERSION = "2025.04.23"
    SETTINGS = add_settings(
        filter_max_content_size="0",  # operate on any sized file
        run_timeout=60 * 15,  # unarchivers have lots of children to be inserted so allow more time
        default_passwords=(list[str], ["password", "infected"]),
        max_extracted_files=(int, 1000),
    )
    # Child unbox subclass should set any additional features it generates (but don't need to duplicate these)
    FEATURES = [
        Feature(name="box_password", desc="Password used to unbox this binary", type=FeatureType.String),
        Feature(name="box_count", desc="Number of items found in the box", type=FeatureType.Integer),
        Feature(name="box_type", desc="The binary is of this box type", type=FeatureType.String),
        Feature(name="box_filepath", desc="This entity contains this filepath", type=FeatureType.Filepath),
        Feature(name="box_insertdate", desc="Date the file was inserted into the archive", type=FeatureType.Datetime),
        Feature(name="filename", desc="The name of the file in its parent archive", type=FeatureType.Filepath),
        # Set generic feature to allow correlation against other sources of passwords too
        Feature(name="password", desc="Password used to unbox this binary", type=FeatureType.String),
    ]

    # Active Unbox # FUTURE make this cmdline option.
    ACTIVE_UNBOX: list[BaseUnbox] = [
        arj.Arj(),
        cabinet.Cab(),
        chm.CHM(),
        pdf.Pdf(),
        rar.Rar(),
        sevenzip.SevenZip(),
        unix_archive.UnixArchive(),
        upx.UPX(),
    ]

    def __init__(self, config: settings.Settings | dict = None):
        super().__init__(config)

        self.current_file_format = None
        self.current_passwords = None
        self.current_source_filepath = None

        def get(unboxClass: BaseUnbox):
            return lambda x: self.execute_unboxer(unboxClass, x)

        for m in self.ACTIVE_UNBOX:
            self.register_multiplugin(m.box_display_name, None, get(m))

    def _alter_config(self, config: settings.Settings) -> settings.Settings:
        # hack to do these feature changes, but necessary
        AzulPluginUnbox.FEATURES = set(AzulPluginUnbox.FEATURES)
        input_data_types = set()
        for m in self.ACTIVE_UNBOX:
            AzulPluginUnbox.FEATURES.update(m.FEATURES)
            input_data_types.update(m.INPUT_DATA_TYPE)

        config.filter_data_types = {"content": list(input_data_types)}

        feature_names = [fv.name for fv in AzulPluginUnbox.FEATURES]
        for m in self.ACTIVE_UNBOX:
            metatypes = m.metatypes + m.key_metatypes
            for t in metatypes:
                if t[1] not in feature_names:
                    raise BadMultiUnboxConfigError()

        return config

    def execute(self, job: Job):
        """Required to ensure all multiplugins run."""
        # Future download file here.
        data_streams = job.get_all_data()

        if not data_streams:
            return State(State.Label.OPT_OUT, "no_streamsrequires data_stream(s)")

        provided_passwords = []
        data = None
        for s in data_streams:
            if s.file_info.label == "content":
                data = s
            elif s.file_info.label == "password_dictionary":
                provided_passwords = s.read().decode("utf-8").splitlines()

        if data is None:
            return State(State.Label.OPT_OUT, "no_stream_contentrequires data stream with label=content")

        settings_provided_passwords = job.event.source.settings.get(SETTINGS_PASSWORD_KEY, "")
        # Find all non-empty passwords
        settings_provided_passwords = [x for x in settings_provided_passwords.split("\n") if x]

        # make a copy of passwords to avoid a box modifying them for future runs
        passwords = list(self.cfg.default_passwords or ["password", "infected"])
        passwords.extend(provided_passwords)
        passwords.extend(settings_provided_passwords)

        self.current_file_format = data.file_info.file_format
        self.current_passwords = passwords
        self.current_source_filepath = data.get_filepath()

        if not self.current_source_filepath:
            return State(
                State.Label.ERROR_EXCEPTION,
                "failed to find a filepath or download the data file",
            )

        return State(State.Label.COMPLETED)

    def execute_unboxer(self, unboxer: BaseUnbox, job: Job):
        """Extract any contained child entities with the current unboxer."""
        # Verify that declared metatypes and key_metatypes exist in FEATURES
        # Multi plugins will OPTOUT if they aren't configured to take particular file_type.
        if job.event.entity.file_format not in unboxer.INPUT_DATA_TYPE:
            return State(
                State.Label.OPT_OUT,
                "wrong_file_type",
                f"wrong file type '{job.event.entity.file_format}' provided",
            )

        BoxClass: Type[Box] = boxes[unboxer.box_class]
        try:
            box: Box = BoxClass(
                self.current_source_filepath,
                tempfile.gettempdir(),
                passwords=self.current_passwords,
            )
        except Exception as ex:
            return unboxer.exception_handler(ex, self)

        child_filepaths = []
        file_count = 0
        max_files = self.cfg.max_extracted_files or 1000
        # Add each child for this box type
        try:
            try:
                box_children = sorted(box.get_children(), key=lambda b: b.name)
            except Exception:
                # Attempt to use a secondary unboxer if the primary failed and has a backoup.
                did_secondary_fail = True
                if unboxer.secondary_box_class:
                    with contextlib.suppress(Exception):
                        SecondaryBoxClass: Type[Box] = boxes[unboxer.secondary_box_class]
                        secondary_box = SecondaryBoxClass(box.src_filepath, box.dest_filedir, passwords=box.passwords)
                        box_children = sorted(secondary_box.get_children(), key=lambda b: b.name)
                        box = secondary_box
                        did_secondary_fail = False

                if did_secondary_fail:
                    raise

            for box_child in box_children:
                # Filter out unwanted extracted files
                if file_filter.is_filter_out_file(box_child):
                    continue
                file_count += 1

                # Warning for too many extracted files.
                if file_count > max_files:
                    self.logger.warning(
                        f"The extractor '{unboxer.box_display_name}' has extracted too many files for the file "
                        + f"'{job.id}', extracted {len(box_children)} files, dropping excess "
                        + f"{len(box_children) - max_files} files."
                    )
                    # FUTURE this is really a completed with warnings case, because it's completed but not everything
                    # went well.
                    return State(State.Label.COMPLETED)

                full_key = box_child.name
                child_features = {}
                if unboxer.children_have_useable_filenames:
                    if full_key.endswith(("/", "\\")):
                        # this is where we have an empty folder
                        # set filepath and continue
                        child_filepaths.append(full_key)
                        continue

                    # Always set box_filepath on parent even if no path structure. Otherwise we get inconsistencies
                    # with numbers vs box_count and not all files listed in box_filepath when some are in the root
                    # and others in subdirs, which is confusing.
                    child_filepaths.append(full_key)
                    child_features["filename"] = full_key

                # Add the metadata defined for this key's box type
                for metatype, feature_name, conv_func in unboxer.key_metatypes:
                    metadata = box_child.get_meta().get(metatype)
                    if metadata is None:
                        continue

                    # ensure we use the full file path, otherwise we could get duplicate labels
                    self.add_feature_values(
                        feature_name,
                        FV(value=metadata if conv_func is None else conv_func(metadata), label=full_key),
                    )

                rel_metadata = []
                for metatype, feature_name, conv_func in unboxer.rel_metatypes:
                    metadata = box_child.get_meta().get(metatype)
                    if metadata is None:
                        continue
                    rel_metadata.append((feature_name, metadata if conv_func is None else conv_func(metadata)))

                self.add_binary(
                    box_child,
                    relationship={"action": unboxer.box_action, **{k: v for k, v in rel_metadata}},
                    child_features=child_features,
                )
            if box.password is not None:
                pw = box.password
                if isinstance(pw, bytes):
                    # Some boxes require the password to be bytes, while others are unicode
                    # Try to decode it as utf8; on failure display it as a python raw string ("b'abc\x00\x12\x34'")
                    try:
                        pw = pw.decode("utf-8")
                    except UnicodeDecodeError:
                        pw = str(pw)
                self.add_feature_values("box_password", pw)
                self.add_feature_values("password", pw)
            self.add_feature_values("box_type", unboxer.get_descriptive_box_display_name(self.current_file_format))
            # count may not match num children if box lists dirs separately
            self.add_feature_values("box_count", len(box_children))

            # Add the metadata defined for this box type
            for metatype, feature_name, conv_func in unboxer.metatypes:
                metadata = box.get_meta().get(metatype)
                if metadata is None:
                    continue
                # Not added as FV() as value might be a list.
                self.add_feature_values(feature_name, metadata if conv_func is None else conv_func(metadata))
            if child_filepaths:
                self.add_feature_values("box_filepath", child_filepaths)

        except Exception as exp:
            return unboxer.exception_handler(exp, self)
        finally:
            # trigger a cleanup at end of processing to find samples that cause this to fail
            box.cleanup()

    def add_binary(self, child: BoxChild, relationship: dict, child_features: dict[str, Any] = None):
        """Add a binary as per BinaryTemplate plugin."""
        if child.file_path:
            # Drop empty file
            if os.path.getsize(child.file_path) == 0:
                self.logger.warning("An empty file is being created by one of the box handlers.")
                return
            with open(child.file_path, "rb") as f:
                c = self.add_child_with_data_file(relationship, f)
        elif child.raw_data:
            c = self.add_child_with_data(relationship, child.raw_data)
        else:
            # Drop empty file
            return

        c.add_many_feature_values(child_features)


def main():
    """Commandline run."""
    cmdline_run(plugin=AzulPluginUnbox)


if __name__ == "__main__":
    main()
