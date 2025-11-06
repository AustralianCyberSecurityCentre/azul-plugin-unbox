"""Extract files from ZIP archives.

It supports password detection / guessing (via Unbox template).
"""

import datetime

from azul_runner import Feature, FeatureType

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox


class Zip(BaseUnbox):
    """Extract files from ZIP archives."""

    INPUT_DATA_TYPE = ["archive/zip"]  # Do we want to include JAR as well?
    FEATURES = [
        Feature(name="box_compression", desc="Compression method used on this file entry", type=FeatureType.String),
    ]

    box_display_name = "zip"
    box_class = "Zip"
    box_action = "extracted"

    key_metatypes = [
        ("modified", "box_insertdate", datetime.datetime.fromisoformat),
        ("method", "box_compression", None),
    ]
