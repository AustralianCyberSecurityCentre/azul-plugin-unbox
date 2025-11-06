"""Use 7Zip to extract files from many archive formats.

Also supports password detection / guessing (via Unbox template)
"""

import datetime

from azul_runner import Feature, FeatureType

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

# 7-Zip can handle a lot other other formats to varying degrees
# this list can be expanded as needed but each format will need verification
TYPE_MAP = {
    "archive/zip": "zip",  # can handle some compression modes that unbox_zip can't
    "archive/7-zip": "sevenzip",
    "archive/iso": "iso",
    "document/installer/windows": "msi",
    "installer/windows": "msi",
}


class SevenZip(BaseUnbox):
    """Use 7Zip to extract files from many archive formats."""

    INPUT_DATA_TYPE = list(TYPE_MAP.keys())
    FEATURES = [
        Feature(name="box_compression", desc="Compression method used on this file entry", type=FeatureType.String),
    ]

    box_display_name = "sevenzip"
    box_class = "Szip"
    box_action = "extracted"
    secondary_box_class = "zip"

    key_metatypes = [
        ("modified", "box_insertdate", datetime.datetime.fromisoformat),
        ("method", "box_compression", None),
    ]

    def get_descriptive_box_display_name(self, file_type: str) -> str:
        """Report more useful box_type based on the file_type that 7zip processed."""
        return TYPE_MAP.get(file_type, self.box_display_name)
