"""
7-Zip plugin test suite
"""

import datetime

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "sevenzip"
    unbox_type_key = "archive/7-zip"

    def test_7zip_cart_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "9329540cefd748499e57e228db64962b3583da8cc7af344ca70a02055810c587",
                    "Zip folder through of meme JPGs.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="9329540cefd748499e57e228db64962b3583da8cc7af344ca70a02055810c587",
                        features={
                            "box_compression": [
                                FV("ZipCrypto Deflate", label="made logo.png"),
                                FV("ZipCrypto Deflate", label="meme.jpg"),
                                FV("ZipCrypto Store", label="fruit.jpg"),
                            ],
                            "box_count": [FV("3")],
                            "box_filepath": [FV("fruit.jpg"), FV("made logo.png"), FV("meme.jpg")],
                            "box_insertdate": [
                                FV("2024-03-06T01:26:28.254446", label="made logo.png"),
                                FV("2024-04-08T00:20:35.846682", label="meme.jpg"),
                                FV("2024-04-08T00:21:26.640355", label="fruit.jpg"),
                            ],
                            "box_password": [FV("infected")],
                            "box_type": [FV("zip")],
                            "password": [FV("infected")],
                        },
                    ),
                    Event(
                        sha256="244bd963e1d786430a4ab968f2b161096377041b6fb80fe7093bdf108948f44e",
                        parent=EventParent(sha256="9329540cefd748499e57e228db64962b3583da8cc7af344ca70a02055810c587"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="244bd963e1d786430a4ab968f2b161096377041b6fb80fe7093bdf108948f44e",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("fruit.jpg")]},
                    ),
                    Event(
                        sha256="d151d27353f99cd05334fe6c7897fe61ee5e0b033303e354623f040b47b9e8af",
                        parent=EventParent(sha256="9329540cefd748499e57e228db64962b3583da8cc7af344ca70a02055810c587"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="d151d27353f99cd05334fe6c7897fe61ee5e0b033303e354623f040b47b9e8af",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("made logo.png")]},
                    ),
                    Event(
                        sha256="d70bec5f8299563a74d4f971c2df8d9ae739db4d38e285e64f30131a78ae8d3e",
                        parent=EventParent(sha256="9329540cefd748499e57e228db64962b3583da8cc7af344ca70a02055810c587"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="d70bec5f8299563a74d4f971c2df8d9ae739db4d38e285e64f30131a78ae8d3e",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("meme.jpg")]},
                    ),
                ],
                data={
                    "244bd963e1d786430a4ab968f2b161096377041b6fb80fe7093bdf108948f44e": b"",
                    "d151d27353f99cd05334fe6c7897fe61ee5e0b033303e354623f040b47b9e8af": b"",
                    "d70bec5f8299563a74d4f971c2df8d9ae739db4d38e285e64f30131a78ae8d3e": b"",
                },
            ),
        )

    def test_szip(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "c3febe226e1f1b140e9502780b3640a4d3f8e7f8f00edd4f492b6d9e8affa546", "Benign 7zip file."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="c3febe226e1f1b140e9502780b3640a4d3f8e7f8f00edd4f492b6d9e8affa546",
                        features={
                            "box_compression": [
                                FV("LZMA:16", label="test_dir/test_subdir_file.txt"),
                                FV("LZMA:16", label="test_file_1.txt"),
                                FV("LZMA:16", label="test_file_2.txt"),
                            ],
                            "box_count": [FV(3)],
                            "box_filepath": [
                                FV("test_dir/test_subdir_file.txt"),
                                FV("test_file_1.txt"),
                                FV("test_file_2.txt"),
                            ],
                            "box_insertdate": [
                                FV(datetime.datetime(2016, 7, 14, 6, 8, 1), label="test_file_1.txt"),
                                FV(datetime.datetime(2016, 7, 14, 6, 8, 22), label="test_file_2.txt"),
                                FV(datetime.datetime(2016, 7, 18, 3, 37, 31), label="test_dir/test_subdir_file.txt"),
                            ],
                            "box_type": [FV("sevenzip")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="c3febe226e1f1b140e9502780b3640a4d3f8e7f8f00edd4f492b6d9e8affa546",
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
                        features={"filename": [FV("test_dir/test_subdir_file.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="c3febe226e1f1b140e9502780b3640a4d3f8e7f8f00edd4f492b6d9e8affa546",
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
                            entity_id="c3febe226e1f1b140e9502780b3640a4d3f8e7f8f00edd4f492b6d9e8affa546",
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
                ],
                data={
                    "c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0": b"",
                    "77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0": b"",
                    "816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b": b"",
                },
            ),
        )

    def test_symbolic_link_directories(self):
        """Verify the plugin completes on directories with symbolic links."""
        result = self.get_result_from_cart(
            self.load_test_file_bytes(
                "c376d4b358dcc87c617ac68b257fb1a2a26baa2abc281ebb458e9d4ce20f4737", "Zip with symbolic links in it."
            )
        )
        self.assertEqual(result.state, State(State.Label.COMPLETED))

    def test_szip_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "ee27f61f5b1fa77c1bc1f2d52310da9022e1cb83078b15efdd517e3f91231bac", "Benign passworded 7zip."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="ee27f61f5b1fa77c1bc1f2d52310da9022e1cb83078b15efdd517e3f91231bac",
                        features={
                            "box_compression": [
                                FV("LZMA:16 7zAES:19", label="test_dir/test_subdir_file.txt"),
                                FV("LZMA:16 7zAES:19", label="test_file_1.txt"),
                                FV("LZMA:16 7zAES:19", label="test_file_2.txt"),
                            ],
                            "box_count": [FV(3)],
                            "box_filepath": [
                                FV("test_dir/test_subdir_file.txt"),
                                FV("test_file_1.txt"),
                                FV("test_file_2.txt"),
                            ],
                            "box_insertdate": [
                                FV(datetime.datetime(2016, 7, 14, 6, 8, 1), label="test_file_1.txt"),
                                FV(datetime.datetime(2016, 7, 14, 6, 8, 22), label="test_file_2.txt"),
                                FV(datetime.datetime(2016, 7, 18, 3, 37, 31), label="test_dir/test_subdir_file.txt"),
                            ],
                            "box_password": [FV("password")],
                            "box_type": [FV("sevenzip")],
                            "password": [FV("password")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="ee27f61f5b1fa77c1bc1f2d52310da9022e1cb83078b15efdd517e3f91231bac",
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
                        features={"filename": [FV("test_dir/test_subdir_file.txt")]},
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="ee27f61f5b1fa77c1bc1f2d52310da9022e1cb83078b15efdd517e3f91231bac",
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
                            entity_id="ee27f61f5b1fa77c1bc1f2d52310da9022e1cb83078b15efdd517e3f91231bac",
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
                ],
                data={
                    "c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0": b"",
                    "77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0": b"",
                    "816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b": b"",
                },
            ),
        )

    def test_szip_unknown_password(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "b52d5cda8bff897efcfbc1227a5edffa07d683cb57da9f607bd770c1cf1c483a",
                    "Zip file with an unknown password.",
                )
            ),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="Failed to guess password")),
        )

    def test_szip_broken(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "ec365eb8026cf58c69631d3a7d299b05ff0245993023946be74b7fa6ecb74163", "Corrupted 7zip file."
                )
            ),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="File Corrupt")),
        )

    def test_non_sevenzip_file(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "9589e0f02cd3065507f9b0119fd5215eb187227cbc0659468e2799966e942bb2", "Corrupted 7zip file."
                )
            ),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="File Corrupt")),
        )

    def test_missing_start_file(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "07b9cbf517556f656958de8b18e609056d281f787eddd8354aec4e5ef7654cf0",
                    "Benign 7zip file with it's front clipped.",
                )
            ),
            JobResult(
                state=State(State.Label.ERROR_EXCEPTION, message="7zip decode error: Unavailable start of archive")
            ),
        )

    def test_corrupted_file(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "435a43e36890006ef02db7217bc17ba0411c15f56199a59af061557364615cb1",
                    "Malicious Zip file, malware family strictor.",
                )
            ),
            JobResult(
                state=State(
                    State.Label.COMPLETED_WITH_ERRORS,
                    message="File Corrupt: Unexpected end of archive",
                )
            ),
        )

    def test_zip_extra_content_at_start(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "91e34fc6918dcaa1975b7cea8bf3ed874d52d51dc06f694ea1675dec44e6a076",
                    "Zip file with leading binary content added.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="91e34fc6918dcaa1975b7cea8bf3ed874d52d51dc06f694ea1675dec44e6a076",
                        features={
                            "box_compression": [FV("Deflate", label="nested/file_001.txt")],
                            "box_count": [FV("1")],
                            "box_filepath": [FV("nested/file_001.txt")],
                            "box_insertdate": [FV("2025-08-26T18:29:10", label="nested/file_001.txt")],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="fdf3c53c421fdf61ab77aa31dc31c9e3e63ef634d398557513ea55790dc9ecb9",
                        parent=EventParent(sha256="91e34fc6918dcaa1975b7cea8bf3ed874d52d51dc06f694ea1675dec44e6a076"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="fdf3c53c421fdf61ab77aa31dc31c9e3e63ef634d398557513ea55790dc9ecb9",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("nested/file_001.txt")]},
                    ),
                ],
                data={"fdf3c53c421fdf61ab77aa31dc31c9e3e63ef634d398557513ea55790dc9ecb9": b""},
            ),
        )

    def test_zip_extra_content_at_end(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "99a6346fd2e3256cd5d1775f9d3d725fc2e0abf6afe02f70c024309ae89088e3",
                    "Zip with trailing extra content",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="99a6346fd2e3256cd5d1775f9d3d725fc2e0abf6afe02f70c024309ae89088e3",
                        features={
                            "box_compression": [FV("Deflate", label="nested/file_001.txt")],
                            "box_count": [FV("1")],
                            "box_filepath": [FV("nested/file_001.txt")],
                            "box_insertdate": [FV("2025-08-26T18:29:10", label="nested/file_001.txt")],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="fdf3c53c421fdf61ab77aa31dc31c9e3e63ef634d398557513ea55790dc9ecb9",
                        parent=EventParent(sha256="99a6346fd2e3256cd5d1775f9d3d725fc2e0abf6afe02f70c024309ae89088e3"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="fdf3c53c421fdf61ab77aa31dc31c9e3e63ef634d398557513ea55790dc9ecb9",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("nested/file_001.txt")]},
                    ),
                ],
                data={"fdf3c53c421fdf61ab77aa31dc31c9e3e63ef634d398557513ea55790dc9ecb9": b""},
            ),
        )

    def test_iso(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "f303cdea6a123ce4501449936c7c809f855a2d32d3d17cc2630390df2f588d07", "Malicious ISO."
                ),
                format_override="archive/iso",
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="f303cdea6a123ce4501449936c7c809f855a2d32d3d17cc2630390df2f588d07",
                        features={
                            "box_count": [FV(1)],
                            "box_filepath": [FV("payment slip and bank confirmation document.exe")],
                            "box_insertdate": [
                                FV(
                                    datetime.datetime(2017, 5, 25, 1, 58, 51),
                                    label="payment slip and bank confirmation document.exe",
                                )
                            ],
                            "box_type": [FV("iso")],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="f303cdea6a123ce4501449936c7c809f855a2d32d3d17cc2630390df2f588d07",
                        ),
                        entity_type="binary",
                        entity_id="84b73d9bc64da09072ebba537418a35c4883daba40fa7b348080fa10b1dfeb41",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="84b73d9bc64da09072ebba537418a35c4883daba40fa7b348080fa10b1dfeb41",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("payment slip and bank confirmation document.exe")]},
                    ),
                ],
                data={"84b73d9bc64da09072ebba537418a35c4883daba40fa7b348080fa10b1dfeb41": b""},
            ),
        )

    def test_zipbomb_alt(self):
        """Attempt to unzip a known zip bomb sourced from https://github.com/iamtraction/ZOD/commits/master/"""
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "bd28d9adccd2ff2e3fa5bcc81d8f5fce654bd1d316e019959a5c68717c59f91b",
                    "Malicious Zip Bomb ZOD (Zip Of Death)",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="bd28d9adccd2ff2e3fa5bcc81d8f5fce654bd1d316e019959a5c68717c59f91b",
                        features={
                            "box_compression": [
                                FV("Store", label="42/42 (1).zip"),
                                FV("Store", label="42/42 (10).zip"),
                                FV("Store", label="42/42 (100).zip"),
                                FV("Store", label="42/42 (11).zip"),
                                FV("Store", label="42/42 (12).zip"),
                                FV("Store", label="42/42 (13).zip"),
                                FV("Store", label="42/42 (14).zip"),
                                FV("Store", label="42/42 (15).zip"),
                                FV("Store", label="42/42 (16).zip"),
                                FV("Store", label="42/42 (17).zip"),
                                FV("Store", label="42/42 (18).zip"),
                                FV("Store", label="42/42 (19).zip"),
                                FV("Store", label="42/42 (2).zip"),
                                FV("Store", label="42/42 (20).zip"),
                                FV("Store", label="42/42 (21).zip"),
                                FV("Store", label="42/42 (22).zip"),
                                FV("Store", label="42/42 (23).zip"),
                                FV("Store", label="42/42 (24).zip"),
                                FV("Store", label="42/42 (25).zip"),
                                FV("Store", label="42/42 (26).zip"),
                                FV("Store", label="42/42 (27).zip"),
                                FV("Store", label="42/42 (28).zip"),
                                FV("Store", label="42/42 (29).zip"),
                                FV("Store", label="42/42 (3).zip"),
                                FV("Store", label="42/42 (30).zip"),
                                FV("Store", label="42/42 (31).zip"),
                                FV("Store", label="42/42 (32).zip"),
                                FV("Store", label="42/42 (33).zip"),
                                FV("Store", label="42/42 (34).zip"),
                                FV("Store", label="42/42 (35).zip"),
                                FV("Store", label="42/42 (36).zip"),
                                FV("Store", label="42/42 (37).zip"),
                                FV("Store", label="42/42 (38).zip"),
                                FV("Store", label="42/42 (39).zip"),
                                FV("Store", label="42/42 (4).zip"),
                                FV("Store", label="42/42 (40).zip"),
                                FV("Store", label="42/42 (41).zip"),
                                FV("Store", label="42/42 (42).zip"),
                                FV("Store", label="42/42 (43).zip"),
                                FV("Store", label="42/42 (44).zip"),
                                FV("Store", label="42/42 (45).zip"),
                                FV("Store", label="42/42 (46).zip"),
                                FV("Store", label="42/42 (47).zip"),
                                FV("Store", label="42/42 (48).zip"),
                                FV("Store", label="42/42 (49).zip"),
                                FV("Store", label="42/42 (5).zip"),
                                FV("Store", label="42/42 (50).zip"),
                                FV("Store", label="42/42 (51).zip"),
                                FV("Store", label="42/42 (52).zip"),
                                FV("Store", label="42/42 (53).zip"),
                                FV("Store", label="42/42 (54).zip"),
                                FV("Store", label="42/42 (55).zip"),
                                FV("Store", label="42/42 (56).zip"),
                                FV("Store", label="42/42 (57).zip"),
                                FV("Store", label="42/42 (58).zip"),
                                FV("Store", label="42/42 (59).zip"),
                                FV("Store", label="42/42 (6).zip"),
                                FV("Store", label="42/42 (60).zip"),
                                FV("Store", label="42/42 (61).zip"),
                                FV("Store", label="42/42 (62).zip"),
                                FV("Store", label="42/42 (63).zip"),
                                FV("Store", label="42/42 (64).zip"),
                                FV("Store", label="42/42 (65).zip"),
                                FV("Store", label="42/42 (66).zip"),
                                FV("Store", label="42/42 (67).zip"),
                                FV("Store", label="42/42 (68).zip"),
                                FV("Store", label="42/42 (69).zip"),
                                FV("Store", label="42/42 (7).zip"),
                                FV("Store", label="42/42 (70).zip"),
                                FV("Store", label="42/42 (71).zip"),
                                FV("Store", label="42/42 (72).zip"),
                                FV("Store", label="42/42 (73).zip"),
                                FV("Store", label="42/42 (74).zip"),
                                FV("Store", label="42/42 (75).zip"),
                                FV("Store", label="42/42 (76).zip"),
                                FV("Store", label="42/42 (77).zip"),
                                FV("Store", label="42/42 (78).zip"),
                                FV("Store", label="42/42 (79).zip"),
                                FV("Store", label="42/42 (8).zip"),
                                FV("Store", label="42/42 (80).zip"),
                                FV("Store", label="42/42 (81).zip"),
                                FV("Store", label="42/42 (82).zip"),
                                FV("Store", label="42/42 (83).zip"),
                                FV("Store", label="42/42 (84).zip"),
                                FV("Store", label="42/42 (85).zip"),
                                FV("Store", label="42/42 (86).zip"),
                                FV("Store", label="42/42 (87).zip"),
                                FV("Store", label="42/42 (88).zip"),
                                FV("Store", label="42/42 (89).zip"),
                                FV("Store", label="42/42 (9).zip"),
                                FV("Store", label="42/42 (90).zip"),
                                FV("Store", label="42/42 (91).zip"),
                                FV("Store", label="42/42 (92).zip"),
                                FV("Store", label="42/42 (93).zip"),
                                FV("Store", label="42/42 (94).zip"),
                                FV("Store", label="42/42 (95).zip"),
                                FV("Store", label="42/42 (96).zip"),
                                FV("Store", label="42/42 (97).zip"),
                                FV("Store", label="42/42 (98).zip"),
                                FV("Store", label="42/42 (99).zip"),
                                FV("Store", label="42/42.zip"),
                            ],
                            "box_count": [FV("101")],
                            "box_filepath": [
                                FV("42/42 (1).zip"),
                                FV("42/42 (10).zip"),
                                FV("42/42 (100).zip"),
                                FV("42/42 (11).zip"),
                                FV("42/42 (12).zip"),
                                FV("42/42 (13).zip"),
                                FV("42/42 (14).zip"),
                                FV("42/42 (15).zip"),
                                FV("42/42 (16).zip"),
                                FV("42/42 (17).zip"),
                                FV("42/42 (18).zip"),
                                FV("42/42 (19).zip"),
                                FV("42/42 (2).zip"),
                                FV("42/42 (20).zip"),
                                FV("42/42 (21).zip"),
                                FV("42/42 (22).zip"),
                                FV("42/42 (23).zip"),
                                FV("42/42 (24).zip"),
                                FV("42/42 (25).zip"),
                                FV("42/42 (26).zip"),
                                FV("42/42 (27).zip"),
                                FV("42/42 (28).zip"),
                                FV("42/42 (29).zip"),
                                FV("42/42 (3).zip"),
                                FV("42/42 (30).zip"),
                                FV("42/42 (31).zip"),
                                FV("42/42 (32).zip"),
                                FV("42/42 (33).zip"),
                                FV("42/42 (34).zip"),
                                FV("42/42 (35).zip"),
                                FV("42/42 (36).zip"),
                                FV("42/42 (37).zip"),
                                FV("42/42 (38).zip"),
                                FV("42/42 (39).zip"),
                                FV("42/42 (4).zip"),
                                FV("42/42 (40).zip"),
                                FV("42/42 (41).zip"),
                                FV("42/42 (42).zip"),
                                FV("42/42 (43).zip"),
                                FV("42/42 (44).zip"),
                                FV("42/42 (45).zip"),
                                FV("42/42 (46).zip"),
                                FV("42/42 (47).zip"),
                                FV("42/42 (48).zip"),
                                FV("42/42 (49).zip"),
                                FV("42/42 (5).zip"),
                                FV("42/42 (50).zip"),
                                FV("42/42 (51).zip"),
                                FV("42/42 (52).zip"),
                                FV("42/42 (53).zip"),
                                FV("42/42 (54).zip"),
                                FV("42/42 (55).zip"),
                                FV("42/42 (56).zip"),
                                FV("42/42 (57).zip"),
                                FV("42/42 (58).zip"),
                                FV("42/42 (59).zip"),
                                FV("42/42 (6).zip"),
                                FV("42/42 (60).zip"),
                                FV("42/42 (61).zip"),
                                FV("42/42 (62).zip"),
                                FV("42/42 (63).zip"),
                                FV("42/42 (64).zip"),
                                FV("42/42 (65).zip"),
                                FV("42/42 (66).zip"),
                                FV("42/42 (67).zip"),
                                FV("42/42 (68).zip"),
                                FV("42/42 (69).zip"),
                                FV("42/42 (7).zip"),
                                FV("42/42 (70).zip"),
                                FV("42/42 (71).zip"),
                                FV("42/42 (72).zip"),
                                FV("42/42 (73).zip"),
                                FV("42/42 (74).zip"),
                                FV("42/42 (75).zip"),
                                FV("42/42 (76).zip"),
                                FV("42/42 (77).zip"),
                                FV("42/42 (78).zip"),
                                FV("42/42 (79).zip"),
                                FV("42/42 (8).zip"),
                                FV("42/42 (80).zip"),
                                FV("42/42 (81).zip"),
                                FV("42/42 (82).zip"),
                                FV("42/42 (83).zip"),
                                FV("42/42 (84).zip"),
                                FV("42/42 (85).zip"),
                                FV("42/42 (86).zip"),
                                FV("42/42 (87).zip"),
                                FV("42/42 (88).zip"),
                                FV("42/42 (89).zip"),
                                FV("42/42 (9).zip"),
                                FV("42/42 (90).zip"),
                                FV("42/42 (91).zip"),
                                FV("42/42 (92).zip"),
                                FV("42/42 (93).zip"),
                                FV("42/42 (94).zip"),
                                FV("42/42 (95).zip"),
                                FV("42/42 (96).zip"),
                                FV("42/42 (97).zip"),
                                FV("42/42 (98).zip"),
                                FV("42/42 (99).zip"),
                                FV("42/42.zip"),
                            ],
                            "box_insertdate": [
                                FV("2025-04-23T13:29:28", label="42/42 (1).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (10).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (100).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (11).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (12).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (13).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (14).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (15).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (16).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (17).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (18).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (19).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (2).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (20).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (21).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (22).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (23).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (24).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (25).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (26).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (27).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (28).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (29).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (3).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (30).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (31).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (32).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (33).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (34).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (35).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (36).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (37).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (38).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (39).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (4).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (40).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (41).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (42).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (43).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (44).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (45).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (46).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (47).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (48).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (49).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (5).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (50).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (51).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (52).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (53).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (54).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (55).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (56).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (57).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (58).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (59).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (6).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (60).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (61).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (62).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (63).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (64).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (65).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (66).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (67).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (68).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (69).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (7).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (70).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (71).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (72).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (73).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (74).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (75).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (76).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (77).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (78).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (79).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (8).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (80).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (81).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (82).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (83).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (84).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (85).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (86).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (87).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (88).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (89).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (9).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (90).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (91).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (92).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (93).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (94).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (95).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (96).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (97).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (98).zip"),
                                FV("2025-04-23T13:29:28", label="42/42 (99).zip"),
                                FV("2025-04-23T13:29:28", label="42/42.zip"),
                            ],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa",
                        parent=EventParent(sha256="bd28d9adccd2ff2e3fa5bcc81d8f5fce654bd1d316e019959a5c68717c59f91b"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa",
                                label="content",
                            )
                        ],
                        features={
                            "filename": [
                                FV("42/42 (1).zip"),
                                FV("42/42 (10).zip"),
                                FV("42/42 (100).zip"),
                                FV("42/42 (11).zip"),
                                FV("42/42 (12).zip"),
                                FV("42/42 (13).zip"),
                                FV("42/42 (14).zip"),
                                FV("42/42 (15).zip"),
                                FV("42/42 (16).zip"),
                                FV("42/42 (17).zip"),
                                FV("42/42 (18).zip"),
                                FV("42/42 (19).zip"),
                                FV("42/42 (2).zip"),
                                FV("42/42 (20).zip"),
                                FV("42/42 (21).zip"),
                                FV("42/42 (22).zip"),
                                FV("42/42 (23).zip"),
                                FV("42/42 (24).zip"),
                                FV("42/42 (25).zip"),
                                FV("42/42 (26).zip"),
                                FV("42/42 (27).zip"),
                                FV("42/42 (28).zip"),
                                FV("42/42 (29).zip"),
                                FV("42/42 (3).zip"),
                                FV("42/42 (30).zip"),
                                FV("42/42 (31).zip"),
                                FV("42/42 (32).zip"),
                                FV("42/42 (33).zip"),
                                FV("42/42 (34).zip"),
                                FV("42/42 (35).zip"),
                                FV("42/42 (36).zip"),
                                FV("42/42 (37).zip"),
                                FV("42/42 (38).zip"),
                                FV("42/42 (39).zip"),
                                FV("42/42 (4).zip"),
                                FV("42/42 (40).zip"),
                                FV("42/42 (41).zip"),
                                FV("42/42 (42).zip"),
                                FV("42/42 (43).zip"),
                                FV("42/42 (44).zip"),
                                FV("42/42 (45).zip"),
                                FV("42/42 (46).zip"),
                                FV("42/42 (47).zip"),
                                FV("42/42 (48).zip"),
                                FV("42/42 (49).zip"),
                                FV("42/42 (5).zip"),
                                FV("42/42 (50).zip"),
                                FV("42/42 (51).zip"),
                                FV("42/42 (52).zip"),
                                FV("42/42 (53).zip"),
                                FV("42/42 (54).zip"),
                                FV("42/42 (55).zip"),
                                FV("42/42 (56).zip"),
                                FV("42/42 (57).zip"),
                                FV("42/42 (58).zip"),
                                FV("42/42 (59).zip"),
                                FV("42/42 (6).zip"),
                                FV("42/42 (60).zip"),
                                FV("42/42 (61).zip"),
                                FV("42/42 (62).zip"),
                                FV("42/42 (63).zip"),
                                FV("42/42 (64).zip"),
                                FV("42/42 (65).zip"),
                                FV("42/42 (66).zip"),
                                FV("42/42 (67).zip"),
                                FV("42/42 (68).zip"),
                                FV("42/42 (69).zip"),
                                FV("42/42 (7).zip"),
                                FV("42/42 (70).zip"),
                                FV("42/42 (71).zip"),
                                FV("42/42 (72).zip"),
                                FV("42/42 (73).zip"),
                                FV("42/42 (74).zip"),
                                FV("42/42 (75).zip"),
                                FV("42/42 (76).zip"),
                                FV("42/42 (77).zip"),
                                FV("42/42 (78).zip"),
                                FV("42/42 (79).zip"),
                                FV("42/42 (8).zip"),
                                FV("42/42 (80).zip"),
                                FV("42/42 (81).zip"),
                                FV("42/42 (82).zip"),
                                FV("42/42 (83).zip"),
                                FV("42/42 (84).zip"),
                                FV("42/42 (85).zip"),
                                FV("42/42 (86).zip"),
                                FV("42/42 (87).zip"),
                                FV("42/42 (88).zip"),
                                FV("42/42 (89).zip"),
                                FV("42/42 (9).zip"),
                                FV("42/42 (90).zip"),
                                FV("42/42 (91).zip"),
                                FV("42/42 (92).zip"),
                                FV("42/42 (93).zip"),
                                FV("42/42 (94).zip"),
                                FV("42/42 (95).zip"),
                                FV("42/42 (96).zip"),
                                FV("42/42 (97).zip"),
                                FV("42/42 (98).zip"),
                                FV("42/42 (99).zip"),
                                FV("42/42.zip"),
                            ]
                        },
                    ),
                ],
                data={"bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa": b""},
            ),
        )

    def test_zipbomb(self):
        """Attempt to unzip a known zip bomb sourced from https://github.com/iamtraction/ZOD/commits/master/"""
        result = self.do_execution(
            entity_attrs={"file_format": self.unbox_type_key},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa",
                        "Known Zip Bomb ZOD (Zip Of Death)",
                    ),
                ),
            ],
            submission_settings={"passwords": "42\n43\n44"},
        )

        expected_result = JobResult(
            state=State(State.Label.COMPLETED),
            events=[
                Event(
                    sha256="bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa",
                    features={
                        "box_compression": [
                            FV("AES-256 Deflate", label="lib 0.zip"),
                            FV("AES-256 Deflate", label="lib 1.zip"),
                            FV("AES-256 Deflate", label="lib 2.zip"),
                            FV("AES-256 Deflate", label="lib 3.zip"),
                            FV("AES-256 Deflate", label="lib 4.zip"),
                            FV("AES-256 Deflate", label="lib 5.zip"),
                            FV("AES-256 Deflate", label="lib 6.zip"),
                            FV("AES-256 Deflate", label="lib 7.zip"),
                            FV("AES-256 Deflate", label="lib 8.zip"),
                            FV("AES-256 Deflate", label="lib 9.zip"),
                            FV("AES-256 Deflate", label="lib a.zip"),
                            FV("AES-256 Deflate", label="lib b.zip"),
                            FV("AES-256 Deflate", label="lib c.zip"),
                            FV("AES-256 Deflate", label="lib d.zip"),
                            FV("AES-256 Deflate", label="lib e.zip"),
                            FV("AES-256 Deflate", label="lib f.zip"),
                        ],
                        "box_count": [FV("16")],
                        "box_filepath": [
                            FV("lib 0.zip"),
                            FV("lib 1.zip"),
                            FV("lib 2.zip"),
                            FV("lib 3.zip"),
                            FV("lib 4.zip"),
                            FV("lib 5.zip"),
                            FV("lib 6.zip"),
                            FV("lib 7.zip"),
                            FV("lib 8.zip"),
                            FV("lib 9.zip"),
                            FV("lib a.zip"),
                            FV("lib b.zip"),
                            FV("lib c.zip"),
                            FV("lib d.zip"),
                            FV("lib e.zip"),
                            FV("lib f.zip"),
                        ],
                        "box_insertdate": [
                            FV("2000-03-28T20:40:54", label="lib 0.zip"),
                            FV("2000-03-28T20:40:54", label="lib 1.zip"),
                            FV("2000-03-28T20:40:54", label="lib 2.zip"),
                            FV("2000-03-28T20:40:54", label="lib 3.zip"),
                            FV("2000-03-28T20:40:54", label="lib 4.zip"),
                            FV("2000-03-28T20:40:54", label="lib 5.zip"),
                            FV("2000-03-28T20:40:54", label="lib 6.zip"),
                            FV("2000-03-28T20:40:54", label="lib 7.zip"),
                            FV("2000-03-28T20:40:54", label="lib 8.zip"),
                            FV("2000-03-28T20:40:54", label="lib 9.zip"),
                            FV("2000-03-28T20:40:54", label="lib a.zip"),
                            FV("2000-03-28T20:40:54", label="lib b.zip"),
                            FV("2000-03-28T20:40:54", label="lib c.zip"),
                            FV("2000-03-28T20:40:54", label="lib d.zip"),
                            FV("2000-03-28T20:40:54", label="lib e.zip"),
                            FV("2000-03-28T20:40:54", label="lib f.zip"),
                        ],
                        "box_password": [FV("42")],
                        "box_type": [FV("zip")],
                        "password": [FV("42")],
                    },
                ),
                Event(
                    sha256="9056b87f079861d1b0f041317d6415927d9ffb6498ce2530ff90fda69fa64e78",
                    parent=EventParent(sha256="bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa"),
                    relationship={"action": "extracted"},
                    data=[
                        EventData(
                            hash="9056b87f079861d1b0f041317d6415927d9ffb6498ce2530ff90fda69fa64e78",
                            label="content",
                        )
                    ],
                    features={
                        "filename": [
                            FV("lib 0.zip"),
                            FV("lib 1.zip"),
                            FV("lib 2.zip"),
                            FV("lib 3.zip"),
                            FV("lib 4.zip"),
                            FV("lib 5.zip"),
                            FV("lib 6.zip"),
                            FV("lib 7.zip"),
                            FV("lib 8.zip"),
                            FV("lib 9.zip"),
                            FV("lib a.zip"),
                            FV("lib b.zip"),
                            FV("lib c.zip"),
                            FV("lib d.zip"),
                            FV("lib e.zip"),
                            FV("lib f.zip"),
                        ]
                    },
                ),
            ],
            data={"9056b87f079861d1b0f041317d6415927d9ffb6498ce2530ff90fda69fa64e78": b""},
        )

        self.assertJobResult(result.get(self.unbox_result_key), expected_result)

        # Verify it still works when only one password is provided.
        result2 = self.do_execution(
            entity_attrs={"file_format": self.unbox_type_key},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "bbd05de19aa2af1455c0494639215898a15286d9b05073b6c4817fe24b2c36fa",
                        "Known Zip Bomb ZOD (Zip Of Death)",
                    ),
                ),
            ],
            submission_settings={"passwords": "42"},
        )
        self.assertJobResult(result2.get(self.unbox_result_key), expected_result)

    def test_zipbomb_multilayered(self):
        """Attempt to unzip a known zip bomb sourced from https://github.com/uint128-t/ZIPBOMB/tree/main"""
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "dbbfc2e4ff312cc2a699fb34a980e9efebd9bb8b768a221e6582953315211436", "Malicious Zip Bomb."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="dbbfc2e4ff312cc2a699fb34a980e9efebd9bb8b768a221e6582953315211436",
                        features={
                            "box_compression": [FV("Deflate", label="32-256.zip")],
                            "box_count": [FV("1")],
                            "box_filepath": [FV("32-256.zip")],
                            "box_insertdate": [FV("2024-07-17T14:10:45.596326", label="32-256.zip")],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="49fcb86e94034485f8507b359de220650d3f0933ce8902eacbb427ae9a93a833",
                        parent=EventParent(sha256="dbbfc2e4ff312cc2a699fb34a980e9efebd9bb8b768a221e6582953315211436"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="49fcb86e94034485f8507b359de220650d3f0933ce8902eacbb427ae9a93a833",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("32-256.zip")]},
                    ),
                ],
                data={"49fcb86e94034485f8507b359de220650d3f0933ce8902eacbb427ae9a93a833": b""},
            ),
        )

    def test_zipbomb_multilayered_bigger(self):
        """Attempt to unzip a known zip bomb sourced from https://github.com/uint128-t/ZIPBOMB/tree/main"""
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "21a6f6a45ee9ed386e8a441699cfd482ee1ea1c04b5d54e9c764bd5b9f48715d", "Malicious ZIP file."
                )
            ),
            JobResult(state=State(State.Label.ERROR_EXCEPTION, message="7zip decode error: Headers Error")),
        )

    def test_zipbomb_zod_xl(self):
        """Attempt to unzip a known zip bomb sourced from https://github.com/iamtraction/ZOD/commits/master/"""
        result = self.do_execution(
            entity_attrs={"file_format": self.unbox_type_key},
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "ad8c29cc54d5b0ca727c95266c2160e9068792b6b416cccf095739dddc2556c7",
                        "Known zip bomb ZOD (zip of death).",
                    ),
                ),
                ("password_dictionary", b"zipbomb190\nzipbomb35\n65500\nzod_165\n362\n7zb\n7zb"),
            ],
        )
        self.assertJobResult(
            result.get(self.unbox_result_key),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="ad8c29cc54d5b0ca727c95266c2160e9068792b6b416cccf095739dddc2556c7",
                        features={
                            "box_compression": [
                                FV("ZipCrypto LZMA:eos", label="Root 0.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 1.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 2.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 3.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 4.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 5.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 6.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 7.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 8.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root 9.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root a.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root b.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root c.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root d.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root e.zip"),
                                FV("ZipCrypto LZMA:eos", label="Root f.zip"),
                            ],
                            "box_count": [FV("16")],
                            "box_filepath": [
                                FV("Root 0.zip"),
                                FV("Root 1.zip"),
                                FV("Root 2.zip"),
                                FV("Root 3.zip"),
                                FV("Root 4.zip"),
                                FV("Root 5.zip"),
                                FV("Root 6.zip"),
                                FV("Root 7.zip"),
                                FV("Root 8.zip"),
                                FV("Root 9.zip"),
                                FV("Root a.zip"),
                                FV("Root b.zip"),
                                FV("Root c.zip"),
                                FV("Root d.zip"),
                                FV("Root e.zip"),
                                FV("Root f.zip"),
                            ],
                            "box_insertdate": [
                                FV("2023-11-22T12:23:32.248568", label="Root 0.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 1.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 2.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 3.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 4.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 5.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 6.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 7.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 8.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root 9.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root a.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root b.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root c.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root d.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root e.zip"),
                                FV("2023-11-22T12:23:32.248568", label="Root f.zip"),
                            ],
                            "box_password": [FV("65500")],
                            "box_type": [FV("zip")],
                            "password": [FV("65500")],
                        },
                    ),
                    Event(
                        sha256="8c1f17bf0a9dbac5ffe8cd3f1a90d6b9461870182b20dccb2db42bc25795f3dd",
                        parent=EventParent(sha256="ad8c29cc54d5b0ca727c95266c2160e9068792b6b416cccf095739dddc2556c7"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="8c1f17bf0a9dbac5ffe8cd3f1a90d6b9461870182b20dccb2db42bc25795f3dd",
                                label="content",
                            )
                        ],
                        features={
                            "filename": [
                                FV("Root 0.zip"),
                                FV("Root 1.zip"),
                                FV("Root 2.zip"),
                                FV("Root 3.zip"),
                                FV("Root 4.zip"),
                                FV("Root 5.zip"),
                                FV("Root 6.zip"),
                                FV("Root 7.zip"),
                                FV("Root 8.zip"),
                                FV("Root 9.zip"),
                                FV("Root a.zip"),
                                FV("Root b.zip"),
                                FV("Root c.zip"),
                                FV("Root d.zip"),
                                FV("Root e.zip"),
                                FV("Root f.zip"),
                            ]
                        },
                    ),
                ],
                data={"8c1f17bf0a9dbac5ffe8cd3f1a90d6b9461870182b20dccb2db42bc25795f3dd": b""},
            ),
        )

    def test_zip_widening_children(self):
        """Attempt to unzip a zip that has 10 children at each level and keeps expanding out."""
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546",
                    "Custom made Zip that has 10 children at each level expanding like a tree, designed to hurt Azul UI relationship graph.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546",
                        features={
                            "box_compression": [
                                FV("Deflate", label="1.zip"),
                                FV("Deflate", label="124445.zip"),
                                FV("Deflate", label="155556.zip"),
                                FV("Deflate", label="186667.zip"),
                                FV("Deflate", label="217778.zip"),
                                FV("Deflate", label="248889.zip"),
                                FV("Deflate", label="280000.zip"),
                                FV("Deflate", label="31112.zip"),
                                FV("Deflate", label="62223.zip"),
                                FV("Deflate", label="93334.zip"),
                            ],
                            "box_count": [FV("10")],
                            "box_filepath": [
                                FV("1.zip"),
                                FV("124445.zip"),
                                FV("155556.zip"),
                                FV("186667.zip"),
                                FV("217778.zip"),
                                FV("248889.zip"),
                                FV("280000.zip"),
                                FV("31112.zip"),
                                FV("62223.zip"),
                                FV("93334.zip"),
                            ],
                            "box_insertdate": [
                                FV("1980-01-01T00:00:00", label="1.zip"),
                                FV("1980-01-01T00:00:00", label="124445.zip"),
                                FV("1980-01-01T00:00:00", label="155556.zip"),
                                FV("1980-01-01T00:00:00", label="186667.zip"),
                                FV("1980-01-01T00:00:00", label="217778.zip"),
                                FV("1980-01-01T00:00:00", label="248889.zip"),
                                FV("1980-01-01T00:00:00", label="280000.zip"),
                                FV("1980-01-01T00:00:00", label="31112.zip"),
                                FV("1980-01-01T00:00:00", label="62223.zip"),
                                FV("1980-01-01T00:00:00", label="93334.zip"),
                            ],
                            "box_type": [FV("zip")],
                        },
                    ),
                    Event(
                        sha256="9facf52dd9915a32c58dcf558cac4220fe9cd3c23740ab8562082c0d22e8fd0d",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="9facf52dd9915a32c58dcf558cac4220fe9cd3c23740ab8562082c0d22e8fd0d",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("1.zip")]},
                    ),
                    Event(
                        sha256="a89ae8250a669803cdab11409081a375f55fd91bbcedd40a4a7451a9e029f22c",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="a89ae8250a669803cdab11409081a375f55fd91bbcedd40a4a7451a9e029f22c",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("124445.zip")]},
                    ),
                    Event(
                        sha256="aba6fe6405a9f48938ec82ead3361af9b61336391ae6a1448d6679c8cc3e24d7",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="aba6fe6405a9f48938ec82ead3361af9b61336391ae6a1448d6679c8cc3e24d7",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("155556.zip")]},
                    ),
                    Event(
                        sha256="70a151ce625d1bd5b1df3911402e1283fa27164deffd04c5451d02dcdee73c4b",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="70a151ce625d1bd5b1df3911402e1283fa27164deffd04c5451d02dcdee73c4b",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("186667.zip")]},
                    ),
                    Event(
                        sha256="023d86d75ce81e54418b811ce82922d4e710b85adc0eb8404996a65ea2166b64",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="023d86d75ce81e54418b811ce82922d4e710b85adc0eb8404996a65ea2166b64",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("217778.zip")]},
                    ),
                    Event(
                        sha256="dce34836cef28371c70f223c3068340f61cb739f7f3fe35e125b8f3d4733ebb0",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="dce34836cef28371c70f223c3068340f61cb739f7f3fe35e125b8f3d4733ebb0",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("248889.zip")]},
                    ),
                    Event(
                        sha256="605639c20780ce7f54ee0657604e1e517c9ff67ba5371ba2e3fea6d4bf6afb7b",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="605639c20780ce7f54ee0657604e1e517c9ff67ba5371ba2e3fea6d4bf6afb7b",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("280000.zip")]},
                    ),
                    Event(
                        sha256="3de425aa3f20914fc7e8bb154426b23ced4e5a98b02c141d80edd768d4b45f73",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="3de425aa3f20914fc7e8bb154426b23ced4e5a98b02c141d80edd768d4b45f73",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("31112.zip")]},
                    ),
                    Event(
                        sha256="d2e5dfa16786a8fd96e28aa53d88e9b6e00d8721e05247b1be185c7f57878b0a",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="d2e5dfa16786a8fd96e28aa53d88e9b6e00d8721e05247b1be185c7f57878b0a",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("62223.zip")]},
                    ),
                    Event(
                        sha256="ec7da54f315af4656558ab22ffa0b25b5dfa5f255a9b6ae629353392a3cd7686",
                        parent=EventParent(sha256="2b9ba8d4bd499872f990d29e960580c82b4718764aad61b8b9ca91f84a255546"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="ec7da54f315af4656558ab22ffa0b25b5dfa5f255a9b6ae629353392a3cd7686",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("93334.zip")]},
                    ),
                ],
                data={
                    "9facf52dd9915a32c58dcf558cac4220fe9cd3c23740ab8562082c0d22e8fd0d": b"",
                    "a89ae8250a669803cdab11409081a375f55fd91bbcedd40a4a7451a9e029f22c": b"",
                    "aba6fe6405a9f48938ec82ead3361af9b61336391ae6a1448d6679c8cc3e24d7": b"",
                    "70a151ce625d1bd5b1df3911402e1283fa27164deffd04c5451d02dcdee73c4b": b"",
                    "023d86d75ce81e54418b811ce82922d4e710b85adc0eb8404996a65ea2166b64": b"",
                    "dce34836cef28371c70f223c3068340f61cb739f7f3fe35e125b8f3d4733ebb0": b"",
                    "605639c20780ce7f54ee0657604e1e517c9ff67ba5371ba2e3fea6d4bf6afb7b": b"",
                    "3de425aa3f20914fc7e8bb154426b23ced4e5a98b02c141d80edd768d4b45f73": b"",
                    "d2e5dfa16786a8fd96e28aa53d88e9b6e00d8721e05247b1be185c7f57878b0a": b"",
                    "ec7da54f315af4656558ab22ffa0b25b5dfa5f255a9b6ae629353392a3cd7686": b"",
                },
            ),
        )
