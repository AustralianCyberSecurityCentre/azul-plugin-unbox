# coding=utf-8
import os

from azul_plugin_unbox.unbox.box import box_szip
from azul_plugin_unbox.unbox.libs import szip
from tests.unbox.base_test import BaseFileTest


class TestSZipBox(BaseFileTest):
    def test_unzip(self):
        """unzipping a normal 7z file."""
        fpath = self.copy_test_file_to_src_dir("normal.7z")
        box = box_szip.Szip(fpath, self.dest_dir)

        children = box.get_children()
        # 7z lib filters out dirs
        self.assertCountEqual(self.get_child_names(children), self.all_files)

        self.assertEqual(self.f1_contents, self.get_f1(children))
        self.assertEqual(self.f2_contents, self.get_f2(children))

    def test_unzip_unicode_file(self):
        """Unzipping a zip file that has children with unicode names."""
        # Zip file that contains children with unicode names.
        fpath = self.file_manager.download_file_path(
            "9f9583d42fdbce1326a10435f0e8c01f1508b55c6f072d73810c7aad22f0fa8a"
        )
        box = box_szip.Szip(fpath, self.dest_dir)

        children = box.get_children()
        # 7z lib filters out dirs
        print(self.get_child_names(children))
        self.assertCountEqual(
            self.get_child_names(children), ["DPSetup.exe", "Readme.txt", "Readme-˵\udcc3\udcf7.htm"]
        )

    def test_unzip_symbolic_directory_in_archive(self):
        """Test that symbolic directories aren't extracted as files."""
        # Zip with symbolic links in it.
        fpath = self.file_manager.download_file_path(
            "c376d4b358dcc87c617ac68b257fb1a2a26baa2abc281ebb458e9d4ce20f4737"
        )
        box = box_szip.Szip(fpath, self.dest_dir)

        children = box.get_children()
        # 7z lib filters out dirs
        print(self.get_child_names(children))
        #
        self.assertCountEqual(
            self.get_child_names(children),
            [
                "OPAutoClicker.app/Contents/Info.plist",
                "OPAutoClicker.app/Contents/PkgInfo",
                "OPAutoClicker.app/Contents/_CodeSignature/CodeResources",
                "OPAutoClicker.app/Contents/MacOS/OPAutoClicker",
                "OPAutoClicker.app/Contents/Resources/paused.icns",
                "OPAutoClicker.app/Contents/Resources/waiting.icns",
                "OPAutoClicker.app/Contents/Resources/clicking.icns",
                "OPAutoClicker.app/Contents/Resources/clicking3.icns",
                "OPAutoClicker.app/Contents/Resources/clicking2.icns",
                "OPAutoClicker.app/Contents/Resources/default.icns",
                "OPAutoClicker.app/Contents/Resources/clicking1.icns",
                "OPAutoClicker.app/Contents/Resources/Base.lproj/MainMenu.nib",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/ShortcutRecorder",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/_CodeSignature/CodeResources",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/ATTRIBUTION.md",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/Assets.car",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/LICENSE.txt",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/Info.plist",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/de.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/el.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/zh-Hans.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/ja.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/en.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/nb.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/es.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/it.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/sk.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/sv.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/cs.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/ko.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/zh-Hant.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/pl.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/pt-BR.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/ru.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/fr.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/nl.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/th.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/pt.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/ro.lproj/ShortcutRecorder.strings",
                "OPAutoClicker.app/Contents/Frameworks/ShortcutRecorder.framework/Versions/A/Resources/ca.lproj/ShortcutRecorder.strings",
            ],
        )

    def test_unzip_password(self):
        """unzipping a passworded SZip file."""
        expected_password = "correct"
        fpath = self.copy_test_file_to_src_dir("passworded.7z")

        passwords = ["wrongpassword1", "wrongpassword2", expected_password]
        box = box_szip.Szip(fpath, self.dest_dir, passwords)

        children = box.get_children()
        # 7z lib filters out dirs
        self.assertCountEqual(self.get_child_names(children), self.all_files)
        self.assertEqual(self.f1_contents, self.get_f1(children))
        self.assertEqual(box.password, expected_password)

    def test_extract_iso(self):
        """7zip works on other file types."""
        # Benign ISO named memtest86+.iso
        fpath = self.file_manager.download_file_path(
            "1b7384a7132696e58f3c7139983b2d79e38b36082627d6f92e4eaca8acb3e29f"
        )
        box = box_szip.Szip(fpath, self.dest_dir)
        children = box.get_children()
        self.assertCountEqual(
            self.get_child_names(children),
            [
                "boot/boot.catalog",
                "boot/memtest.img",
                "README.TXT",
                "[BOOT]/Boot-1.44M.img",
            ],
        )
        # am assuming the readme doesn't change often
        content = self.read_file_from_children(children, "README.TXT")
        self.assertEqual(
            content,
            b"There is nothing to do here\r\r\n"
            b"Memtest86+ is located on the bootsector of this CD\r\r\n"
            b"Just boot from this CD and Memtest86+ will launch",
        )


