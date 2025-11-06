"""Extract files from common Unix archive types.

Currently, this includes: tar, tar.gz, tar.bz2, gz, bz2.
"""

from azul_runner import Feature, FeatureType

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox


class UnixArchive(BaseUnbox):
    """Extract files from common Unix archives (tar, gzip, bzip)."""

    INPUT_DATA_TYPE = ["archive/tar", "archive/gzip", "archive/bzip2"]
    FEATURES = [
        Feature(name="archive_encoding", desc="Character Encoding used by this archive", type=FeatureType.String),
        Feature(
            name="extra_content",
            desc="Archive has extra content that was ignored during extraction",
            type=FeatureType.String,
        ),
    ]

    box_display_name = "archive"
    box_class = "Archive"
    box_action = "extracted"

    metatypes = [("encoding", "archive_encoding", None), ("has_extra_content", "extra_content", None)]
