"""Box module for Microsoft Cabinet files."""

import os
import subprocess  # noqa: S404 # nosec B404
from datetime import datetime

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild
from azul_plugin_unbox.unbox.libs import cabextract

try:
    subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
        ["cabextract"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
except OSError as err:
    raise ImportError(
        "error = %s\n"
        "module 'cabextract' requires the program 'cabextract'. "
        "Please run apt-get install cabextract" % str(err)
    )


class Cab(box_base.Box):
    """Unbox wrapper for MS Cabinet files."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new Cab unpacker for the supplied filepath.

        Passwords are not support in Cab files.
        """
        super().__init__(src_filepath, target_dir, passwords)
        self.__cab = None

    def __get_cab(self):
        """Get the Cab file and creates it if it doesn't already exist."""
        if not self.__cab:
            self.__cab = cabextract.CabExtract(self.src_filepath)
        return self.__cab

    def _extract(self):
        """Extract all of the contents of the CAB archive."""
        try:
            self.__get_cab().extract_all(self.dest_filedir)
        except box_base.NotSupported:
            raise box_base.NotSupported("Not a Cab file")

    def _get_all_children(self) -> list[BoxChild]:
        """Get all BoxChild objects associated with the files extracted from the CAB file."""
        children = list()
        for each_child in self.__get_cab().fileDetails.keys():
            path = os.path.join(self.dest_filedir, each_child)
            new_child = BoxChild(each_child, path)
            self.child_metadata_modified(new_child)
            children.append(new_child)
        return children

    def child_metadata_modified(self, new_child: BoxChild):
        """Return the last modified time as a datetime obj for the child object."""
        date = self.__get_cab().fileDetails[new_child.name]
        date = date.strip()
        new_child._meta["modified"] = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").isoformat()
