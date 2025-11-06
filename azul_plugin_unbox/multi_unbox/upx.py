"""Unpack UPX (Ultimate Packer for Executables) format."""

from azul_runner import BinaryPlugin, Feature, FeatureType, State

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

from ..unbox import box_base
from ..unbox.libs import upx


class UPX(BaseUnbox):
    """Unpack UPX (Ultimate Packer for Executables) format."""

    INPUT_DATA_TYPE = [
        # Windows exe
        "executable/windows/pe",
        "executable/windows/pe32",
        "executable/windows/pe64",
        "executable/windows/dll",
        "executable/windows/dll32",
        "executable/windows/dll64",
        "executable/windows/dos",
        "executable/windows/com",
        # Potential Windows Exe
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
        Feature(name="upx_version", desc="Detected upx version used to pack executable", type=FeatureType.String),
    ]

    children_have_useable_filenames = False
    box_display_name = "upx"
    box_class = "UPX"
    box_action = "unpacked"

    metatypes = [("upx_version", "upx_version", bytes.decode)]

    def exception_handler(self, ex: Exception, plugin_ref: BinaryPlugin) -> dict:
        """Non-UPX files are not an error condition."""
        if isinstance(ex, box_base.NotSupported):
            return State(State.Label.OPT_OUT, "not_upx", "not a UPX packed file")
        # Handle case where the error occurred because the input file was too small.
        if isinstance(ex, upx.UpxRaisedAnError) and "IOException: file is too small" in ex.value:
            return State(State.Label.OPT_OUT, "not_upx", "too small to be a UPX file")
        if isinstance(ex, upx.ModifiedHackedProtectedException):
            # can't unpack it but can flag it
            plugin_ref.add_many_feature_values({"upx_version": {"upx modified"}, "box_type": {"upx"}})
        raise
