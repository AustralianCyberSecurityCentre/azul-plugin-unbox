"""Box module to support the RAR archive format."""

import datetime
import os
import subprocess  # noqa: S404 # nosec B404

import rarfile

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild

# ensure unrar is installed in this OS
try:
    subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
        ["unrar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
except OSError as err:
    raise ImportError(
        "error = %s\nmodule 'rarfile' requires the program 'unrar'. Please run apt-get install unrar" % str(err)
    ) from err


class Rar(box_base.Box):
    """RAR archive box handler."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a new rar unpacker which can extract RAR files."""
        super().__init__(src_filepath, target_dir, passwords)
        self.__rar_file = None

    def __get_password_or_none(self):
        """Gets the password or None if the password is currently an empty string.

        This method is required because RAR doesn't handle empty string passwords very well.
        """
        password = self.password
        if self.password == "":  # nosec B105
            # rarfile hangs on empty password (calls unrar with -p)
            password = None
        return password

    def __get_rarfile(self):
        """Get the RAR file, will throw an exception if the password is invalid."""
        if not self.__rar_file:
            self.__rar_file = rarfile.RarFile(self.src_filepath)
        try:
            self.__rar_file.setpassword(self.__get_password_or_none())
        except rarfile.BadRarFile as e:
            raise box_base.PasswordError() from e
        return self.__rar_file

    def _extract(self):
        """Extract RAR file to target directory."""
        try:
            self.__get_rarfile().extractall(path=self.dest_filedir, pwd=self.__get_password_or_none())
        except rarfile.PasswordRequired as e:
            raise box_base.PasswordError() from e
        except rarfile.BadRarFile as e:
            # Depending on the error message, we might need to raise a
            # PasswordError here
            if str(e).startswith("Failed the read enough data"):
                raise box_base.PasswordError() from e
            elif "CRC check failed" in str(e):
                raise box_base.PasswordError() from e

            raise box_base.NotSupported("File is corrupt") from e

    def _get_all_children(self) -> list[BoxChild]:
        """Obtain all BoxChild objects associated with the files extracted from the archive."""
        infolist = self.__get_rarfile().infolist()
        if not infolist:
            raise box_base.PasswordError()

        children = list()

        for each_file in infolist:
            if each_file.isdir():
                continue
            new_child = BoxChild(each_file.filename, os.path.join(self.dest_filedir, each_file.filename))
            self.child_metadata_createdate(new_child)
            self.child_metadata_compresstype(new_child)
            children.append(new_child)

        return children

    def child_metadata_createdate(self, new_child: BoxChild):
        """Return the creation date of the specified child object, as a datetime obj."""
        dt_tuple = self.__get_rarfile().getinfo(new_child.name).date_time
        new_child._meta["createdate"] = datetime.datetime(*dt_tuple).isoformat()

    def child_metadata_compresstype(self, new_child: BoxChild):
        """Return the compression type (value) of the specified child object."""
        t = self.__get_rarfile().getinfo(new_child.name)
        new_child._meta["compresstype"] = t.compress_type
