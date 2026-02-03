"""Box module to support unzipping zip archives."""

import os
import zipfile
from datetime import datetime

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild

# Try and match 7zip output.
zip_compression_dict = {
    zipfile.ZIP_STORED: "Store",
    zipfile.ZIP_DEFLATED: "Deflate",
    zipfile.ZIP_BZIP2: "bzip2",
    zipfile.ZIP_LZMA: "LZMA",
}


class Zip(box_base.Box):
    """Zip format unpacker."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new zip unpacker for the given filepath."""
        super().__init__(src_filepath, target_dir, passwords)
        self.__zip_file = None

    def __get_zipfile(self) -> zipfile.ZipFile:
        """Get a reference to the zip file if it already exists, and always sets the new password."""
        if not self.__zip_file:
            self.__zip_file = zipfile.ZipFile(self.src_filepath)
        self.__zip_file.setpassword(self.password_bytes)
        return self.__zip_file

    def _extract(self):
        """Extract all contents of the zip file to the destination directory."""
        try:
            self.__get_zipfile().extractall(path=self.dest_filedir, pwd=self.password_bytes)
        except RuntimeError as e:
            if isinstance(e, NotImplementedError):
                # Typically message is "That compression method is not supported"
                raise box_base.NotSupported(f"{e}") from e
            raise box_base.PasswordError() from e
        except ValueError as e:
            raise box_base.NotSupported("Bad Zip Header, probably an invalid zip file.") from e
        except OSError as e:  # Occurs when malformed zip file returns a negative header offset.
            raise box_base.NotSupported("Bad Zip Header, probably an invalid zip file.") from e
        except Exception as bad_zip:
            raise box_base.NotSupported(str(bad_zip)[:80] + "...") from bad_zip

    def _get_all_children(self) -> list[BoxChild]:
        """Obtain all child objects from the zip and return them."""
        children = list()
        for each_child in self.__get_zipfile().namelist():
            child_path = os.path.join(self._target_dir, each_child)
            new_child = BoxChild(each_child, child_path)
            self.child_metadata_modified(new_child)
            self.child_metadata_method(new_child)
            children.append(new_child)

        return children

    def child_metadata_method(self, new_child: BoxChild):
        """Return the compression method for the specified child object."""
        zip_info = self.__get_zipfile().getinfo(new_child.name)
        new_child._meta["method"] = zip_compression_dict.get(zip_info.compress_type, None)

    def child_metadata_modified(self, new_child: BoxChild):
        """Gets the creation date for child objects."""
        zip_info = self.__get_zipfile().getinfo(new_child.name)
        try:
            time = datetime(*zip_info.date_time).isoformat()
        except ValueError:
            # corrupted date
            return
        new_child._meta["modified"] = time
