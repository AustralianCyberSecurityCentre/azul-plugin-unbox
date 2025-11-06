"""
UPX plugin test suite
"""

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "upx"
    unbox_type_key = "executable/linux/elf64"

    def test_upx_elf(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "fe2b1e98bd082960d2e7aad58743d204c0112fadd9f0a36220f3540e4976df41", "UPX obfuscated file."
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="fe2b1e98bd082960d2e7aad58743d204c0112fadd9f0a36220f3540e4976df41",
                        features={"box_count": [FV("1")], "box_type": [FV("upx")], "upx_version": [FV("4.24")]},
                    ),
                    Event(
                        sha256="8deb23390c1c3614ff5324d191ff630f1684e0175cd5c26c684cf52b085c6dee",
                        parent=EventParent(sha256="fe2b1e98bd082960d2e7aad58743d204c0112fadd9f0a36220f3540e4976df41"),
                        relationship={"action": "unpacked"},
                        data=[
                            EventData(
                                hash="8deb23390c1c3614ff5324d191ff630f1684e0175cd5c26c684cf52b085c6dee",
                                label="content",
                            )
                        ],
                    ),
                ],
                data={"8deb23390c1c3614ff5324d191ff630f1684e0175cd5c26c684cf52b085c6dee": b""},
            ),
        )

    def test_not_upx(self):
        self.complete_double_optout_test(
            self.load_test_file_bytes(
                "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                "Benign WIN32 EXE, python library executable python_mcp.exe",
            ),
            opt_out_type_override="EXE",
        )

    def test_very_small_pe_file(self):
        self.assertJobResult(
            self.get_result_from_cart(
                b"abcdefghimnopqrst",
                ent_id_override="not_a_test_entity_to_allow_type_override",
            ),
            JobResult(state=State(State.Label.OPT_OUT, failure_name="not_upx", message="too small to be a UPX file")),
        )
