"""Box module to support formats handled by 7Zip."""

import os
import subprocess  # noqa: S404 # nosec B404

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild
from azul_plugin_unbox.unbox.libs import szip

# ensure 7zip is installed in this OS
try:
    subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
        ["7zzs"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
except OSError as err:
    msg = [
        "error = %s" % err,
        "7z requires the program '7zip'.  \
            Please run apt-get install p7zip-full",
    ]
    raise ImportError("\n".join(msg)) from err


class Szip(box_base.Box):
    """An unbox wrapper for 7Zip tool."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new unpacker that uses 7zip to unpack files."""
        super().__init__(src_filepath, target_dir, passwords)
        self.__cached_sz: szip.Unzip = None
        self.__prev_password: str = ""

    def __get_sz(self):
        """Get the 7zip object, if the password has changed create a new 7zip object."""
        if self.__prev_password != self.password or not self.__cached_sz:
            self.__prev_password = self.password
            self.__cached_sz = szip.Unzip(self.src_filepath, password=self.password)
        return self.__cached_sz

    def _extract(self):
        """Extract all of the files in the seven zip archive to the destination directory."""
        try:
            self.__get_sz().extractall(self.dest_filedir)
        except szip.ExtractNotOK as e:
            raise box_base.PasswordError("Extract Not OK") from e
        except szip.PasswordProtectedFile as e:
            raise box_base.PasswordError("Password Error") from e
        except szip.NotSupportedArchive as e:
            raise box_base.NotSupported("File Corrupt") from e
        except szip.SevenZipException as e:
            # this error is returned when file is corrupt.
            if "Unexpected end of archive" in e.cause:
                raise box_base.Corrupted("File Corrupt: %s" % e.cause) from e
            else:
                raise box_base.NotSupported("7zip decode error: %s" % e.cause) from e

    def _get_all_children(self):
        """Get all of the ChildBox objects for the objects extracted from the 7zip archive."""
        children = list()
        for child_info in self.__get_sz().fileinfo:
            path = child_info["Path"]
            new_child = BoxChild(path, os.path.join(self.dest_filedir, path))
            self.child_metadata_modified(new_child, child_info)
            self.child_metadata_method(new_child, child_info)
            children.append(new_child)
        return children

    def child_metadata_modified(self, new_child: BoxChild, info: dict):
        """Return the modified time of the specified child object."""
        res = info.get("Modified", None)
        if res is not None:
            res = res.replace(" ", "T")
        new_child._meta["modified"] = res

    def child_metadata_method(self, new_child: BoxChild, info: dict):
        """Return the compression method for the specified child object."""
        new_child._meta["method"] = info.get("Method", None)
