"""Holds the information for child objects of an unboxed file."""

from typing import Any


class InvalidChildError(Exception):
    """If a child object with no file path and no data is created this error is thrown."""

    pass


class BoxChild:
    """Child object that has been extracted from a box."""

    def __init__(self, name: str, file_path: str = None, data: bytes = None):
        """Init.

        Args:
            name (str): Name of the extracted object.
            file_path (str): absolute file path to the extracted file.
            data (bytes): Raw data
        """
        if file_path is None and data is None:
            print("WARNING: A BoxChild has been created with an no data and no file_path.")
        self.name = name
        self.__file_path = file_path
        self._meta: dict = dict()
        self.__raw_data: bytes | None = data

    @property
    def file_path(self) -> str | None:
        """The file path to the child object if it's available (otherwise it will be raw_data)."""
        return self.__file_path

    @property
    def raw_data(self) -> bytes | None:
        """Raw data of the child object file if it's available (otherwise it will be file_path)."""
        return self.__raw_data

    def get_meta(self) -> dict[str, Any]:
        """Return all of the metadata for this child object in a dictionary.

        Keys are the name of the metadata and value is the metadatas value
        """
        return self._meta

    def list_meta(self) -> list[str]:
        """List all of the available metadata types for the box."""
        return list(self._meta.keys())
