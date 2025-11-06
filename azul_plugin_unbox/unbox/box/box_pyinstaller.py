"""Box module for unpacking PyInstaller built python executables."""

from datetime import datetime

from azul_plugin_unbox.pyinstaller_unpacker import pyi
from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild


class PyIKeyError(Exception):
    """Error retrieving key from PyInstaller executable."""

    def __init__(self, filename, msg):
        """Create a new exception for the given PyI filename."""
        super().__init__(msg, filename)
        self.value = "Error for %s: %s" % (filename, msg)

    def __str__(self):
        """Human-readable string of exception."""
        return str(self.value)


class PyInstaller(box_base.Box):
    """Unpacker for PyInstaller executables."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new pyinstaller unpacker for the given filepath.

        Passwords are not supported for the pyinstaller format.
        """
        super().__init__(src_filepath, target_dir, passwords)
        self.__file_details = dict()
        self._contents = None

    def _extract(self):
        try:
            # Read everything into memory # FUTURE replace this when pyinstaller gets updated.
            with open(self.src_filepath, "rb") as raw_contents:
                self._contents = pyi.process_pyinstaller(raw_contents.read())
        except pyi.NoPackage:
            raise box_base.NotSupported("No package found")
        except pyi.InvalidFile:
            raise box_base.NotSupported("Invalid file")
        except pyi.UnsupportedFile:
            raise box_base.NotSupported("Unsupported file")

        # check that it worked
        if self._contents is None:
            raise box_base.NotSupported("PyInstaller unpacking failed")

        # scripts contains a list of tuples of scripts and their contents
        if "scripts" in self._contents:
            for script_info in self._contents["scripts"]:
                self.__file_details[script_info[0]] = script_info[1]
        else:
            raise box_base.NotSupported("No scripts were extracted")

        ise = set()
        iss = set()
        ile = set()
        ils = set()

        # get pyz archives
        for key, value in self._contents.items():
            if key.lower().endswith(".pyz"):
                self.__file_details[key] = value[0]
                # set python libraries
                iss.update(value[1]["standard"])
                ise.update(value[1]["external"])
                ils.update(value[2]["standard"])
                ile.update(value[2]["external"])
        self._contents["imports_short"] = {"standard": sorted(list(iss)), "external": sorted(list(ise))}
        self._contents["imports_long"] = {"standard": sorted(list(ils)), "external": sorted(list(ile))}

    def _get_all_children(self) -> list[BoxChild]:
        children = list()
        for detail_name, content in self.__file_details.items():
            new_child = BoxChild(detail_name, data=content)
            children.append(new_child)
        return children

    def metadata_python_version(self):
        """Return the Python version used in the installer."""
        if "python_version" in self._contents and len(self._contents["python_version"]) == 2:
            return "Python %i.%i" % self._contents["python_version"]
        return None

    def metadata_python_compile_time(self):
        """Return the compile time of the main script, if it exists."""
        if "compile_time_unix" in self._contents:
            return datetime.utcfromtimestamp(self._contents["compile_time_unix"]).isoformat()
        return None

    def metadata_pyinstaller_build_platform(self):
        """Return the PyInstaller build platform, if it was identified."""
        return self._contents.get("build_platform")

    def metadata_python_libraries(self):
        """Return the libraries packaged within the .pyz archive."""
        if "imports_short" in self._contents:
            return self._contents["imports_short"]["standard"] + self._contents["imports_short"]["external"]
        return []
