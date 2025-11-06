"""
Rar plugin test suite
"""

import datetime

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "rar"
    unbox_type_key = "archive/rar"

    def test_rar_bad_permissions(self):
        # this file has read only files within it
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "cf0317395708f762a7b0abf0c7e37466c5236e96fbccd5fc0e10ce5922fa3f0a",
                    "RAR with bad permissions within the archive.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="cf0317395708f762a7b0abf0c7e37466c5236e96fbccd5fc0e10ce5922fa3f0a",
                        features={
                            "box_count": [FV("1")],
                            "box_filepath": [FV("notepad.exe")],
                            "box_insertdate": [FV("2025-10-15T00:10:20", label="notepad.exe")],
                            "box_type": [FV("rar")],
                            "rar_compression": [FV("51", label="notepad.exe")],
                        },
                    ),
                    Event(
                        sha256="1552f6a579b77b61460df56cb4b2ce0a34fe96b6176829d7916275b806edc2bb",
                        parent=EventParent(sha256="cf0317395708f762a7b0abf0c7e37466c5236e96fbccd5fc0e10ce5922fa3f0a"),
                        relationship={"action": "unrar"},
                        data=[
                            EventData(
                                hash="1552f6a579b77b61460df56cb4b2ce0a34fe96b6176829d7916275b806edc2bb",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("notepad.exe")]},
                    ),
                ],
                data={"1552f6a579b77b61460df56cb4b2ce0a34fe96b6176829d7916275b806edc2bb": b""},
            ),
        )

    def test_rar_no_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a", "Benign RAR."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a",
                        features={
                            "box_count": [FV(2)],
                            "box_filepath": [FV("test_file_1.txt"), FV("test_file_2.txt")],
                            "box_insertdate": [
                                FV(datetime.datetime(2016, 7, 14, 16, 8, 1), label="test_file_1.txt"),
                                FV(datetime.datetime(2016, 7, 14, 16, 8, 22), label="test_file_2.txt"),
                            ],
                            "box_type": [FV("rar")],
                            "rar_compression": [FV(51, label="test_file_1.txt"), FV(51, label="test_file_2.txt")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a",
                        ),
                        entity_type="binary",
                        entity_id="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
                        relationship={"action": "unrar"},
                        data=[
                            EventData(
                                hash="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_file_1.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a",
                        ),
                        entity_type="binary",
                        entity_id="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                        relationship={"action": "unrar"},
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

    def test_rar_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "7e92d460ef92f94f1840296206a2c82f3f6f90f971b4fdef6b626b1836657cc3", "Benign RAR file."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="7e92d460ef92f94f1840296206a2c82f3f6f90f971b4fdef6b626b1836657cc3",
                        features={
                            "box_count": [FV(2)],
                            "box_filepath": [FV("test_file_1.txt"), FV("test_file_2.txt")],
                            "box_insertdate": [
                                FV(datetime.datetime(2016, 7, 14, 16, 8, 1), label="test_file_1.txt"),
                                FV(datetime.datetime(2016, 7, 14, 16, 8, 22), label="test_file_2.txt"),
                            ],
                            "box_password": [FV("password")],
                            "box_type": [FV("rar")],
                            "password": [FV("password")],
                            "rar_compression": [FV(51, label="test_file_1.txt"), FV(51, label="test_file_2.txt")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="7e92d460ef92f94f1840296206a2c82f3f6f90f971b4fdef6b626b1836657cc3",
                        ),
                        entity_type="binary",
                        entity_id="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
                        relationship={"action": "unrar"},
                        data=[
                            EventData(
                                hash="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_file_1.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="7e92d460ef92f94f1840296206a2c82f3f6f90f971b4fdef6b626b1836657cc3",
                        ),
                        entity_type="binary",
                        entity_id="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                        relationship={"action": "unrar"},
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

    def test_rar_unknown_password(self):
        # If we force it to run anyway, it should give an entity error
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "fb7242e3b6fa9959862852cd03f141e1311bbbdd49f84dfc692ade088a0846e3",
                    "Benign unknown passworded RAR.",
                )
            ),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="Failed to guess password")),
        )

    def test_not_rar(self):
        # If we force it to run anyway, it should give an entity error
        result = self.do_execution(
            ent_id="not_a_test_entity_to_allow_type_override",  # Disables base_test from calculating type.
            entity_attrs={"file_format": "archive/rar"},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                        "Benign WIN32 EXE, python library executable python_mcp.exe",
                    ),
                )
            ],
            verify_input_content=False,
        )
        self.assertJobResult(
            result.get("rar"),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="Not a RAR file")),
        )
