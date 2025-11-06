"""Extract files from RAR archives.

It supports password detection / guessing (via Unbox template)
"""

import datetime

import rarfile
from azul_runner import BinaryPlugin, Feature, FeatureType, State

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

from ..unbox import box_base


class Rar(BaseUnbox):
    """Extract files from RAR archives."""

    INPUT_DATA_TYPE = ["archive/rar"]
    FEATURES = [
        Feature(name="rar_compression", desc="Compression used on the contained file", type=FeatureType.Integer),
    ]

    box_display_name = "rar"
    box_class = "Rar"
    box_action = "unrar"

    key_metatypes = [
        ("createdate", "box_insertdate", datetime.datetime.fromisoformat),
        ("compresstype", "rar_compression", None),
    ]

    def exception_handler(self, ex: Exception, plugin_ref: BinaryPlugin) -> dict:
        """Handle exceptions."""
        if (
            isinstance(ex, box_base.NotSupported)
            or isinstance(ex, rarfile.BadRarFile)
            or isinstance(ex, rarfile.NotRarFile)
        ):
            return State(State.Label.ERROR_EXCEPTION, message=str(ex))
        if isinstance(ex, box_base.PasswordError):
            return State(State.Label.ERROR_EXCEPTION, message=str(ex))
        raise