class Test7ZipLib(BaseFileTest):
    """test libs.szip - Confirm seven zip extracts"""

    def test_sevenzip_healthy_extract(self):
        """libs.szip - test executing sevenzip over healthy archives"""

        fpath = self.copy_test_file_to_src_dir("normal.7z")
        unzipped = [(fname, self.read_file(abs_path)) for fname, abs_path in szip.Unzip(fpath, dest_dir=self.dest_dir)]
        unzipped.sort()

        expected_unzip = [
            (self.tfile1, self.f1_contents),
            (os.path.join(self.tdir1, self.tfile2), self.f2_contents),
        ]
        expected_unzip.sort()
        self.assertEqual(unzipped, expected_unzip)

    def test_password_error(self):
        """libs.szip - test binary with password protected files (contents only, not file names)"""
        expected_password = "correct"
        fpath = self.copy_test_file_to_src_dir("passworded.7z")

        # need to try to access data to force a password error
        unzipped = szip.Unzip(fpath, self.dest_dir)
        self.assertRaises(szip.ExtractNotOKErrors, list, unzipped)

        # check with correct password
        unzipped = [
            (fname, self.read_file(abs_path))
            for fname, abs_path in szip.Unzip(fpath, dest_dir=self.dest_dir, password=expected_password)
        ]
        unzipped.sort()
        expected_unzip = [
            (self.tfile1, self.f1_contents),
            (os.path.join(self.tdir1, self.tfile2), self.f2_contents),
        ]
        expected_unzip.sort()
        self.assertEqual(unzipped, expected_unzip)

    def test_password_encrypted_filenames(self):
        """libs.szip - test binary with filenames encrypted as well as contents"""
        expected_password = "correct"
        fpath = self.copy_test_file_to_src_dir("pwed_names.7z")

        # Trying to create the szip.Unzip object should throw the error (can't list the file)
        self.assertRaises(szip.PasswordProtectedFile, szip.Unzip, fpath)

        # check with correct password
        unzipped = [
            (fname, self.read_file(abs_path))
            for fname, abs_path in szip.Unzip(fpath, dest_dir=self.dest_dir, password="correct")
        ]
        unzipped.sort()
        expected_unzip = [
            (self.tfile1, self.f1_contents),
            (os.path.join(self.tdir1, self.tfile2), self.f2_contents),
        ]
        expected_unzip.sort()
        self.assertEqual(unzipped, expected_unzip)

    def test_sevenzip_unsupported_extract(self):
        """plugins.sevenzip - test executing unsupported files"""
        fpath = self.copy_test_file_to_src_dir(self.tfile1, local_path="data/base")
        self.assertRaises(szip.NotSupportedArchive, szip.Unzip, fpath)
