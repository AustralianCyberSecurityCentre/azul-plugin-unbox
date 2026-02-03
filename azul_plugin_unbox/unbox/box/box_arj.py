"""Box module for unpacking ARJ compressed archives."""

import os
import subprocess  # noqa: S404 # nosec B404

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild
from azul_plugin_unbox.unbox.libs import arj

# Uses the arj commandline tool to extract files
# we don't just reuse 7z as it doesn't have password support for arj
try:
    subprocess.Popen(["arj"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()  # noqa: S607
except OSError as err:
    msg = [
        "error = %s" % err,
        "Arj requires the program 'arj' to be installed.",
        "Please run apt-get install arj",
    ]
    raise ImportError("\n".join(msg)) from err


class Arj(box_base.Box):
    """Unbox support for ARJ compression."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new zip unpacker for the given filepath."""
        super().__init__(src_filepath, target_dir, passwords)
        self.__arj = None
        self.__prev_password = None

    def __get_arj(self):
        """Gets the Arj file, recreates the Arj file if the password has changed."""
        if not self.__arj or self.__prev_password != self.password:
            self.__arj = arj.Unzip(self.src_filepath, password=self.password)
            self.__prev_password = self.password
        return self.__arj

    def _extract(self):
        """Extract all of the arj file contents into the destination directory."""
        try:
            self.__get_arj().extract_all(self.dest_filedir)
        except arj.ExtractNotOK as e:
            raise box_base.PasswordError("Extract Not OK") from e
        except (arj.PasswordProtectedFile, arj.IncorrectPasswordException) as e:
            raise box_base.PasswordError("Password Error") from e
        except arj.NotSupportedArchive as e:
            raise box_base.NotSupported("File Corrupt") from e

    def _get_all_children(self) -> list[BoxChild]:
        """Get all ChildBox objects associated with the files extracted from the Arj archive."""
        children = list()

        for child in self.__get_arj().fileinfo:
            name = child["filename"]
            children.append(BoxChild(name, os.path.join(self.dest_filedir, name)))
        return children
