"""Unpack pdf streams.

It also supports password guessing (via Unbox template) for encrypted PDFs.
"""

from azul_runner import Feature, FeatureType

from azul_plugin_unbox.multi_unbox.base_unbox import BaseUnbox


class Pdf(BaseUnbox):
    """Unpack pdf streams."""

    INPUT_DATA_TYPE = ["document/pdf", "document/pdf/portfolio", "document/pdf/passwordprotected"]
    FEATURES = {
        Feature(
            "pdf_object_dictionary", desc="Object dictionary/id for the extracted PDF stream", type=FeatureType.String
        ),
    }

    children_have_useable_filenames = False
    box_display_name = "pdf"
    box_class = "PDF"
    box_action = "extracted"

    key_metatypes = [
        ("object_dictionary", "pdf_object_dictionary", lambda x: x.decode("utf-8")),
    ]
    rel_metatypes = [
        ("object_id", "object_id", str),
        ("stream_filter", "filter", lambda x: x.decode("utf-8")),
    ]
