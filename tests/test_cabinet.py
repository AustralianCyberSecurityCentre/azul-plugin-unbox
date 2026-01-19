"""
Cabinet plugin test suite
"""

import datetime

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "cab"
    unbox_type_key = "archive/cabinet"

    def test_cabinet(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "d94e06452910c3ab448ccf929f9cc28df85288deeb488fe7d1123d53ea854f8e",
                    "Basic Cab file with two test files in it.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="d94e06452910c3ab448ccf929f9cc28df85288deeb488fe7d1123d53ea854f8e",
                        features={
                            "box_count": [FV(2)],
                            "box_filepath": [FV("test1.txt"), FV("test2.txt")],
                            "box_insertdate": [
                                FV(datetime.datetime(2018, 3, 12, 0, 40, 32), label="test2.txt"),
                                FV(datetime.datetime(2018, 3, 12, 0, 40, 36), label="test1.txt"),
                            ],
                            "box_type": [FV("cab")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="d94e06452910c3ab448ccf929f9cc28df85288deeb488fe7d1123d53ea854f8e",
                        ),
                        entity_type="binary",
                        entity_id="a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test1.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="d94e06452910c3ab448ccf929f9cc28df85288deeb488fe7d1123d53ea854f8e",
                        ),
                        entity_type="binary",
                        entity_id="837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test2.txt")]},
                    ),
                ],
                data={
                    "a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063": b"",
                    "837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72": b"",
                },
            ),
        )

    def test_self_extracting_cab(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "1060151b539e5cfd4ca5e4dbeba5afb92ca29b37bd5def6df535615c08c5d59d", "Benign self extracting Cab."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="1060151b539e5cfd4ca5e4dbeba5afb92ca29b37bd5def6df535615c08c5d59d",
                        features={
                            "box_count": [FV(2)],
                            "box_filepath": [FV("test1.txt"), FV("test2.txt")],
                            "box_insertdate": [
                                FV(datetime.datetime(2018, 3, 12, 0, 40, 32), label="test2.txt"),
                                FV(datetime.datetime(2018, 3, 12, 0, 40, 36), label="test1.txt"),
                            ],
                            "box_type": [FV("cab")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="1060151b539e5cfd4ca5e4dbeba5afb92ca29b37bd5def6df535615c08c5d59d",
                        ),
                        entity_type="binary",
                        entity_id="a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test1.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="1060151b539e5cfd4ca5e4dbeba5afb92ca29b37bd5def6df535615c08c5d59d",
                        ),
                        entity_type="binary",
                        entity_id="837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test2.txt")]},
                    ),
                ],
                data={
                    "a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063": b"",
                    "837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72": b"",
                },
            ),
        )

    def test_not_cab(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a", "Benign RAR."
                ),
                format_override="unknown",
            ),
            JobResult(
                state=State(
                    State.Label.OPT_OUT,
                    failure_name="wrong_file_type",
                    message="wrong file type 'archive/rar' provided",
                )
            ),
        )

    def test_not_cab2(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                    "Benign WIN32 EXE, python library executable python_mcp.exe",
                ),
                format_override="archive/cabinet",
            ),
            JobResult(state=State(State.Label.OPT_OUT, failure_name="not_cab", message="not a cab file")),
        )
