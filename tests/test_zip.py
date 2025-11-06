"""
Zip plugin test suite
"""

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from azul_plugin_unbox.main import AzulPluginUnbox
from azul_plugin_unbox.multi_unbox.zip import Zip as ZipPluginBox
from tests.base_test import BaseUnboxPluginTest


class AzulPluginUnboxWithZip(AzulPluginUnbox):
    ACTIVE_UNBOX = [ZipPluginBox()]


class TestExecute(BaseUnboxPluginTest):
    PLUGIN_TO_TEST = AzulPluginUnboxWithZip

    unbox_result_key = "zip"
    unbox_type_key = "archive/zip"

    def test_zip_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "a95306380a9295bd82603050252a4720eaf7e5425f53ff4fc1d4b4e99d05e71e", "Benign Zip Passworded."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="a95306380a9295bd82603050252a4720eaf7e5425f53ff4fc1d4b4e99d05e71e",
                        features={
                            "box_compression": [
                                FV("Deflate", label="test_file_1.txt"),
                                FV("Deflate", label="test_file_2.txt"),
                            ],
                            "box_count": [FV("2")],
                            "box_filepath": [FV("test_file_1.txt"), FV("test_file_2.txt")],
                            "box_insertdate": [
                                FV("2016-07-14T16:08:02", label="test_file_1.txt"),
                                FV("2016-07-14T16:08:22", label="test_file_2.txt"),
                            ],
                            "box_password": [FV("password")],
                            "box_type": [FV("zip")],
                            "password": [FV("password")],
                        },
                    ),
                    Event(
                        sha256="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
                        parent=EventParent(sha256="a95306380a9295bd82603050252a4720eaf7e5425f53ff4fc1d4b4e99d05e71e"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_file_1.txt")]},
                    ),
                    Event(
                        sha256="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                        parent=EventParent(sha256="a95306380a9295bd82603050252a4720eaf7e5425f53ff4fc1d4b4e99d05e71e"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_file_2.txt")]},
                    ),
                ],
                data={
                    "77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0": b"",
                    "816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b": b"",
                },
            ),
        )

    def test_zip_password_infected(self):
        result = self.do_execution(
            entity_attrs={"file_format": self.unbox_type_key},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "5638509ad8880d35711bed55834ea2e007e90f01cdb5528ac43fad8a26d5a3fa",
                        "Malicious Zip password protected.",
                    ),
                ),
            ],
        )
        self.assertJobResult(
            result.get(self.unbox_result_key),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="That compression method is not supported")),
        )

    def test_zip_password_supplied(self):
        result = self.do_execution(
            entity_attrs={"file_format": self.unbox_type_key},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "2f7701b74e2c2a0908062150ab3f373b1abeaf6da793cb5433d65a479e07244a", "Benign Zip Passworded"
                    ),
                ),
                ("password_dictionary", b"foobar\nmonkeys\ndish water\n00965abcZ\nhello"),
            ],
        )
        self.assertJobResult(
            result.get(self.unbox_result_key),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="2f7701b74e2c2a0908062150ab3f373b1abeaf6da793cb5433d65a479e07244a",
                        features={
                            "box_compression": [FV("Store", label="testing/secret.txt")],
                            "box_count": [FV("2")],
                            "box_filepath": [FV("testing/"), FV("testing/secret.txt")],
                            "box_insertdate": [FV("2021-02-06T18:20:46", label="testing/secret.txt")],
                            "box_password": [FV("00965abcZ")],
                            "box_type": [FV("zip")],
                            "password": [FV("00965abcZ")],
                        },
                    ),
                    Event(
                        sha256="2dd1024397903525cc168d4e1ae7106c89c5385374694908815e42b657b6be98",
                        parent=EventParent(sha256="2f7701b74e2c2a0908062150ab3f373b1abeaf6da793cb5433d65a479e07244a"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="2dd1024397903525cc168d4e1ae7106c89c5385374694908815e42b657b6be98",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("testing/secret.txt")]},
                    ),
                ],
                data={"2dd1024397903525cc168d4e1ae7106c89c5385374694908815e42b657b6be98": b""},
            ),
        )

    def test_zip_that_has_discarded_contents(self):
        result = self.do_execution(
            ent_id="not_test_entity",
            entity_attrs={"file_format": self.unbox_type_key},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "7c5e3b3de7257c6f13eb5104cc8afdb09d1c54010a156cba7d046bd98d364dd3",
                        "Benign Zip containing a file with text pretending to be a java class.",
                    ),
                ),
            ],
            verify_input_content=False,
        )
        self.assertJobResult(
            result.get(self.unbox_result_key),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="not_test_entity",
                        features={
                            "box_compression": [FV("Store", label="java_cls/fake_java.class")],
                            "box_count": [FV("3")],
                            "box_filepath": [FV("java_cls/"), FV("java_cls/fake_java.class")],
                            "box_insertdate": [FV("2023-12-18T06:24:24", label="java_cls/fake_java.class")],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="105b87ff8c2a1176305a66862b2c9c183f42b4b4da3751c089a057fd8d16ec8a",
                        parent=EventParent(sha256="not_test_entity"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="105b87ff8c2a1176305a66862b2c9c183f42b4b4da3751c089a057fd8d16ec8a",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("java_cls/fake_java.class")]},
                    ),
                ],
                data={"105b87ff8c2a1176305a66862b2c9c183f42b4b4da3751c089a057fd8d16ec8a": b""},
            ),
        )

    def test_invalid_date(self):
        # this sample has an invalid date so doesnt publish box_insertdate
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "ef10a5d28a29fbd9bc67fdba50b56f17f3d606df486278ff0e08c147ac32a343",
                    "Benign Zip, invalid child date.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="ef10a5d28a29fbd9bc67fdba50b56f17f3d606df486278ff0e08c147ac32a343",
                        features={
                            "box_compression": [
                                FV(
                                    "Deflate",
                                    label="C:\\Users\\GS\\AppData\\Local\\Temp\\Revit{98966E87-00E3-4C25-853F-2CD8513CD241}.project.xml",
                                )
                            ],
                            "box_count": [FV("1")],
                            "box_filepath": [
                                FV(
                                    "C:\\Users\\GS\\AppData\\Local\\Temp\\Revit{98966E87-00E3-4C25-853F-2CD8513CD241}.project.xml"
                                )
                            ],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="6aa718e2d29c2a29789985ab3379acb56e22f23cd1403092ac4711fcca22ba1b",
                        parent=EventParent(sha256="ef10a5d28a29fbd9bc67fdba50b56f17f3d606df486278ff0e08c147ac32a343"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="6aa718e2d29c2a29789985ab3379acb56e22f23cd1403092ac4711fcca22ba1b",
                                label="content",
                            )
                        ],
                        features={
                            "filename": [
                                FV(
                                    "C:\\Users\\GS\\AppData\\Local\\Temp\\Revit{98966E87-00E3-4C25-853F-2CD8513CD241}.project.xml"
                                )
                            ]
                        },
                    ),
                ],
                data={"6aa718e2d29c2a29789985ab3379acb56e22f23cd1403092ac4711fcca22ba1b": b""},
            ),
        )

    def test_corrupt_zip(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "26fe4537855d5afd036e77e042a735e80cc611653255b5a1cf75e065fa20ce8e", "Benign Corrupted Zip file."
                )
            ),
            JobResult(
                state=State(
                    State.Label.ERROR_EXCEPTION,
                    message="Error -3 while decompressing data: invalid code lengths set...",
                )
            ),
        )

    def test_not_zip(self):
        self.complete_error_and_optout_test(
            self.load_test_file_bytes(
                "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                "Benign WIN32 EXE, python library executable python_mcp.exe",
            )
        )
