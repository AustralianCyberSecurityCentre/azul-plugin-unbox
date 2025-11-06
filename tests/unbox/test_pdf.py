from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box import box_pdf
from tests.unbox.base_test import BaseFileTest

raw_bytes_33 = b"q\n\nBT\n48.24 793.926 Td\nET\n\n/DeviceRGB cs\n0.2 0.2 0.2 scn\n/DeviceRGB CS\n0.2 0.2 0.2 SCN\n\nBT\n48.24 793.926 Td\n/F2.0 10.5 Tf\n[<417061636865205a6f6f4b> 20.01953 <6565706572>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n0.73066 Tw\n\nBT\n63.24 775.146 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n0.73066 Tw\n\nBT\n63.24 775.146 Td\n/F1.0 10.5 Tf\n[<417061636865205a6f6f4b> 20.01953 <6565706572206973206120636f726520646570656e64656e637920666f72204b61666b612061732069742070726f7669646573206120636c757374657220636f6f7264696e6174696f6e20736572766963652c>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n0.70444 Tw\n\nBT\n63.24 759.366 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n0.70444 Tw\n\nBT\n63.24 759.366 Td\n/F1.0 10.5 Tf\n[<73746f72696e6720616e64207472> 20.01953 <61636b696e672074686520737461747573206f662062726f6b> 20.01953 <65727320616e6420636f6e73756d6572732e205a6f6f4b> 20.01953 <656570657220697320616c736f207573656420666f7220636f6e74726f6c6c6572>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n63.24 743.586 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n63.24 743.586 Td\n/F1.0 10.5 Tf\n<656c656374696f6e2e> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n48.24 715.806 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n48.24 715.806 Td\n/F2.0 10.5 Tf\n<4b61666b6120436f6e6e656374> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n2.00569 Tw\n\nBT\n63.24 697.026 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n2.00569 Tw\n\nBT\n63.24 697.026 Td\n/F1.0 10.5 Tf\n[<4b61666b6120436f6e6e65637420697320616e20696e74656772> 20.01953 <6174696f6e20746f6f6c6b697420666f722073747265616d696e672064617461206265747765656e204b61666b612062726f6b> 20.01953 <65727320616e64206f74686572>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n2.08686 Tw\n\nBT\n63.24 681.246 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n2.08686 Tw\n\nBT\n63.24 681.246 Td\n/F1.0 10.5 Tf\n<73797374656d73207573696e6720> Tj\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n2.08686 Tw\n\nBT\n139.37021 681.246 Td\n/F3.0 10.5 Tf\n<436f6e6e6563746f72> Tj\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n2.08686 Tw\n\nBT\n189.62321 681.246 Td\n/F1.0 10.5 Tf\n[<20706c7567696e732e204b61666b6120436f6e6e6563742070726f76696465732061206672> 20.01953 <616d65776f726b20666f7220696e74656772> 20.01953 <6174696e67204b61666b61>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n1.34659 Tw\n\nBT\n63.24 665.466 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n1.34659 Tw\n\nBT\n63.24 665.466 Td\n/F1.0 10.5 Tf\n<7769746820616e2065787465726e616c206461746120736f75726365206f72207461726765742c207375636820617320612064617461626173652c20666f7220696d706f7274206f72206578706f7274206f662064617461207573696e67> Tj\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n63.24 649.686 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n63.24 649.686 Td\n/F1.0 10.5 Tf\n[<636f6e6e6563746f72732e20436f6e6e6563746f72732061726520706c7567696e7320746861742070726f766964652074686520636f6e6e656374696f6e20636f6e6669677572> 20.01953 <6174696f6e206e65656465642e>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n-0.5 Tc\n\n0.0 Tc\n\n-0.5 Tc\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n71.8805 621.906 Td\n/F1.0 10.5 Tf\n<a5> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n0.0 Tc\n\nBT\n81.24 621.906 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n81.24 621.906 Td\n/F1.0 10.5 Tf\n<4120> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n91.362 621.906 Td\n/F3.0 10.5 Tf\n<736f75726365> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n123.723 621.906 Td\n/F1.0 10.5 Tf\n<20636f6e6e6563746f72207075736865732065787465726e616c206461746120696e746f204b61666b612e> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n-0.5 Tc\n\n0.0 Tc\n\n-0.5 Tc\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n71.8805 600.126 Td\n/F1.0 10.5 Tf\n<a5> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n0.0 Tc\n\nBT\n81.24 600.126 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n81.24 600.126 Td\n/F1.0 10.5 Tf\n<4120> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n91.362 600.126 Td\n/F3.0 10.5 Tf\n<73696e6b> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n111.669 600.126 Td\n/F1.0 10.5 Tf\n[<20636f6e6e6563746f722065787472> 20.01953 <616374732064617461206f7574206f66204b61666b61>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n81.24 572.346 Td\n/F1.0 10.5 Tf\n[<45787465726e616c2064617461206973207472> 20.01953 <616e736c6174656420616e64207472> 20.01953 <616e73666f726d656420696e746f2074686520617070726f70726961746520666f726d61742e>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n0.24042 Tw\n\nBT\n81.24 544.566 Td\n/F1.0 10.5 Tf\n[<59> 69.82422 <6f752063616e206465706c6f> 20.01953 <79204b61666b6120436f6e6e656374207769746820>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.69412 0.12941 0.27451 scn\n0.69412 0.12941 0.27451 SCN\n\n0.24042 Tw\n\nBT\n261.32067 544.566 Td\n/F4.0 10.5 Tf\n<6275696c64> Tj\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n0.24042 Tw\n\nBT\n287.57067 544.566 Td\n/F1.0 10.5 Tf\n[<20636f6e6669677572> 20.01953 <6174696f6e2074686174206175746f6d61746963616c6c79206275696c6473206120636f6e7461696e6572>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n81.24 528.786 Td\n/F1.0 10.5 Tf\n<696d61676520776974682074686520636f6e6e6563746f7220706c7567696e7320796f75207265717569726520666f7220796f7572206461746120636f6e6e656374696f6e732e> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n48.24 501.006 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n48.24 501.006 Td\n/F2.0 10.5 Tf\n[<4b61666b61204d6972726f724d616b> 20.01953 <6572>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n63.24 482.226 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n63.24 482.226 Td\n/F1.0 10.5 Tf\n[<4b61666b61204d6972726f724d616b> 20.01953 <6572207265706c6963617465732064617461206265747765656e2074776f204b61666b6120636c7573746572732c2077697468696e206f72206163726f737320646174612063656e746572732e>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n2.06042 Tw\n\nBT\n63.24 454.446 Td\n/F1.0 10.5 Tf\n[<4d6972726f724d616b> 20.01953 <65722074616b> 20.01953 <6573206d657373616765732066726f6d206120736f75726365204b61666b6120636c757374657220616e6420777269746573207468656d20746f206120746172676574204b61666b61>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n63.24 438.666 Td\n/F1.0 10.5 Tf\n<636c75737465722e> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n48.24 410.886 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n48.24 410.886 Td\n/F2.0 10.5 Tf\n<4b61666b6120427269646765> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n63.24 392.106 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n63.24 392.106 Td\n/F1.0 10.5 Tf\n[<4b61666b61204272696467652070726f766964657320616e2041504920666f7220696e74656772> 20.01953 <6174696e6720485454502d626173656420636c69656e747320776974682061204b61666b6120636c75737465722e>] TJ\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n48.24 364.326 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n48.24 364.326 Td\n/F2.0 10.5 Tf\n<4b61666b61204578706f72746572> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n2.57356 Tw\n\nBT\n63.24 345.546 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n2.57356 Tw\n\nBT\n63.24 345.546 Td\n/F1.0 10.5 Tf\n[<4b61666b61204578706f727465722065787472> 20.01953 <61637473206461746120666f7220616e616c797369732061732050726f6d657468657573206d6574726963732c207072696d6172696c7920646174612072656c6174696e6720746f>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n1.02991 Tw\n\nBT\n63.24 329.766 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n1.02991 Tw\n\nBT\n63.24 329.766 Td\n/F1.0 10.5 Tf\n[<6f6666736574732c20636f6e73756d65722067726f7570732c20636f6e73756d6572206c616720616e6420746f706963732e20436f6e73756d6572206c6167206973207468652064656c61> 20.01953 <79206265747765656e20746865206c617374>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\n0.31306 Tw\n\nBT\n63.24 313.986 Td\nET\n\n\n0.0 Tw\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\n0.31306 Tw\n\nBT\n63.24 313.986 Td\n/F1.0 10.5 Tf\n[<6d657373616765207772697474656e20746f206120706172746974696f6e20616e6420746865206d6573736167652063757272656e746c79206265696e67207069636b> 20.01953 <65642075702066726f6d207468617420706172746974696f6e2062> 20.01953 <79>] TJ\nET\n\n\n0.0 Tw\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\n\nBT\n63.24 298.206 Td\nET\n\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n63.24 298.206 Td\n/F1.0 10.5 Tf\n<6120636f6e73756d6572> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\nq\n0.0 0.0 0.0 scn\n0.0 0.0 0.0 SCN\n1 w\n0 J\n0 j\n[] 0 d\n/Stamp2 Do\n0.2 0.2 0.2 scn\n0.2 0.2 0.2 SCN\n\nBT\n49.24 14.263 Td\n/F1.0 9 Tf\n<34> Tj\nET\n\n0.0 0.0 0.0 SCN\n0.0 0.0 0.0 scn\nQ\nQ\n"


