# coding=utf-8
"""Test suite for unbox PyInstaller integration - note this still generates binaries because they are quite large (22MB).
It also helps with portability between python versions.
"""
import os.path
import subprocess
import sys

from azul_plugin_unbox.pyinstaller_unpacker.pyi import PYI_MAGIC
from azul_plugin_unbox.unbox.box import box_pyinstaller
from azul_plugin_unbox.unbox.box_base import NotSupported
from tests.unbox.base_test import BaseFileTest

test_script = """
import pprint
import PyInstaller
pprint([\"Hello testing world!\",\"日本語\", PyInstaller.loader.pyimod02_archive.CRYPT_BLOCK_SIZE])
"""
# check for PyInstaller
try:
    import PyInstaller
except ImportError as err:
    raise ImportError(
        "error = %s\ntest_pyinstaller requires the 'PyInstaller' package to be installed.\n"
        "Please run pip install PyInstaller==3.4" % str(err)
    )


class PyInstallerTest(BaseFileTest):
    """Test Pyinstaller box."""

    def setUp(self):
        """Read in stored test file and decode base64 data."""
        super().setUp()

        pyinstaller_script = "テスト.py"
        pyinstaller_script_path = os.path.join(self.src_dir, pyinstaller_script)
        with open(pyinstaller_script_path, "w") as f:
            f.write(test_script)

        # run pyinstaller in the temp dir
        subprocess.call(["python", "-m", "PyInstaller", "-F", pyinstaller_script_path], cwd=self.src_dir)

        # confirm that PyInstaller file was built
        self.compiled_script_name = pyinstaller_script + "c"
        self.compiled_script_path = os.path.join(os.path.join(self.src_dir, "dist"), pyinstaller_script[:-3])
        assert os.path.isfile(self.compiled_script_path)

        # read that file into data
        with open(self.compiled_script_path, "rb") as f:
            self.data_pyi = f.read()

        # create corrupted pyi file
        corrupted = bytearray(self.data_pyi)

        # alter offset
        i = corrupted.rfind(PYI_MAGIC)
        # overwrite package size in pyi cookie
        corrupted[i + 8 : i + 12] = b"\x00\x00\x00\x00"

        self.corrupted_script_path = os.path.join(self.src_dir, "corrupted.pyc")
        with open(self.corrupted_script_path, "wb") as f:
            f.write(bytes(corrupted))

    def test_pyinstaller(self):
        """Test unpacking the test PyInstaller file data loaded during setup."""
        box = box_pyinstaller.PyInstaller(self.compiled_script_path, self.dest_dir)
        children = box.get_children()
        self.assertEqual(len(children), 2)

        self.assertIn(self.compiled_script_name, self.get_child_names(children))

        # count 1 file ending with .pyz, since different PyInstaller versions may change this filename
        count = 0
        for child in children:
            if child.name.endswith(".pyz"):
                count += 1

        self.assertEqual(count, 1)

        # Python version is whatever this is
        version_string = "Python {}.{}".format(sys.version_info[0], sys.version_info[1])

        meta = box.get_meta()
        self.assertEqual(meta.get("python_version"), version_string)

        # no compile time in .pyc header (note: this changes between versions, as of latest this is None)
        self.assertEqual(meta.get("python_compile_time"), None)

        # os should be in there correctly
        self.assertIn(meta.get("pyinstaller_build_platform").lower(), sys.platform)

        # check on pyc contents
        child = self.get_child(children, self.compiled_script_name)

        # python bytcode header
        # note: as of 5.3+, the header is missing and a fake one installed by pyinstaller_unpacker
        self.assertTrue(child.raw_data[2:4] in (b"\x0d\x0a", b"\x00\x00"))
        self.assertIn(b"Hello testing world!", child.raw_data)

        # python libraries
        # these might change with different PyInstaller versions, so just look for a subset of libs that
        # MUST be included in the installer, such as those explicitly imported into the main test script
        # plus some others that PyInstaller needs to bootstrap
        expected_libraries = ["pprint", "PyInstaller", "dis"]
        for lib in expected_libraries:
            self.assertIn(lib, meta.get("python_libraries"))

        self.assertNotIn("exchangelib", meta.get("python_libraries"))

    def test_corrupted(self):
        """Test whether intentionally corrupted file throws NotSupported for corrupted file."""
        box = box_pyinstaller.PyInstaller(self.corrupted_script_path, self.dest_dir)
        self.assertRaises(NotSupported, box.extract)
