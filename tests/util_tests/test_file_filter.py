"""Testing the file_filter.py methods."""

import tempfile
import unittest

from azul_runner.test_utils import FileManager

from azul_plugin_unbox.file_filter import is_filter_out_file
from azul_plugin_unbox.unbox.box_child import BoxChild


class TestFileFilter(unittest.TestCase):
    def test_cart_should_not_be_filtered_raw_data(self):
        file = BoxChild(name="fake_java.class", data=b"Garbage text because this isn't a real java class file.")
        self.assertFalse(is_filter_out_file(file))

    def test_cart_should_not_be_filtered_file_path(self):
        with tempfile.NamedTemporaryFile("wb+") as f:
            f.write(b"Garbage text because this isn't a real java class file.")
            file = BoxChild(name="fake_java.class", file_path=f.name)
            self.assertFalse(is_filter_out_file(file))

    def test_cart_should_be_filtered_raw_data(self):
        fm = FileManager()
        file = BoxChild(
            name="hello.java.class",
            data=fm.download_file_bytes("2263c7a1b9db691b9619cf0565eb1f06c2b37aa0ddbbca7bd359c774145c37ed"),
        )
        self.assertTrue(is_filter_out_file(file))

    def test_cart_should_be_filtered_file_path(self):
        fm = FileManager()
        with tempfile.NamedTemporaryFile("wb+") as f:
            f.write(fm.download_file_bytes("2263c7a1b9db691b9619cf0565eb1f06c2b37aa0ddbbca7bd359c774145c37ed"))
            file = BoxChild(name="hello.java.class", file_path=f.name)
            self.assertFalse(is_filter_out_file(file))

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile("wb+") as f:
            f.write(b"")
            file = BoxChild(name="empty_file.class", file_path=f.name)
            self.assertFalse(is_filter_out_file(file))

    def test_no_filename(self):
        file = BoxChild(name=None, file_path="/notvalidfilepath")
        self.assertFalse(is_filter_out_file(file))

        file = BoxChild(name="", file_path="/notvalidfilepath")
        self.assertFalse(is_filter_out_file(file))

    def test_filter_on_filename(self):
        file = BoxChild(name="fake_java.clas", file_path="/notvalidfilepath")
        self.assertFalse(is_filter_out_file(file))

        file = BoxChild(name="random_filename.txt", file_path="/notvalidfilepath")
        self.assertFalse(is_filter_out_file(file))

        file = BoxChild(name="nearly_hitting_regexclass", file_path="/notvalidfilepath")
        self.assertFalse(is_filter_out_file(file))
