"""
CHM plugin test suite
"""

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "chm"
    unbox_type_key = "archive/chm"

    def test_chm(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866", "Benign CHM file."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866",
                        features={
                            "box_count": [FV(5)],
                            "box_filepath": [
                                FV("/Content/Main.htm"),
                                FV("/Content/Page.htm"),
                                FV("/Project.hhc"),
                                FV("/Project.hhk"),
                                FV("/_#_README_#_"),
                            ],
                            "box_type": [FV("chm")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866",
                        ),
                        entity_type="binary",
                        entity_id="5edf10501797afcc8c8612a83f847c1f9f0a5c4eac401cab9a9ffab8e01a76c3",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="5edf10501797afcc8c8612a83f847c1f9f0a5c4eac401cab9a9ffab8e01a76c3",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("/Content/Main.htm")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866",
                        ),
                        entity_type="binary",
                        entity_id="2f6ea5d512de1d24baac526aa837371e7a1b15c5f3f31edb52f88ded4eba57f5",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="2f6ea5d512de1d24baac526aa837371e7a1b15c5f3f31edb52f88ded4eba57f5",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("/Content/Page.htm")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866",
                        ),
                        entity_type="binary",
                        entity_id="5e47de2c21ac971e405fcd0bc54888e080a9e317bd0d1737bcac52c1601f5f92",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="5e47de2c21ac971e405fcd0bc54888e080a9e317bd0d1737bcac52c1601f5f92",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("/Project.hhc")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866",
                        ),
                        entity_type="binary",
                        entity_id="83302c10e4838a67ceb39d3f11250251135e56e221701f8eecf5263d6de30577",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="83302c10e4838a67ceb39d3f11250251135e56e221701f8eecf5263d6de30577",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("/Project.hhk")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fceea1b3c32d67438b25d775fa80b6afc3241a40ebb5dc4eee7aeacce4fd9866",
                        ),
                        entity_type="binary",
                        entity_id="348773b69aeb3549b7dca28e899adb488b50c9958e99ab26b494eb02646f3d3b",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="348773b69aeb3549b7dca28e899adb488b50c9958e99ab26b494eb02646f3d3b",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("/_#_README_#_")]},
                    ),
                ],
                data={
                    "5edf10501797afcc8c8612a83f847c1f9f0a5c4eac401cab9a9ffab8e01a76c3": b"",
                    "2f6ea5d512de1d24baac526aa837371e7a1b15c5f3f31edb52f88ded4eba57f5": b"",
                    "5e47de2c21ac971e405fcd0bc54888e080a9e317bd0d1737bcac52c1601f5f92": b"",
                    "83302c10e4838a67ceb39d3f11250251135e56e221701f8eecf5263d6de30577": b"",
                    "348773b69aeb3549b7dca28e899adb488b50c9958e99ab26b494eb02646f3d3b": b"",
                },
            ),
        )

    def test_not_chm(self):
        self.complete_error_and_optout_test(
            self.load_test_file_bytes(
                "3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a", "Benign RAR."
            )
        )
