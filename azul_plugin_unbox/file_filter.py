"""Filter out unwanted extracted files."""

import re

from azul_bedrock import identify

from .unbox.box_child import BoxChild

reg = re.compile(r"\.(class)$")

banned_file_types = ["code/class"]


def is_filter_out_file(file: BoxChild) -> bool:
    """Filter out unwanted files, returning True if the file should be filtered out."""
    # Check if file name suggests file should be filtered out.
    if file.name is None or reg.search(file.name) is None:
        return False

    # Attempt to get raw data of the boxChild object.
    file_type_al = None
    if file.file_path:
        _, _, file_type_al, _, _ = identify.from_file(file.file_path)
    elif file.raw_data:
        _, _, file_type_al, _, _ = identify.from_buffer(file.raw_data)
    else:
        # File has no content and can be handled by the main processor.
        return False

    if file_type_al in banned_file_types:
        return True

    return False
