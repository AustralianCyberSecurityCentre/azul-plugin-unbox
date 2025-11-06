# coding=utf-8
import os
import os.path
import signal
import stat

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box import box_rar
from tests.unbox.base_test import BaseFileTest


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    """handle the timeout signal"""
    del signum, frame
    raise TimeoutError()


class TestRar(BaseFileTest):
    def test_previous_read_only(self):
        fpath = self.copy_test_file_to_src_dir("normal.rar")

        target = os.path.join(self.dest_dir, "thing")
        with open(target, "w") as f:
            f.write("hello")

        mode = os.stat(target).st_mode
        ro_mask = 0o777 ^ (stat.S_IWRITE | stat.S_IWGRP | stat.S_IWOTH)
        os.chmod(target, mode & ro_mask)

        # trigger cleanup code
        box = box_rar.Rar(fpath, self.dest_dir)

    def test_unrar(self):
        """unzipping a normal Rar file"""
        fpath = self.copy_test_file_to_src_dir("normal.rar")
        box = box_rar.Rar(fpath, self.dest_dir)

        children = box.get_children()
        self.assertCountEqual(self.get_child_names(children), self.all_files)
        self.assertEqual(self.f1_contents, self.get_f1(children))

    def test_unrar_password(self):
        """unzipping a passworded Rar file"""
        expected_password = "correct"
        fpath = self.copy_test_file_to_src_dir("passworded.rar")
        passwords = ["wrongpassword1", "wrongpassword2", expected_password]
        box = box_rar.Rar(fpath, self.dest_dir, passwords)

        children = box.get_children()
        self.assertCountEqual(self.get_child_names(children), self.all_files)
        self.assertEqual(self.f1_contents, self.get_f1(children))
        self.assertEqual(box.password, expected_password)

    def test_unrar_unknown_password(self):
        """unzipping a passworded Rar file"""
        expected_password = "correct"
        fpath = self.copy_test_file_to_src_dir("passworded.rar")
        passwords = ["wrongpassword1"]

        box = box_rar.Rar(fpath, self.dest_dir, passwords)
        self.assertRaises(box_base.PasswordError, box.extract)

    def test_rar_metadata(self):
        """metadata for a rar file"""
        fpath = self.copy_test_file_to_src_dir("normal.rar")
        box = box_rar.Rar(fpath, self.dest_dir)

        self.check_metadata_list_correct(box, [], ["compresstype", "createdate"])
        children = box.get_children()
        for child in children:
            meta = child.get_meta()
            self.assertTrue(meta["createdate"])
            self.assertTrue(meta["compresstype"])

    def test_empty_password(self):
        """ensure empty string password doesn't hang"""
        expected_password = "correct"
        fpath = self.copy_test_file_to_src_dir("passworded.rar")
        # rarfile will hang on empty string password, make sure we skip it
        passwords = ["", expected_password]

        box = box_rar.Rar(fpath, self.dest_dir, passwords)

        # timeout 30sec just in case the empty string isn't ignored
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)

        try:
            children = box.get_children()
            content = self.get_f1(children)
        finally:
            signal.alarm(0)

        self.assertCountEqual(self.get_child_names(children), self.all_files)
        self.assertEqual(self.f1_contents, content)

        # test only empty password
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)

        passwords = [""]
        box = box_rar.Rar(fpath, self.dest_dir, passwords)
        try:
            self.assertRaises(box_base.PasswordError, box.extract)
        finally:
            signal.alarm(0)
