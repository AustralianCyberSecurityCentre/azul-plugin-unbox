import os

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box import box_upx
from tests.unbox.base_test import BaseFileTest


class TestUPX(BaseFileTest):
    def test_unpack(self):
        """Test unpacking a UPX packed ELF file."""
        # UPX obfuscated file.
        src_file = self.file_manager.download_file_path(
            "d6e0eb28cfe1b224f061eff0581091dac985516c78d222f4921587d2ec612010"
        )

        box = box_upx.UPX(src_file, self.dest_dir)
        children = box.get_children()
        for child in children:
            self.assertEqual(child.name, "d6e0eb28cfe1b224f061eff0581091dac985516c78d222f4921587d2ec612010")
            self.assertTrue(os.path.exists(child.file_path))

        # Confirm metadata is acquired and loaded correctly.
        meta = box.get_meta()
        self.assertTrue(float(box.metadata_upx_version()))
        self.assertCountEqual(meta.keys(), ["upx_version"])
        self.assertEqual(meta.get("upx_version"), box.metadata_upx_version())

    def test_invalid_file(self):
        """Tests that non-packed files are handled gracefully."""
        tfile = self.src_file = os.path.realpath("/bin/ls")
        box = box_upx.UPX(tfile, self.dest_dir)
        self.assertRaises(box_base.NotSupported, box.extract)
