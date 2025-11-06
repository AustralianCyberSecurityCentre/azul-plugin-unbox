import importlib
import os
import pathlib
import shutil
import tempfile
import unittest

from azul_runner.test_utils import FileManager

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild

# test file names


class BaseFileTest(unittest.TestCase):
    """Base test with generic setup for archives and extracting content from box children."""

    # Temporary src and destination directories for storing created test content.
    src_dir: str
    dest_dir: str

    # Short hand variables to access expected BoxChild names.
    all_files: list[str]
    all_files_no_dir_info: list[str]
    all_files_and_folders: list[str]

    # Name of the files and directories to be archived.
    tfile1 = "test.txt"
    tfile2 = "Ṹnɨɔŏƌɇ.txt"
    tdir1 = "adir"
    tdir2 = "bdir"

    # Contents of the two files to be archived.
    f1_contents = b"Nothing to see here... move along"
    f2_contents = b"why, hello..."

    @classmethod
    def setUpClass(cls):
        """Create the FileManager."""
        cls.file_manager = FileManager()
        super().setUpClass()

    def setUp(self):
        """Create files to archive and extract. These files are removed in the teardown."""
        self.src_dir = tempfile.mkdtemp(prefix="unbox_src")
        self.dest_dir = tempfile.mkdtemp(prefix="unbox_dest")

        d1 = BaseFileTest.tdir1
        d2 = os.path.join(d1, BaseFileTest.tdir2)

        f1 = BaseFileTest.tfile1
        f2 = os.path.join(d1, BaseFileTest.tfile2)

        self.all_files_and_folders = [f"{d1}/", f"{d2}/", f1, f2]
        self.all_files = [f1, f2]
        self.all_files_no_dir_info = [BaseFileTest.tfile1, BaseFileTest.tfile2]

    def tearDown(self):
        """Remove the test files created during setup."""
        shutil.rmtree(self.src_dir, ignore_errors=True)
        shutil.rmtree(self.dest_dir, ignore_errors=True)

    def check_metadata_list_correct(self, box: box_base.Box, parent_meta: list[str], child_meta: list[str]):
        """checking metadata"""
        # dummy src and dest
        parent_meta = box.list_meta()
        child_meta = box.list_child_meta()
        self.assertCountEqual(parent_meta, parent_meta)
        self.assertCountEqual(child_meta, child_meta)

    @staticmethod
    def get_child_names(children: list[BoxChild]):
        return [child.name for child in children]

    @staticmethod
    def get_child(children: list[BoxChild], child_name: str):
        for child in children:
            if child.name == child_name:
                return child
        return None

    @staticmethod
    def read_file(file_path: str | BoxChild) -> bytes:
        """Read a file's contents as bytes given a BoxChild or file_path.

        Args:
            file_path (str | BoxChild): a BoxChild or path to the file to be read into memory.

        Returns:
            bytes: the bytes of the files.
        """
        content = ""
        if isinstance(file_path, BoxChild):
            file_path = file_path.file_path
        with open(file_path, "rb") as f:
            content = f.read()
        return content

    @staticmethod
    def read_file_from_children(children: list[BoxChild], file_name) -> bytes:
        """Find and read the contents of a file with the provided file_name, from the dictionary of children provided.

        Args:
            children (list[BoxChild]): Dictionary of BoxChild objects to be searched for the file.
            file_name (_type_): Name of the file to locate and read contents from.

        Returns:
            bytes: contents of the requested file or None if it couldn't be found.
        """
        for child in children:
            if child.name == file_name:
                return BaseFileTest.read_file(child.file_path)
        return None

    def get_f1(self, children: list[BoxChild]) -> bytes:
        """Shorthand method to get the contents of the test file f1 when it has been extracted.

        Args:
            children (list[BoxChild]): children to locate the f1 file in.

        Returns:
            bytes: contents of the extracted f1 file.
        """
        return self.read_file_from_children(children, self.tfile1)

    def get_f2(self, children: list[BoxChild]) -> bytes:
        """Shorthand method to get the contents of the test file f2 when it has been extracted.

        Args:
            children (list[BoxChild]): children to locate the f2 file in.

        Returns:
            bytes: contents of the extracted f2 file.
        """
        return self.read_file_from_children(children, os.path.join(self.tdir1, self.tfile2))

    def _get_location(self) -> str:
        """Return path to child class that implements this class."""
        # import child module
        module = type(self).__module__
        i = importlib.import_module(module)
        # get location to child module
        return i.__file__

    def get_data_path(self, sub1: str, sub2: str = None) -> str:
        """Return expected path to test data."""
        # get folder where test is
        folder = os.path.split(self._get_location())[0]
        path = os.path.join(sub1, sub2) if sub2 else sub1
        path = os.path.join(folder, "data", path)
        return path

    def copy_test_file_to_src_dir(self, file_name: str, local_path="data/base_archives") -> str:
        """Copy a file from the test data directory to the src directory and return the path to the file.

        Expected usage:
        file_src = copy_test_file_to_src_dir("name-of-it.pdf")
        returns path to file removing cart extension.
        """
        base_folder = os.path.split(self._get_location())[0]
        # Remove cart if present and add it again.
        path = os.path.join(base_folder, local_path, file_name)
        src_path = os.path.join(self.src_dir, file_name)
        shutil.copyfile(path, src_path)
        return src_path
