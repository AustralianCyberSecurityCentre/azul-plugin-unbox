"""Box module for Microsoft Compiled HTML Help files."""

import os
import subprocess  # noqa: S404 # nosec B404

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild

# ensure chmlib is installed in this OS
try:
    subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
        ["extract_chmLib"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
except OSError as err:
    msg = [
        "error = %s" % err,
        "module 'chm' requires the program 'extract_chmLib'.  \
            Please run apt-get install libchm-bin",
    ]
    raise ImportError("\n".join(msg)) from err


class CHM(box_base.Box):
    """Box wrapper Microsoft CHM files."""

    # builtin metadata records that get written out during extraction
    # these are usually not of interest and are excluded by default
    ignore_list = [
        "/#IDXHDR",
        "/#ITBITS",
        "/#STRINGS",
        "/#SYSTEM",
        "/#TOPICS",
        "/#URLSTR",
        "/#URLTBL",
        "/#WINDOWS",
        "/$FIftiMain",
        "/$OBJINST",
        "/$WWAssociativeLinks/Property",
        "/$WWKeywordLinks/Property",
        "/$WWKeywordLinks/Map",
        "/$WWKeywordLinks/Data",
        "/$WWKeywordLinks/BTree",
    ]

    def __init__(self, src_filepath: str, target_dir: str, passwords=None, ignore_builtins=True):
        """Create a new CHM unpacker for the supplied filepath.

        Passwords are not supported in CHM files.
        """
        super().__init__(src_filepath, target_dir, passwords)
        self.ignore_builtins = ignore_builtins

    def _extract(self):
        """Extract all of the contents of the CHM file to the target directory."""
        # try to extract to disk
        p = subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
            ["extract_chmLib", self.src_filepath, self.dest_filedir], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()
        if p.returncode:
            raise box_base.NotSupported("extract_chmLib returned %i: %s" % (p.returncode, stderr))

    def _get_all_children(self) -> list[BoxChild]:
        """Get all BoxChild objects associated with the files extracted from the CHM file."""
        children = list()
        for root, _, files in os.walk(self.dest_filedir):
            for filename in files:
                filepath = os.path.join(root, filename)
                rel_file_path = filepath[len(self.dest_filedir) :]
                if self.ignore_builtins and rel_file_path in CHM.ignore_list:
                    continue
                # drop leading slash
                rel_file_path = rel_file_path
                children.append(BoxChild(rel_file_path, os.path.join(root, filename)))

        return children
