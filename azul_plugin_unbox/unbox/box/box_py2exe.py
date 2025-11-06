"""Box module for unpacking Py2Exe python executables."""

from datetime import datetime

from azul_plugin_unbox.py2exe_unpacker import Py2ExeUnpacker, Py2ExeUnpackError
from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild


class Py2ExeKeyError(Exception):
    """Unable to find key in Py2Exe archive."""

    def __init__(self, filename, msg):
        """Create a new exception for the given py2exe file."""
        super().__init__(msg, filename)
        self.value = "Error for %s: %s" % (filename, msg)

    def __str__(self):
        """Human-readable stirng of the exception."""
        return str(self.value)


class Py2Exe(box_base.Box):
    """Unbox wrapper for Py2Exe unpacking."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new Py2Exe unpacker for the fiven filepath.

        Passwords are not supported for the py2exe format.
        """
        super().__init__(src_filepath, target_dir, passwords)
        self.__file_details = dict()

    def _extract(self):
        """Extract all the py2exe contents and get all the child script information out."""
        try:
            # unpack everything and store it until extract needs it
            with open(self.src_filepath, "rb") as f:
                self._py2exe = Py2ExeUnpacker(f.read())
                self._contents = self._py2exe.get_results()

        except Py2ExeUnpackError:
            raise box_base.NotSupported("Extraction error")

        # check that it worked
        if self._contents is None:
            raise box_base.NotSupported("Py2Exe unpacking failed")

        # scripts contains a list of tuples of scripts and their contents
        if "scripts" in self._contents:
            for script_name, script_contents in self._contents["scripts"].items():
                # need to exclude default py2exe scripts by name
                if not (script_name.endswith("\\py2exe\\boot_common.pyc") or script_name.startswith("<")):
                    self.__file_details[script_name] = script_contents
        else:
            raise box_base.NotSupported("No scripts were extracted")

        # get zip archive, if it exists
        for key, value in self._contents.items():
            if key.lower().endswith(".zip"):
                self.__file_details[key] = value

    def _get_all_children(self) -> list[BoxChild]:
        """Get all the child python scripts from the py2Exe file."""
        children = list()
        for child_name, content in self.__file_details.items():
            new_child = BoxChild(child_name, data=content)
            children.append(new_child)
        return children

    def metadata_python_version(self):
        """Return the Python version used in the installer."""
        return self._contents.get("python_version")

    def metadata_python_compile_time(self):
        """Return the compile/build time of the py2exe package, if it exists."""
        if "build_time" in self._contents:
            return datetime.utcfromtimestamp(self._contents["build_time"]).isoformat()
        return None

    def metadata_python_libraries(self):
        """Return the import lists, if they are available."""
        if "imports_short" in self._contents:
            return self._contents["imports_short"]["standard"] + self._contents["imports_short"]["external"]
        return []
