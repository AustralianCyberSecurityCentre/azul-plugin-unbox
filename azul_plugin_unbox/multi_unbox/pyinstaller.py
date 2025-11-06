"""Unbox python artifacts from PyInstaller packed executables."""

from datetime import datetime

from azul_runner import BinaryPlugin, Feature, FeatureType, State

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

from ..unbox import box_base


class PyInstallerArchive(BaseUnbox):
    """Unbox python artifacts from PyInstaller packed executables."""

    INPUT_DATA_TYPE = [
        # Windows exe
        "executable/windows/pe",
        "executable/windows/pe32",
        "executable/windows/pe64",
        "executable/windows/dos",
        "executable/windows/com",
        # # Potential Windows Exe
        "executable/dll32",
        "executable/pe32",
        # Linux exe
        "executable/linux/elf64",
        "executable/linux/elf32",
        "executable/linux/so64",
        "executable/linux/so32",
        "executable/mach-o",
    ]
    FEATURES = [
        Feature(name="python_version", desc="Python version used to build archive", type=FeatureType.String),
        Feature(
            name="pyinstaller_build_platform",
            desc="Platform used to build PyInstaller archive",
            type=FeatureType.String,
        ),
        Feature(name="pyinstaller_build_time", desc="Build time of PyInstaller archive", type=FeatureType.Datetime),
        Feature(name="python_library", desc="Python library package within this archive", type=FeatureType.String),
    ]

    box_display_name = "pyinstaller"
    box_class = "PyInstaller"
    box_action = "unpacked"

    # python_libraries will be shared by py2exe and pyinstaller
    metatypes = [
        ("python_version", "python_version", str),
        ("pyinstaller_build_platform", "pyinstaller_build_platform", str),
        ("python_compile_time", "pyinstaller_build_time", datetime.fromisoformat),
        # python_library returns a list of strs, which is accepted by the runner as multiple feature values
        # Since this is what we want, no further processing is necessary.
        ("python_libraries", "python_library", None),
    ]

    def exception_handler(self, ex: Exception, plugin_ref: BinaryPlugin) -> dict:
        """Non-PyInstaller files are not an error condition."""
        if isinstance(ex, box_base.NotSupported):
            return State(State.Label.OPT_OUT, "not_pyinstaller", "not a PyInstaller exe")
        raise
