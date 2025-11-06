import os
import shutil

from azul_plugin_unbox.unbox.box import box_chm
from tests.unbox.base_test import BaseFileTest

# CHM project filenames
chm_filename = "Project.chm"
hhp_filename = "Project.hhp"
hhc_filename = "Project.hhc"
hhk_filename = "Project.hhk"
unlinked_page_fname = "Page.htm"
main_page_fname = "Main.htm"
content_dir = "Content"


class TestCHM(BaseFileTest):
    def setUp(self):
        super().setUp()
        # Benign CHM encoded directory.
        raw_bytes = self.file_manager.download_file_bytes(
            "2aa154928a63851b1f82a21bc49d5668823e629219aeecc08d0cadefa09e117d"
        )
        self.base_dir_zip = os.path.join(self.src_dir, "chm.zip")
        with open(self.base_dir_zip, "wb") as f:
            f.write(raw_bytes)

        self.base_dir = self.base_dir_zip.removesuffix(".zip")
        shutil.unpack_archive(self.base_dir_zip, self.base_dir)

    def test_chm(self):
        """unbox a normal CHM file"""
        filepath = os.path.join(self.base_dir, chm_filename)
        box = box_chm.CHM(filepath, self.dest_dir)
        children = box.get_children()

        expected_keys = [
            "/%s" % hhc_filename,
            "/%s" % hhk_filename,
            "/%s/%s" % (content_dir, unlinked_page_fname),
            "/%s/%s" % (content_dir, main_page_fname),
            "/_#_README_#_",
        ]

        self.assertCountEqual(BaseFileTest.get_child_names(children), expected_keys)
        child_name = f"/{content_dir}/{main_page_fname}"
        content = BaseFileTest.read_file_from_children(children, child_name)
        expected = os.path.join(self.base_dir, "Content", main_page_fname)
        with open(expected, "r") as f:
            main_page = f.read()
        self.assertEqual(main_page, content.decode("utf-8"))

    def test_chm_full_list(self):
        """unbox a CHM file and don't ignore metadata keys"""
        filepath = os.path.join(self.base_dir, chm_filename)
        # filepath = os.path.join(base_dir, chm_filename)
        box = box_chm.CHM(filepath, self.dest_dir, ignore_builtins=False)

        children = box.get_children()
        expected_keys = [
            "/%s" % hhc_filename,
            "/%s" % hhk_filename,
            "/%s/%s" % (content_dir, unlinked_page_fname),
            "/%s/%s" % (content_dir, main_page_fname),
            "/_#_README_#_",
            "/#WINDOWS",
            "/#TOPICS",
            "/$FIftiMain",
            "/#URLSTR",
            "/#SYSTEM",
            "/#URLTBL",
            "/#STRINGS",
            "/$OBJINST",
            "/#ITBITS",
            "/#IDXHDR",
            "/$WWKeywordLinks/Property",
            "/$WWKeywordLinks/Map",
            "/$WWKeywordLinks/Data",
            "/$WWKeywordLinks/BTree",
            "/$WWAssociativeLinks/Property",
        ]
        self.assertCountEqual(BaseFileTest.get_child_names(children), expected_keys)
