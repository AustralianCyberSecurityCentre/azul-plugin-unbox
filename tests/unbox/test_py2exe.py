import os.path

from azul_runner.test_utils import FileManager

from azul_plugin_unbox.unbox.box import box_py2exe
from tests.unbox.base_test import BaseFileTest


class Py2ExeTest(BaseFileTest):
    """Test Suite for Py2Exe unboxer."""

    def setUp(self):
        """Initialise some data for the test cases.

        Read in stored test file and decode base64 data
        Py2Exe is Windows native, so we can't build an installer here easily
        """
        super().setUp()
        self.py2exe_file_path = os.path.join(self.src_dir, "stitch.exe")

        with open(self.py2exe_file_path, "wb") as f:
            # Malicious Windows 32 EXE, malware family redcap.
            f.write(
                self.file_manager.download_file_bytes(
                    "5cf8e07fb186ca108d5006f138c1f3477c7cac4e138728d0739075f38d129c1c"
                )
            )

    def test_py2exe(self):
        """Test unpacking the test Py2Exe file (stitch.exe)."""
        box = box_py2exe.Py2Exe(self.py2exe_file_path, self.dest_dir)
        children = box.get_children()
        self.assertEqual(len(children), 1)

        # correct files were extracted
        self.assertIn("st_main.pyc", self.get_child_names(children))
        child = self.get_child(children, "st_main.pyc")

        self.assertEqual(child.raw_data[:16], b"\x03\xf3\x0d\x0a\xc8\xa5\xa2\x58\x63\x00\x00\x00\x00\x00\x00\x00")

        meta = box.get_meta()
        self.assertEqual(meta.get("python_version"), "Python 2.7")

        self.assertEqual(meta.get("python_compile_time"), "2017-02-14T06:38:00")

        # python libraries
        expected_libraries = [
            "Cookie",
            "Queue",
            "StringIO",
            "UserDict",
            "_LWPCookieJar",
            "_MozillaCookieJar",
            "__future__",
            "_abcoll",
            "_strptime",
            "_threading_local",
            "_weakrefset",
            "abc",
            "atexit",
            "base64",
            "bdb",
            "bisect",
            "calendar",
            "cgi",
            "cmd",
            "codecs",
            "collections",
            "colorsys",
            "contextlib",
            "cookielib",
            "copy",
            "copy_reg",
            "ctypes",
            "decimal",
            "difflib",
            "dis",
            "distutils",
            "doctest",
            "dummy_thread",
            "dummy_threading",
            "email",
            "encodings",
            "fnmatch",
            "fractions",
            "ftplib",
            "functools",
            "genericpath",
            "getopt",
            "getpass",
            "gettext",
            "glob",
            "gzip",
            "hashlib",
            "heapq",
            "hmac",
            "httplib",
            "inspect",
            "io",
            "json",
            "keyword",
            "linecache",
            "locale",
            "logging",
            "md5",
            "mimetools",
            "mimetypes",
            "netrc",
            "new",
            "ntpath",
            "nturl2path",
            "numbers",
            "opcode",
            "optparse",
            "os",
            "os2emxpath",
            "pdb",
            "pickle",
            "pipes",
            "platform",
            "plistlib",
            "posixpath",
            "pprint",
            "py_compile",
            "quopri",
            "random",
            "re",
            "readline",
            "repr",
            "rfc822",
            "sets",
            "shlex",
            "shutil",
            "smtplib",
            "socket",
            "sre",
            "sre_compile",
            "sre_constants",
            "sre_parse",
            "ssl",
            "stat",
            "string",
            "stringprep",
            "struct",
            "subprocess",
            "tarfile",
            "tempfile",
            "textwrap",
            "threading",
            "token",
            "tokenize",
            "traceback",
            "types",
            "unittest",
            "urllib",
            "urllib2",
            "urlparse",
            "uu",
            "uuid",
            "warnings",
            "weakref",
            "xml",
            "zipfile",
            "Crypto",
            "PIL",
            "creddump",
            "mss",
            "netbios",
            "pyHook",
            "pyreadline",
            "requests",
            "st_encryption",
            "st_protocol",
            "st_utils",
            "st_win_keylogger",
            "win32con",
            "win32evtlogutil",
            "winerror",
            "zipextimporter",
        ]
        self.assertCountEqual(meta.get("python_libraries"), expected_libraries)
