"""PDF plugin test suite."""

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest


class TestExecute(BaseUnboxPluginTest):
    unbox_result_key = "pdf"
    unbox_type_key = "document/pdf"

    def test_pdf_unencrypted(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "fb5757c13b6be5ddfcc5df34110bd742ec39d572fc12090af877b842e6569026",
                    "Benign PDF appended with additional data.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="fb5757c13b6be5ddfcc5df34110bd742ec39d572fc12090af877b842e6569026",
                        features={
                            "box_count": [FV(4)],
                            "box_type": [FV("pdf")],
                            "pdf_object_dictionary": [
                                FV(
                                    "<< /BBox [ -112 420 708 420.1 ] /Filter /FlateDecode /Group << /CS /DeviceRGB /K true /S /Transparency >> /Length 8 /Subtype /Form /Type /XObject >>",
                                    label="4/0",
                                ),
                                FV("<< /Filter /FlateDecode /Length 3 0 R >>", label="2/0"),
                                FV("<< /Filter /FlateDecode /Length 319 >>", label="11/0"),
                                FV("<< /Filter /FlateDecode /Length 9 0 R /Length1 12652 >>", label="8/0"),
                            ],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fb5757c13b6be5ddfcc5df34110bd742ec39d572fc12090af877b842e6569026",
                        ),
                        entity_type="binary",
                        entity_id="310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0",
                        relationship={"action": "extracted", "object_id": "11/0", "filter": "FlateDecode"},
                        data=[
                            EventData(
                                hash="310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0",
                                label="content",
                            )
                        ],
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fb5757c13b6be5ddfcc5df34110bd742ec39d572fc12090af877b842e6569026",
                        ),
                        entity_type="binary",
                        entity_id="0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb",
                        relationship={"action": "extracted", "object_id": "2/0", "filter": "FlateDecode"},
                        data=[
                            EventData(
                                hash="0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb",
                                label="content",
                            )
                        ],
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="fb5757c13b6be5ddfcc5df34110bd742ec39d572fc12090af877b842e6569026",
                        ),
                        entity_type="binary",
                        entity_id="1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617",
                        relationship={"action": "extracted", "object_id": "8/0", "filter": "FlateDecode"},
                        data=[
                            EventData(
                                hash="1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617",
                                label="content",
                            )
                        ],
                    ),
                ],
                data={
                    "310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0": b"",
                    "0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb": b"",
                    "1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617": b"",
                },
            ),
        )

    def test_pdf_encrypted(self):
        self.assertJobResult(
            self.get_result_from_cart(
                self.load_test_file_bytes(
                    "36abae6e31d591ab08a99c7b30bcb8dc3f208fa625f189c594eaf4caee1de394",
                    "Benign PDF test file encrypted with user password RC4.",
                )
            ),
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="36abae6e31d591ab08a99c7b30bcb8dc3f208fa625f189c594eaf4caee1de394",
                        features={
                            "box_count": [FV(5)],
                            "box_password": [FV("password")],
                            "box_type": [FV("pdf")],
                            "password": [FV("password")],
                            "pdf_object_dictionary": [
                                FV(
                                    "<< /BBox [ -112 420 708 420.1 ] /Filter /FlateDecode /Group << /CS /DeviceRGB /K true /S /Transparency >> /Length 8 /Subtype /Form /Type /XObject >>",
                                    label="10/0",
                                ),
                                FV("<< /Filter /FlateDecode /Length 236 >>", label="6/0"),
                                FV("<< /Filter /FlateDecode /Length 319 >>", label="13/0"),
                                FV("<< /Filter /FlateDecode /Length 8210 /Length1 12652 >>", label="14/0"),
                            ],
                        },
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="36abae6e31d591ab08a99c7b30bcb8dc3f208fa625f189c594eaf4caee1de394",
                        ),
                        entity_type="binary",
                        entity_id="310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0",
                        relationship={"action": "extracted", "object_id": "13/0", "filter": "FlateDecode"},
                        data=[
                            EventData(
                                hash="310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0",
                                label="content",
                            )
                        ],
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="36abae6e31d591ab08a99c7b30bcb8dc3f208fa625f189c594eaf4caee1de394",
                        ),
                        entity_type="binary",
                        entity_id="1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617",
                        relationship={"action": "extracted", "object_id": "14/0", "filter": "FlateDecode"},
                        data=[
                            EventData(
                                hash="1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617",
                                label="content",
                            )
                        ],
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="36abae6e31d591ab08a99c7b30bcb8dc3f208fa625f189c594eaf4caee1de394",
                        ),
                        entity_type="binary",
                        entity_id="0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb",
                        relationship={"action": "extracted", "object_id": "6/0", "filter": "FlateDecode"},
                        data=[
                            EventData(
                                hash="0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb",
                                label="content",
                            )
                        ],
                    ),
                    Event(
                        parent=EventParent(
                            entity_type="binary",
                            entity_id="36abae6e31d591ab08a99c7b30bcb8dc3f208fa625f189c594eaf4caee1de394",
                        ),
                        entity_type="binary",
                        entity_id="e6b611d975aae6bbee8e87751f94eafb009ca3ac102f549e3249a96a3f91dec3",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="e6b611d975aae6bbee8e87751f94eafb009ca3ac102f549e3249a96a3f91dec3",
                                label="content",
                            )
                        ],
                    ),
                ],
                data={
                    "310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0": b"",
                    "1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617": b"",
                    "0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb": b"",
                    "e6b611d975aae6bbee8e87751f94eafb009ca3ac102f549e3249a96a3f91dec3": b"",
                },
            ),
        )

    def test_not_pdf(self):
        self.complete_error_and_optout_test(
            self.load_test_file_bytes(
                "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                "Benign WIN32 EXE, python library executable python_mcp.exe",
            ),
            "file is not a PDF",
        )
