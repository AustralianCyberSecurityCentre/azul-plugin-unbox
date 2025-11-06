"""Extract files from ARJ archives.

Password protected archives are handled by Unbox.
"""

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox


class Arj(BaseUnbox):
    """Extract files from ARJ archives."""

    INPUT_DATA_TYPE = ["archive/arj"]

    box_display_name = "arj"
    box_class = "Arj"
    box_action = "extracted"
