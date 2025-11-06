"""

azul_plugin_unbox py2exe test cases

"""

import datetime

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestPyInstallerArchive(BaseUnboxPluginTest):
    unbox_result_key = "py2exe"
    unbox_type_key = "executable/pe32"

    def test_invalid_file(self):
        self.complete_double_optout_test(
            self.load_test_file_bytes(
                "fb5757c13b6be5ddfcc5df34110bd742ec39d572fc12090af877b842e6569026",
                "Benign PDF appended with additional data.",
            ),
            opt_out_type_override="PDF",
        )

    def test_invalid_exe(self):
        """
        Test on exe that isn't a py2exe file
        """
        self.complete_double_optout_test(
            self.load_test_file_bytes(
                "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                "Benign WIN32 EXE, python library executable python_mcp.exe",
            ),
            opt_out_type_override="EXE",
        )

    def test_py2exe_1(self):
        """
        Test on py2exe file stitch (ec993ff561cbc175953502452bfa554a)
        :return:
        """
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "5cf8e07fb186ca108d5006f138c1f3477c7cac4e138728d0739075f38d129c1c",
                    "Malicious Windows 32 EXE, malware family redcap.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="5cf8e07fb186ca108d5006f138c1f3477c7cac4e138728d0739075f38d129c1c",
                        features={
                            "box_count": [FV("1")],
                            "box_filepath": [FV("st_main.pyc")],
                            "box_type": [FV("py2exe")],
                            "py2exe_build_time": [FV("2017-02-14T06:38:00")],
                            "python_library": [
                                FV("Cookie"),
                                FV("Crypto"),
                                FV("PIL"),
                                FV("Queue"),
                                FV("StringIO"),
                                FV("UserDict"),
                                FV("_LWPCookieJar"),
                                FV("_MozillaCookieJar"),
                                FV("__future__"),
                                FV("_abcoll"),
                                FV("_strptime"),
                                FV("_threading_local"),
                                FV("_weakrefset"),
                                FV("abc"),
                                FV("atexit"),
                                FV("base64"),
                                FV("bdb"),
                                FV("bisect"),
                                FV("calendar"),
                                FV("cgi"),
                                FV("cmd"),
                                FV("codecs"),
                                FV("collections"),
                                FV("colorsys"),
                                FV("contextlib"),
                                FV("cookielib"),
                                FV("copy"),
                                FV("copy_reg"),
                                FV("creddump"),
                                FV("ctypes"),
                                FV("decimal"),
                                FV("difflib"),
                                FV("dis"),
                                FV("distutils"),
                                FV("doctest"),
                                FV("dummy_thread"),
                                FV("dummy_threading"),
                                FV("email"),
                                FV("encodings"),
                                FV("fnmatch"),
                                FV("fractions"),
                                FV("ftplib"),
                                FV("functools"),
                                FV("genericpath"),
                                FV("getopt"),
                                FV("getpass"),
                                FV("gettext"),
                                FV("glob"),
                                FV("gzip"),
                                FV("hashlib"),
                                FV("heapq"),
                                FV("hmac"),
                                FV("httplib"),
                                FV("inspect"),
                                FV("io"),
                                FV("json"),
                                FV("keyword"),
                                FV("linecache"),
                                FV("locale"),
                                FV("logging"),
                                FV("md5"),
                                FV("mimetools"),
                                FV("mimetypes"),
                                FV("mss"),
                                FV("netbios"),
                                FV("netrc"),
                                FV("new"),
                                FV("ntpath"),
                                FV("nturl2path"),
                                FV("numbers"),
                                FV("opcode"),
                                FV("optparse"),
                                FV("os"),
                                FV("os2emxpath"),
                                FV("pdb"),
                                FV("pickle"),
                                FV("pipes"),
                                FV("platform"),
                                FV("plistlib"),
                                FV("posixpath"),
                                FV("pprint"),
                                FV("pyHook"),
                                FV("py_compile"),
                                FV("pyreadline"),
                                FV("quopri"),
                                FV("random"),
                                FV("re"),
                                FV("readline"),
                                FV("repr"),
                                FV("requests"),
                                FV("rfc822"),
                                FV("sets"),
                                FV("shlex"),
                                FV("shutil"),
                                FV("smtplib"),
                                FV("socket"),
                                FV("sre"),
                                FV("sre_compile"),
                                FV("sre_constants"),
                                FV("sre_parse"),
                                FV("ssl"),
                                FV("st_encryption"),
                                FV("st_protocol"),
                                FV("st_utils"),
                                FV("st_win_keylogger"),
                                FV("stat"),
                                FV("string"),
                                FV("stringprep"),
                                FV("struct"),
                                FV("subprocess"),
                                FV("tarfile"),
                                FV("tempfile"),
                                FV("textwrap"),
                                FV("threading"),
                                FV("token"),
                                FV("tokenize"),
                                FV("traceback"),
                                FV("types"),
                                FV("unittest"),
                                FV("urllib"),
                                FV("urllib2"),
                                FV("urlparse"),
                                FV("uu"),
                                FV("uuid"),
                                FV("warnings"),
                                FV("weakref"),
                                FV("win32con"),
                                FV("win32evtlogutil"),
                                FV("winerror"),
                                FV("xml"),
                                FV("zipextimporter"),
                                FV("zipfile"),
                            ],
                            "python_version": [FV("Python 2.7")],
                        },
                    ),
                    Event(
                        sha256="dcfda9fa44c91e8567d81e224f30dc373e07043bd9a32c0f127f5b065dcc3572",
                        parent=EventParent(sha256="5cf8e07fb186ca108d5006f138c1f3477c7cac4e138728d0739075f38d129c1c"),
                        relationship={"action": "unpacked"},
                        data=[
                            EventData(
                                hash="dcfda9fa44c91e8567d81e224f30dc373e07043bd9a32c0f127f5b065dcc3572",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("st_main.pyc")]},
                    ),
                ],
                data={"dcfda9fa44c91e8567d81e224f30dc373e07043bd9a32c0f127f5b065dcc3572": b""},
            ),
        )

    def test_py2exe_2(self):
        """
        Test on py2exe file zjrm (8e469a3c88968a7790a4b74c1ce56f80)
        :return:
        """
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "0565ead1f29f6ee0ee0cdb3d355b4e65d779cca8e5cf244cae169a61bb6b8a0e",
                    "Malicious Windows 32EXE Python based.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="0565ead1f29f6ee0ee0cdb3d355b4e65d779cca8e5cf244cae169a61bb6b8a0e",
                        features={
                            "box_count": [FV("1")],
                            "box_filepath": [FV("ZJRM.pyc")],
                            "box_type": [FV("py2exe")],
                            "python_version": [FV("Python 2.7")],
                        },
                    ),
                    Event(
                        sha256="f13fa6cf3cd72187030e47025344820bd55b2c7d8cb78268e91beeb20168a94e",
                        parent=EventParent(sha256="0565ead1f29f6ee0ee0cdb3d355b4e65d779cca8e5cf244cae169a61bb6b8a0e"),
                        relationship={"action": "unpacked"},
                        data=[
                            EventData(
                                hash="f13fa6cf3cd72187030e47025344820bd55b2c7d8cb78268e91beeb20168a94e",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("ZJRM.pyc")]},
                    ),
                ],
                data={"f13fa6cf3cd72187030e47025344820bd55b2c7d8cb78268e91beeb20168a94e": b""},
            ),
        )

    def test_py2exe_3(self):
        """
        Test on py2exe file proxy (297d8962ce0881a6ed086be53184d7b4)
        :return:
        """
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "dbc0c1b3c94b36d47510af7ad3e6f72133917e8f02c569a02533cbea60989b3d",
                    "Malicious Windows 32EXE Python based.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="dbc0c1b3c94b36d47510af7ad3e6f72133917e8f02c569a02533cbea60989b3d",
                        features={
                            "box_count": [FV("1")],
                            "box_filepath": [FV("proxy.pyc")],
                            "box_type": [FV("py2exe")],
                            "py2exe_build_time": [FV("2010-05-01T12:45:30")],
                            "python_library": [
                                FV("BaseHTTPServer"),
                                FV("SocketServer"),
                                FV("StringIO"),
                                FV("UserDict"),
                                FV("_LWPCookieJar"),
                                FV("_MozillaCookieJar"),
                                FV("__future__"),
                                FV("_abcoll"),
                                FV("_strptime"),
                                FV("_threading_local"),
                                FV("abc"),
                                FV("atexit"),
                                FV("base64"),
                                FV("bdb"),
                                FV("bisect"),
                                FV("calendar"),
                                FV("cmd"),
                                FV("codecs"),
                                FV("collections"),
                                FV("common"),
                                FV("cookielib"),
                                FV("copy"),
                                FV("copy_reg"),
                                FV("difflib"),
                                FV("dis"),
                                FV("doctest"),
                                FV("dummy_thread"),
                                FV("dummy_threading"),
                                FV("email"),
                                FV("encodings"),
                                FV("fnmatch"),
                                FV("ftplib"),
                                FV("functools"),
                                FV("genericpath"),
                                FV("getopt"),
                                FV("getpass"),
                                FV("gettext"),
                                FV("hashlib"),
                                FV("heapq"),
                                FV("httplib"),
                                FV("inspect"),
                                FV("keyword"),
                                FV("linecache"),
                                FV("locale"),
                                FV("logging"),
                                FV("macurl2path"),
                                FV("mainform_ui"),
                                FV("mimetools"),
                                FV("mimetypes"),
                                FV("ntpath"),
                                FV("nturl2path"),
                                FV("opcode"),
                                FV("optparse"),
                                FV("os"),
                                FV("os2emxpath"),
                                FV("pdb"),
                                FV("pickle"),
                                FV("posixpath"),
                                FV("pprint"),
                                FV("quopri"),
                                FV("random"),
                                FV("re"),
                                FV("repr"),
                                FV("rfc822"),
                                FV("shlex"),
                                FV("socket"),
                                FV("sre"),
                                FV("sre_compile"),
                                FV("sre_constants"),
                                FV("sre_parse"),
                                FV("ssl"),
                                FV("stat"),
                                FV("string"),
                                FV("stringprep"),
                                FV("struct"),
                                FV("subprocess"),
                                FV("tempfile"),
                                FV("textwrap"),
                                FV("threading"),
                                FV("token"),
                                FV("tokenize"),
                                FV("traceback"),
                                FV("types"),
                                FV("unittest"),
                                FV("urllib"),
                                FV("urllib2"),
                                FV("urlparse"),
                                FV("uu"),
                                FV("warnings"),
                                FV("zipextimporter"),
                            ],
                            "python_version": [FV("Python 2.6")],
                        },
                    ),
                    Event(
                        sha256="6c1d9c1084def7141ad31ce082fd910e5463f80516a48a3ca112381b7904c197",
                        parent=EventParent(sha256="dbc0c1b3c94b36d47510af7ad3e6f72133917e8f02c569a02533cbea60989b3d"),
                        relationship={"action": "unpacked"},
                        data=[
                            EventData(
                                hash="6c1d9c1084def7141ad31ce082fd910e5463f80516a48a3ca112381b7904c197",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("proxy.pyc")]},
                    ),
                ],
                data={"6c1d9c1084def7141ad31ce082fd910e5463f80516a48a3ca112381b7904c197": b""},
            ),
        )

    def test_py2exe_bad_exe_case(self):
        """Test on py2exe file (b5324ae4cec7bd7b837a726eccf140c1f0ebde82479db919546fe35f4b9439c7).

        The executable doesn't have DIRECTORY_ENTRY_RESOURCE's which causes a fail during extraction.
        """
        self.complete_double_optout_test(
            self.load_test_file_bytes(
                "b5324ae4cec7bd7b837a726eccf140c1f0ebde82479db919546fe35f4b9439c7", "Malicious Windows 32EXE, RAT."
            )
        )
