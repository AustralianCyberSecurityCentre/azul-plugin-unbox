"""Box module to support UPX packed executables."""

import os
import subprocess  # noqa: S404 # nosec B404

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild
from azul_plugin_unbox.unbox.libs import upx

# Uses the upx commandline tool to extract files
try:
    subprocess.Popen(["upx"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()  # noqa: S607
except OSError as err:
    msg = [
        "error = %s" % err,
        "Upx requires the program 'upx' to be installed.",
        "Please run apt-get install upx-ucl",
    ]
    raise ImportError("\n".join(msg)) from err


class UPX(box_base.Box):
    """UPX executable unpacker."""

    def __get_dest_path(self) -> str:
        """Creates a path to extract the upx file to."""
        return os.path.join(self.dest_filedir, os.path.basename(self.src_filepath))

    def _extract(self):
        """Unpacks the UPX file into the dest directory."""
        try:
            upx.unpack(self.src_filepath, self.__get_dest_path())
            return [self.__get_dest_path()]
        except (upx.NotPackedException, upx.CantUnpackException) as e:
            raise box_base.NotSupported("File does not appear to be UPX packed") from e

    def _get_all_children(self) -> list[BoxChild]:
        """Get the single unpacked file as a child object."""
        unpacked_name = os.path.basename(self.src_filepath)
        return [BoxChild(unpacked_name, self.__get_dest_path())]

    def metadata_upx_version(self):
        """Extract the UPX Version Id used to pack the upx file.

        Returns None if unable to determine or not packed.
        """
        return upx.version(self.src_filepath)
