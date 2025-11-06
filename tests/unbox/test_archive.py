# coding=utf-8
import os
import sys

from azul_plugin_unbox.unbox.box import box_archive
from tests.unbox.base_test import BaseFileTest


class TestArchive(BaseFileTest):
    """Test the box_archive module."""

    def test_tar(self):
        """Unzipping a normal tar file."""
        fpath = self.copy_test_file_to_src_dir("normal.tar")
        box = box_archive.Archive(fpath, self.dest_dir)

        children = box.get_children()
        self.assertCountEqual(self.get_child_names(children), self.all_files_and_folders)
        self.assertEqual(self.f1_contents, self.get_f1(children))

    def test_tar_metadata(self):
        """Unzipping and examining the metadata for a tar file."""
        fpath = self.copy_test_file_to_src_dir("normal.tar")
        box = box_archive.Archive(fpath, self.dest_dir)

        self.check_metadata_list_correct(box, ["encoding"], [])
        enc = box.get_meta()
        self.assertEqual(enc.get("encoding"), sys.getfilesystemencoding())

    def test_gzip_tarball(self):
        """Check tarball compressed with gzip works as expected."""
        fpath = self.copy_test_file_to_src_dir("normal.tar.gz")
        box = box_archive.Archive(fpath, self.dest_dir)

        children = box.get_children()
        self.assertCountEqual(self.all_files_and_folders, self.get_child_names(children))
        self.assertEqual(self.f1_contents, self.get_f1(children))

    def test_bzip2_tarball(self):
        """Check tarball compressed with bz2 works as expected."""
        fpath = self.copy_test_file_to_src_dir("normal.tar.bz2")
        box = box_archive.Archive(fpath, self.dest_dir)

        children = box.get_children()
        self.assertCountEqual(self.all_files_and_folders, self.get_child_names(children))
        self.assertEqual(self.f1_contents, self.get_f1(children))

    def test_gzip(self):
        """Check can handle straight gzip compressed file."""
        gzname = "gzipped.gz"
        fpath = self.copy_test_file_to_src_dir(gzname)
        box = box_archive.Archive(fpath, self.dest_dir)
        child = box.get_children()
        self.assertEqual(child[0].name, gzname[: -len(".gz")])
        self.assertEqual(self.f1_contents, self.read_file(child[0]))

    def test_gzip_alternate(self):
        """Check can handle straight gzip compressed file."""
        # Benign GZIP file
        fpath = self.file_manager.download_file_path(
            "94e87762edef627ce4b54556d27db9a4e9cdf5357afdc5efd94b63de077f1c21"
        )
        box = box_archive.Archive(fpath, self.dest_dir)
        child = box.get_children()
        self.assertEqual(child[0].name, "94e87762edef627ce4b54556d27db9a4e9cdf5357afdc5efd94b63de077f1c21")
        self.assertEqual(
            rb'<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M18 13v6h-1v-6h1zm-7-8v14h1V5h-1zM5 9v10h1V9H5z"/></svg>',
            self.read_file(child[0]),
        )

    def test_bzip2(self):
        """Check can handle straight bzip2 compressed file."""
        bzname = "bzipped.bz2"
        fpath = self.copy_test_file_to_src_dir(bzname)

        box = box_archive.Archive(fpath, self.dest_dir)
        child = box.get_children()

        self.assertEqual(child[0].name, bzname[: -len(".bz2")])
        self.assertEqual(self.f1_contents, self.read_file(child[0]))
