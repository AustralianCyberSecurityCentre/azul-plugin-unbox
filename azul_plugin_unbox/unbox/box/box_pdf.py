"""Box module for PDF files.

Supports decrypting PDFs to an unencrypted copy and extraction of
any contained object streams.

Required system packages
------------------------

- qpdf

"""

import os
import re
from subprocess import PIPE, Popen  # noqa: S404 # nosec B404
from sys import platform

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild

try:
    Popen(["qpdf"], stdout=PIPE, stderr=PIPE).communicate()  # noqa: S603, S607 # nosec B603 B607
except OSError as e:
    msg = "error = %s\nbox_pdf requires the program 'qpdf'. Run `$ apt-get install qpdf`"
    raise ImportError(msg % e) from e


class Pdf(box_base.Box):
    """PDF box class for decryption and stream extraction."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None, low_memory=True):
        """Create a new PDF unpacker for the given filepath.

        Note: Will always try the empty password for owner encrypted PDFs.

        Note: Child metadata is not 100% correct for PDF because the extracted PDF child object doesn't have the same
        metadata.
        """
        super().__init__(src_filepath, target_dir, passwords)
        # common to have pdf's encrypted with an owner hash
        # but an empty user password so always try the empty string
        if "" not in self.passwords:
            self.add_password("")
        self._is_encrypted = None
        self._child_streams = dict()
        self.__low_ram = low_memory
        self.__decrypted_file_path = None

        # ensure no window is created.
        self.creationflags = 0
        if platform == "win32":
            self.creationflags = 0x08000000  # CREATE_NO_WINDOW

    def _extract(self):
        """Decrypt the PDF if it's encrypted and get all of the child stream objects."""
        self._decrypt()
        self._extract_child_streams()

    def _get_all_children(self) -> list[BoxChild]:
        """Get all of the child streams from a PDF and if the PDF is encrypted get the pdf as well."""
        children = list()
        if self.is_encrypted:
            file_name = os.path.basename(self.__decrypted_file_path)
            children.append(BoxChild(file_name, file_path=self.__decrypted_file_path))

        for obj_id, data in self._child_streams.items():
            data_or_path = data.get("data_or_path")
            if not data_or_path:
                # Dataless child (just metadata)
                new_child = BoxChild(obj_id)
            elif self.__low_ram:
                new_child = BoxChild(obj_id, file_path=data_or_path)
            else:
                new_child = BoxChild(obj_id, data=data_or_path)

            self.child_metadata_object_id(new_child)
            self.child_metadata_object_dictionary(new_child)
            self.child_metadata_stream_filter(new_child)

            children.append(new_child)
        return children

    def child_metadata_object_id(self, new_child: BoxChild):
        """Return the PDF Object Id that the stream was extracted from."""
        new_child._meta["object_id"] = new_child.name

    def child_metadata_object_dictionary(self, new_child: BoxChild):
        """Return the PDF object dictionary for the given key."""
        new_child._meta["object_dictionary"] = self._child_streams[new_child.name].get("obj_dict", None)

    def child_metadata_stream_filter(self, new_child: BoxChild):
        """Return the stream filter/s that was used for the object."""
        obj_dict = self._child_streams[new_child.name].get("obj_dict", None)
        if obj_dict:
            new_child._meta["stream_filter"] = self._get_filter(obj_dict)

    @staticmethod
    def _get_filter(objdict):
        """Extract the stream filter name from an object dictionary string."""
        # first check for cascaded/multiple
        m = re.search(b"/Filter\\s+\\[(.+?)\\]", objdict)
        if m:
            # return comma-separated string list (in-order)
            return b", ".join([x.strip() for x in m.group(1).split(b"/") if x.strip()])
        # test single filter
        m = re.search(b"/Filter\\s+(\\S+)", objdict)
        if m:
            return m.group(1)[1:]  # strip prefixed /
        return None

    def _decrypt(self) -> bool:
        """Try to decrypt the PDF using the currently set password."""
        if not self.is_encrypted:
            self.decrypted_data = None
            return False

        # it's encrypted, so lets try to decrypt it
        if self.password is None:
            raise box_base.PasswordError("File is encrypted and no password was given")

        # OK, lets decrypt the pdf
        self.__decrypted_file_path = os.path.join(self.dest_filedir, os.path.basename(self.src_filepath))
        cmd = [
            "qpdf",
            "--password=%s" % self.password,
            "--decrypt",
            "--static-id",
            self.src_filepath,
            self.__decrypted_file_path,
        ]
        try:
            process = Popen(  # noqa:  S603, S607 # nosec B603 B607
                cmd, stdout=PIPE, stderr=PIPE, creationflags=self.creationflags
            )
            stdout, stderr = process.communicate()
        except OSError as err:
            raise OSError("Failed to Popen('%s') with %s" % (" ".join(cmd), err)) from err

        if b"invalid password" in stderr:
            raise box_base.PasswordError("invalid password")

        return True

    @property
    def is_encrypted(self):
        """Return if current PDF instance is encrypted."""
        if self._is_encrypted is None:
            # work out if we are encrypted
            cmd = ("qpdf", "--show-encryption", self.src_filepath)
            try:
                process = Popen(  # noqa: S603, S607 # nosec B603 B607
                    cmd, stdout=PIPE, stderr=PIPE, creationflags=self.creationflags
                )
                stdout, stderr = process.communicate()
            except OSError as err:
                raise OSError("Failed to Popen('%s') with %s" % (" ".join(cmd), err)) from err

            # make sure it's actually a PDF
            if b"not a PDF file" in stderr or b"unable to find trailer dictionary while recovering" in stderr:
                raise box_base.NotSupported("file is not a PDF")

            # ignore any other stderr warnings as can prob still process

            self._is_encrypted = False
            if b"File is not encrypted" not in stdout:
                self._is_encrypted = True

        return self._is_encrypted

    def _extract_child_streams(self):
        """Pull apart any streams from the PDF."""
        # Get all object Id's
        cmd_append = []
        if self.password is not None:
            cmd_append = [
                f"--password={self.password}",
                "--decrypt",
            ]
        cmd_append.append(self.src_filepath)

        get_obj_cmd = ["qpdf", "--show-xref"] + cmd_append

        process = Popen(  # noqa: S603, S607 # nosec B603 B607
            get_obj_cmd, stdout=PIPE, stderr=PIPE, creationflags=self.creationflags
        )
        stdout, stderr = process.communicate()

        # Lines should be in the form "330/0: uncompressed; offset = 1312526"
        # Need the object ID which is the leading 330/0 so split on : and check value.
        obj_id_reg = re.compile("^[0-9]+/?[0-9]*$")
        for line in stdout.splitlines():
            obj_id = line.split(b":")[0].decode("utf-8")
            if not obj_id_reg.fullmatch(obj_id):
                print(f"Skipping pdf object with ID {obj_id}")
                continue

            cmd = ["qpdf", f"--show-object={obj_id}"] + cmd_append

            process = Popen(  # noqa: S603, S607 # nosec B603 B607
                cmd, stdout=PIPE, stderr=PIPE, creationflags=self.creationflags
            )
            stdout, stderr = process.communicate()

            # is stream so extract data
            if stdout.startswith(b"Object is stream."):
                objdict = stdout.splitlines()[1]
                cmd.insert(2, "--filtered-stream-data")
                process = Popen(  # noqa: S603, S607 # nosec B603 B607
                    cmd, stdout=PIPE, stderr=PIPE, creationflags=self.creationflags
                )
                stdout, stderr = process.communicate()
                # Set child path to None if there is no stream data.
                if len(stdout) == 0:
                    stdout = None
                elif self.__low_ram:
                    file_path = os.path.join(self.dest_filedir, self._obj_file_id_to_name(obj_id))
                    with open(file_path, "wb") as f:
                        f.write(stdout)

                    stdout = file_path

                self._child_streams[obj_id] = {
                    "obj_dict": objdict,
                    "data_or_path": stdout,
                }

    @staticmethod
    def _obj_file_id_to_name(obj_id):
        return obj_id.replace("/", "-")
