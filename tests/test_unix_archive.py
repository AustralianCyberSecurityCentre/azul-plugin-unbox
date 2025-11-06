"""
Unix archive plugin test suite
"""

import os
import pathlib
import shutil
import tempfile

from azul_runner import FV, Event, EventData, EventParent, JobResult, State

from tests.base_test import BaseUnboxPluginTest

# test file names
tfile1 = "test.txt"
tfile2 = "Uńįĉødệ.txt"
tdir1 = "adir"
tdir2 = "bdir"
f1_contents = b"Nothing to see here... move along"
f2_contents = "why, hello… have some ᴡᴓʀďŝ".encode("utf-8")

""" Expected folder structure of tar:
test.txt
adir
adir - Uńįĉødệ.txt
adir - bdir
"""


class TestUnixArchive(BaseUnboxPluginTest):
    unbox_result_key = "archive"
    unbox_type_key = "archive/tar"

    def setUp(self):
        """Create some test files to archive later. These files should be
        removed in the teardown"""
        super().setUp()
        self.base_dir = tempfile.mkdtemp(prefix="unbox")

    def tearDown(self):
        """remove the test files created during setup"""
        super().tearDown()
        shutil.rmtree(self.base_dir, ignore_errors=True)

    def _get_tar_file_contents(self, compression: str | None = None) -> bytes:
        """Get a tar file based on compression type."""
        tarname = "normal.tar"
        if compression in ("gzip", "gz"):
            tarname += ".gz"
        elif compression in ("bzip2", "bz2"):
            tarname += ".bz2"

        folder = os.path.split(self._get_location())[0]
        return self.load_local_raw(
            os.path.join(folder, "unbox/data/base_archives", tarname), description="Tarfile from the local samples."
        )

    def test_invalid_file(self):
        """not a valid file type"""
        # Test should fail when input content is not the correct type
        self.complete_error_and_optout_test(
            self.load_test_file_bytes(
                "702e31ed1537c279459a255460f12f0f2863f973e121cd9194957f4f3e7b0994",
                "Benign WIN32 EXE, python library executable python_mcp.exe",
            )
        )

    def test_invalid_office(self):
        self.complete_error_and_optout_test(
            self.load_test_file_bytes(
                "6b8e5e0d8f20add0c19980c35b373e58412248629db320afd20c026a40a67df9", "Benign Open Office Document."
            ),
            "Unable to process as tar, gz or bz2",
            opt_out_type_override="DOC",
        )

    def _assert_common_results(self, result: JobResult):
        """asserts the output results that should be common between tar, bz2, and gz test files"""
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="custom_id",
                        features={
                            "archive_encoding": [FV("utf-8")],
                            "box_count": [FV("4")],
                            "box_filepath": [FV("adir/"), FV("adir/bdir/"), FV("adir/Ṹnɨɔŏƌɇ.txt"), FV("test.txt")],
                            "box_type": [FV("archive")],
                        },
                    ),
                    Event(
                        sha256="735ef959e0dc4072c973eaf790b2ee6c4d3cdc7aee8f1b06bf3003e49e44e818",
                        parent=EventParent(sha256="custom_id"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="735ef959e0dc4072c973eaf790b2ee6c4d3cdc7aee8f1b06bf3003e49e44e818",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("adir/Ṹnɨɔŏƌɇ.txt")]},
                    ),
                    Event(
                        sha256="81cb6a246cb0c5e2e403f3f8bf2f845a4b83591820420c3aef3b88b94cca5bf9",
                        parent=EventParent(sha256="custom_id"),
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="81cb6a246cb0c5e2e403f3f8bf2f845a4b83591820420c3aef3b88b94cca5bf9",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("test.txt")]},
                    ),
                ],
                data={
                    "735ef959e0dc4072c973eaf790b2ee6c4d3cdc7aee8f1b06bf3003e49e44e818": b"",
                    "81cb6a246cb0c5e2e403f3f8bf2f845a4b83591820420c3aef3b88b94cca5bf9": b"",
                },
            ),
        )

    def test_tar_file(self):
        """test uncompressed tar file"""
        result = self.do_execution(
            entity_attrs={"file_format": "archive/tar"},
            ent_id="custom_id",
            data_in=[("content", self._get_tar_file_contents())],
        ).get(self.unbox_result_key)
        self._assert_common_results(result)

    def test_tar_gz_file(self):
        """test gzip compressed tar file"""
        result = self.do_execution(
            entity_attrs={"file_format": "archive/gzip"},
            ent_id="custom_id",
            data_in=[("content", self._get_tar_file_contents(compression="gzip"))],
        ).get(self.unbox_result_key)
        self._assert_common_results(result)

    def test_tar_bz2_file(self):
        """test bzip2 compressed tar file"""
        result = self.do_execution(
            entity_attrs={"file_format": "archive/bzip2"},
            ent_id="custom_id",
            data_in=[("content", self._get_tar_file_contents(compression="bzip2"))],
        ).get(self.unbox_result_key)
        self._assert_common_results(result)

    def test_gzip_with_extra_content(self):
        """Test a gzip that has extra content inside of the compressed."""
        result: JobResult = self.do_execution(
            entity_attrs={"file_format": "archive/gzip"},
            ent_id="custom_id",
            data_in=[
                (
                    "content",
                    self.load_test_file_bytes(
                        "94e87762edef627ce4b54556d27db9a4e9cdf5357afdc5efd94b63de077f1c21", "Benign GZIP file."
                    ),
                )
            ],
        ).get(self.unbox_result_key)

        # Set the box_filepath to no-name because the extracted file doesn't have a name and will be the name of the temp file.
        result.events[0].features["box_filepath"] = [FV("no-name")]
        result.events[1].features["filename"] = [FV("no-name")]

        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="custom_id",
                        features={
                            "box_count": [FV(1)],
                            "box_filepath": [FV("no-name")],
                            "box_type": [FV("archive")],
                            "extra_content": [FV("true")],
                        },
                    ),
                    Event(
                        parent=EventParent(entity_type="binary", entity_id="custom_id"),
                        entity_type="binary",
                        entity_id="28e65c268dbcab8733e7205bab86efc9a758a0d8f2156edc85d5f810b66007ab",
                        relationship={"action": "extracted"},
                        data=[
                            EventData(
                                hash="28e65c268dbcab8733e7205bab86efc9a758a0d8f2156edc85d5f810b66007ab",
                                label="content",
                            )
                        ],
                        features={"filename": [FV("no-name")]},
                    ),
                ],
                data={"28e65c268dbcab8733e7205bab86efc9a758a0d8f2156edc85d5f810b66007ab": b""},
            ),
        )
