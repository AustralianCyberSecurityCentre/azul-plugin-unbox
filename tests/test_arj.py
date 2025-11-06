"""
Arj plugin test suite.
"""

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "arj"
    unbox_type_key = "archive/arj"

    def test_arj(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "74250bf1c1eb94b9ea4c2c5496e8abfa2118417856890a6e502dcfd3d627c3f2", "Benign Arj file."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="74250bf1c1eb94b9ea4c2c5496e8abfa2118417856890a6e502dcfd3d627c3f2",
                        features={
                            "box_count": [FV(3)],
                            "box_filepath": [
                                FV("test_file_1.txt"),
                                FV("test_file_2.txt"),
                                FV("test_subdir_file.txt"),
                            ],
                            "box_type": [FV("arj")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="74250bf1c1eb94b9ea4c2c5496e8abfa2118417856890a6e502dcfd3d627c3f2",
                        ),
                        entity_type="binary",
                        entity_id="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
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
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="74250bf1c1eb94b9ea4c2c5496e8abfa2118417856890a6e502dcfd3d627c3f2",
                        ),
                        entity_type="binary",
                        entity_id="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_file_2.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="74250bf1c1eb94b9ea4c2c5496e8abfa2118417856890a6e502dcfd3d627c3f2",
                        ),
                        entity_type="binary",
                        entity_id="c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_subdir_file.txt")]},
                    ),
                ],
                data={
                    "77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0": b"",
                    "816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b": b"",
                    "c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0": b"",
                },
            ),
        )

    def test_arj_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "992fa72f92e9b57ede1ba5e7e947f71019f60bde3a33d64d767c9e388f4a766b", "Benign ARJ file."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="992fa72f92e9b57ede1ba5e7e947f71019f60bde3a33d64d767c9e388f4a766b",
                        features={
                            "box_count": [FV(3)],
                            "box_filepath": [
                                FV("test_file_1.txt"),
                                FV("test_file_2.txt"),
                                FV("test_subdir_file.txt"),
                            ],
                            "box_password": [FV("password")],
                            "box_type": [FV("arj")],
                            "password": [FV("password")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="992fa72f92e9b57ede1ba5e7e947f71019f60bde3a33d64d767c9e388f4a766b",
                        ),
                        entity_type="binary",
                        entity_id="77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0",
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
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="992fa72f92e9b57ede1ba5e7e947f71019f60bde3a33d64d767c9e388f4a766b",
                        ),
                        entity_type="binary",
                        entity_id="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_file_2.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="992fa72f92e9b57ede1ba5e7e947f71019f60bde3a33d64d767c9e388f4a766b",
                        ),
                        entity_type="binary",
                        entity_id="c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test_subdir_file.txt")]},
                    ),
                ],
                data={
                    "77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0": b"",
                    "816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b": b"",
                    "c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0": b"",
                },
            ),
        )

    def test_not_arj(self):
        self.complete_error_and_optout_test(
            self.load_test_file_bytes(
                "3ad88941837affe0da7ec2f84e96773a5600c193e8bcbe27cc57e81d8c0c920a", "Benign RAR."
            ),
            "File Corrupt",
        )