class TestPdf(BaseFileTest):
    """Test Box Pdf."""

    def setUp(self):
        """Create some test files to archive later. These files should be removed in the teardown."""
        super().setUp()
        self.tfile_pdf = "strimzi-doc-overview.pdf"
        self.tfile_pdf_encrypted = self.tfile_pdf + ".encrypted"
        self.pdf_obj_count = 74

    # def _encrypt_pdf(self, passwords: list[str]) -> str:
    #     """Encrypt a PDF with the supplied passwords"""
    #     encrypted_pdf = os.path.join("tmp", self.tfile_pdf_encrypted)
    #     args = [
    #         "qpdf",
    #         "--encrypt",
    #         "128",
    #         "--",
    #         os.path.join(self.src_dir, self.tfile_pdf),
    #         encrypted_pdf,
    #     ]
    #     if passwords:
    #         for password in passwords:
    #             args.insert(2, password)
    #     stderr,stdout = subprocess.Popen(
    #         args,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #     ).communicate()
    #     print(stdout.decode())
    #     print(stderr.decode())

    #     return encrypted_pdf

    def test_pdf(self):
        """Opening a normal pdf file."""
        # PDF of Strimzi documentation Overview.
        fpath = self.file_manager.download_file_path(
            "8a12eaab6b5ff3a80ed6a8f86a06e55340a04109e443b431b0ed913eebbf7690"
        )
        box = box_pdf.Pdf(fpath, self.dest_dir)
        children = box.get_children()

        self.assertEqual(len(children), self.pdf_obj_count)
        for child in children:
            meta_values = child.get_meta()
            self.assertCountEqual(meta_values.keys(), ["object_id", "object_dictionary", "stream_filter"])

        # Check child object has specific value:
        self.assertEqual(self.read_file_from_children(children, "33/0"), raw_bytes_33)

    def test_pdf_password(self):
        """Decrypting a password protected pdf file."""
        # encrypt the existing pdf before testing
        # fpath = self._encrypt_pdf(["super", "secret"])
        # Benign PDF of Strimzi documentation overview with added encryption.
        fpath = self.file_manager.download_file_path(
            "940de252f44c5d2f4e6a67bff3e3071f7e4871410886ccb33d2fe4a1c6865429"
        )

        # show we can decrypt it with either user or owner password
        passwords = ["wrongpassword1", "super"]
        box = box_pdf.Pdf(fpath, self.dest_dir, passwords=passwords)
        self.assertEqual(len(box.get_children()), self.pdf_obj_count)
        self.assertEqual("super", box.password)

        passwords2 = ["wrongpassword1", "secret"]
        box = box_pdf.Pdf(fpath, self.dest_dir, passwords=passwords2)
        self.assertEqual(len(box.get_children()), self.pdf_obj_count)
        self.assertEqual("secret", box.password)

        box = box_pdf.Pdf(fpath, self.dest_dir, passwords=["not correct"])
        self.assertRaises(box_base.PasswordError, box.extract)

    def test_pdf_empty_password(self):
        """Decrypting a null passworded pdf file."""
        # PDF from strimzi documentation with Null encrypted
        fpath = self.file_manager.download_file_path(
            "7aa1fc882ba9f861e2052dd35d803a485d40a4f932df5c46736da51a6b5c5c5c"
        )
        # fpath = self._encrypt_pdf(["", ""])

        box = box_pdf.Pdf(fpath, self.dest_dir, passwords=["not correct"])
        self.assertEqual(len(box.get_children()), self.pdf_obj_count)
        self.assertEqual("", box.password)

        box = box_pdf.Pdf(fpath, self.dest_dir, passwords=None)
        self.assertEqual(len(box.get_children()), self.pdf_obj_count)
        self.assertEqual("", box.password)

    def test_pdf_in_memory(self):
        """Opening a normal pdf file using in memory objects."""
        # PDF of Strimzi documentation Overview.
        fpath = self.file_manager.download_file_path(
            "8a12eaab6b5ff3a80ed6a8f86a06e55340a04109e443b431b0ed913eebbf7690"
        )
        box = box_pdf.Pdf(fpath, self.dest_dir, low_memory=False)
        children = box.get_children()

        self.assertEqual(len(children), self.pdf_obj_count)
        for child in children:
            meta_values = child.get_meta()
            self.assertCountEqual(meta_values.keys(), ["object_id", "object_dictionary", "stream_filter"])
            self.assertIsNotNone(child.raw_data)

        # Check child object has specific value:
        content = None
        for child in children:
            if child.name == "33/0":
                content = child.raw_data
        self.assertEqual(content, raw_bytes_33)

    def test_not_pdf(self):
        """Unbox a non-pdf file."""
        fpath = self.copy_test_file_to_src_dir(self.tfile1, local_path="data/base")
        box = box_pdf.Pdf(fpath, self.dest_dir)
        self.assertRaises(box_base.NotSupported, box.extract)

    def test_meta_list(self):
        self.check_metadata_list_correct(
            box_pdf.Pdf(self.src_dir, self.dest_dir), [], ["object_id", "object_dictionary", "stream_filter"]
        )
