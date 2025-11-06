# coding=utf-8
from azul_plugin_unbox.unbox.box import box_arj
from tests.unbox.base_test import BaseFileTest


class TestArj(BaseFileTest):
    def test_unarj(self):
        """unzipping a normal Arj file"""
        # create an arj file
        fpath = self.copy_test_file_to_src_dir("normal.arj")

        box = box_arj.Arj(fpath, self.dest_dir)
        children = box.get_children()

        self.assertCountEqual(self.get_child_names(children), self.all_files_no_dir_info)
        self.assertEqual(self.f1_contents, self.get_f1(children))
        self.assertEqual(self.f2_contents, self.read_file_from_children(children, self.tfile2))

    def test_unarj_password(self):
        """unzipping a passworded Arj file"""
        # create a tar file
        expected_password = "supersecret"
        fpath = self.copy_test_file_to_src_dir(
            "encrypted.arj",
        )
        passwords = ["wrongpassword1", "wrongpassword2", expected_password]
        box = box_arj.Arj(fpath, self.dest_dir, passwords)

        children = box.get_children()
        self.assertCountEqual(self.get_child_names(children), self.all_files_no_dir_info)
        self.assertEqual(self.f1_contents, self.get_f1(children))
        self.assertEqual(box.password, "supersecret")
