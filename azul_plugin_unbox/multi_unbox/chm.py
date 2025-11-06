"""Extracts contents of MS Compiled HTML Help (CHM) files."""

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox


class CHM(BaseUnbox):
    """Extracts contents of MS Compiled HTML Help (CHM) files."""

    INPUT_DATA_TYPE = ["archive/chm"]

    box_display_name = "chm"
    box_class = "Chm"
    box_action = "extracted"
