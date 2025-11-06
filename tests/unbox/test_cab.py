# coding=utf-8
from azul_plugin_unbox.unbox.box import box_cab
from azul_plugin_unbox.unbox.box_base import NotSupported
from tests.unbox.base_test import BaseFileTest


class CabTest(BaseFileTest):
    def test_cab(self):
        """extracting a normal cab file"""
        src_path = self.copy_test_file_to_src_dir("normal.cab")
        box = box_cab.Cab(src_path, self.dest_dir)
        children = box.get_children()

        self.assertCountEqual(self.get_child_names(children), self.all_files)
        self.assertEqual(self.f1_contents, self.get_f1(children))
        self.assertEqual(self.f2_contents, self.get_f2(children))

    def test_txt(self):
        """extracting a .txt file. Should fail"""
        fpath = self.copy_test_file_to_src_dir(self.tfile1, local_path="data/base")
        box = box_cab.Cab(fpath, self.dest_dir)
        self.assertRaises(NotSupported, box.extract)

    def test_zip(self):
        """unzipping a normal Zip file. Should fail"""
        fpath = self.copy_test_file_to_src_dir("normal.zip")
        box = box_cab.Cab(fpath, self.dest_dir)
        self.assertRaises(NotSupported, box.extract)
