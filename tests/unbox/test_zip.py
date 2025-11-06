# coding=utf-8
from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box import box_zip
from tests.unbox.base_test import BaseFileTest


class TestZip(BaseFileTest):
    def test_unzip(self):
        """unzipping a normal Zip file"""
        fpath = self.copy_test_file_to_src_dir("normal.zip")

        box = box_zip.Zip(fpath, self.dest_dir)

        children = box.get_children()
        child_names = self.get_child_names(children)
        self.assertCountEqual(child_names, self.all_files_and_folders)

        self.assertEqual(self.f1_contents, self.get_f1(children))

    def test_unzip_password(self):
        """unzipping a passworded Zip file"""
        fpath = self.copy_test_file_to_src_dir("password.zip")

        passwords = ["wrongpassword1", "wrongpassword2", "correct"]
        box = box_zip.Zip(fpath, self.dest_dir, passwords)

        children = box.get_children()
        child_names = self.get_child_names(children)
        self.assertCountEqual(child_names, self.all_files_and_folders)
        self.assertEqual(box.password, "correct")

        box = box_zip.Zip(fpath, self.dest_dir, ["wrong"])
        self.assertRaises(box_base.PasswordError, box.extract)

    def test_unzip_metadata(self):
        """checking metadata"""
        fpath = self.copy_test_file_to_src_dir("normal2.zip")
        box = box_zip.Zip(fpath, self.dest_dir)

        meta2 = box.list_child_meta()
        self.assertEqual(meta2, ["method", "modified"])

        children = box.get_children()
        for child in children:
            date = child.get_meta().get("modified", None)
            self.assertTrue(date)
            method = child.get_meta().get("method", None)
            self.assertEqual(method, "Store")
