"""Extract files from Microsoft Cabinet (CAB) compressed files.

Any decompressed content is raised as children.
Self-extracting executable CAB files are also supported.
"""

import datetime

from azul_runner import BinaryPlugin, State

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox

from ..unbox import box_base


class Cab(BaseUnbox):
    """Extract files from Microsoft Cabinet (CAB) compressed files."""

    INPUT_DATA_TYPE = [
        "archive/cabinet",
        "executable/pe32",
        "executable/windows/pe",
        "executable/windows/pe32",
        "executable/windows/pe64",
    ]

    box_display_name = "cab"
    box_class = "Cab"
    box_action = "extracted"

    key_metatypes = [
        ("modified", "box_insertdate", datetime.datetime.fromisoformat),
    ]

    def exception_handler(self, ex: Exception, plugin_ref: BinaryPlugin) -> dict:
        """Non-CAB files are not an error condition."""
        if isinstance(ex, box_base.NotSupported):
            return State(State.Label.OPT_OUT, "not_cab", "not a cab file")
        raise
