"""Unpack python code from Py2Exe packed executables."""

from datetime import datetime

from azul_runner import BinaryPlugin, Feature, FeatureType, State

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

from ..unbox import box_base


class Py2ExeArchive(BaseUnbox):
    """Unpack python code from Py2Exe packed executables."""

    INPUT_DATA_TYPE = [
        "executable/pe32",
        "executable/windows/pe",
        "executable/windows/pe32",
        "executable/windows/pe64",
        "executable/windows/dos",
        "executable/windows/com",
    ]
    FEATURES = [
        Feature(name="python_version", desc="Python version used to build archive", type=FeatureType.String),
        Feature(name="py2exe_build_time", desc="Build time of Py2Exe archive", type=FeatureType.Datetime),
        Feature(name="python_library", desc="Python library package within this archive", type=FeatureType.String),
    ]

    box_display_name = "py2exe"
    box_class = "Py2Exe"
    box_action = "unpacked"

    # python_libraries will be shared by py2exe and pyinstaller
    metatypes = [
        ("python_version", "python_version", str),
        ("python_compile_time", "py2exe_build_time", datetime.fromisoformat),
        ("python_libraries", "python_library", None),
    ]

    def exception_handler(self, ex: Exception, plugin_ref: BinaryPlugin) -> dict:
        """Non-Py2Exe files are not an error condition."""
        if isinstance(ex, box_base.NotSupported):
            return State(State.Label.OPT_OUT, "not_py2exe", "not a py2exe file")
        raise
