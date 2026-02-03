"""Box module for unpacking unix archives and compression like Tar and GZip."""

import bz2
import enum
import gzip
import io
import os
import tarfile
import zlib

from azul_plugin_unbox.unbox import box_base
from azul_plugin_unbox.unbox.box_child import BoxChild


def resolve(path):
    """Fully resolve any symlink and relative paths."""
    # we need to handle safe extraction of possibly malicious tarfiles
    # not just abspaths but relative and symlinks too
    return os.path.realpath(os.path.abspath(path))


def badpath(path, base):
    """Return if path resolves outside base dir."""
    return not resolve(os.path.join(base, path)).startswith(base)


def badlink(info, base):
    """Return if link resolves outside own tree."""
    tip = resolve(os.path.join(base, os.path.dirname(info.name)))
    return badpath(info.linkname, base=tip)


def safemembers(members, base):
    """Only yield 'safe' member fileinfo members."""
    for finfo in members:
        if badpath(finfo.name, base):
            pass
        elif finfo.issym() and badlink(finfo, base):
            pass
        elif finfo.islnk() and badlink(finfo, base):
            pass
        else:
            yield finfo


class ArchiveType(enum.Enum):
    """Type of the archive being extracted."""

    TAR = 1
    BZ2 = 2
    GZ = 3
    UNKNOWN = 4


class Archive(box_base.Box):
    """Box for handling Unix archives .tar, .tar.gz, .tar.bz2, .gz and .bz2."""

    def __init__(self, src_filepath: str, target_dir: str, passwords=None):
        """Create a box for the given filepath.

        Passwords not supported for Archive box type.
        """
        super().__init__(src_filepath, target_dir, passwords)
        self._archive_type: ArchiveType = ArchiveType.UNKNOWN
        self.__single_child_fname: str = ""
        self.__metadata_encoding: str = None
        self.__metadata_extra_content: str = None

    def __write_single_compressed_file(self, fh: gzip.GzipFile | bz2.BZ2File | io.BufferedRandom, strip_ext: str):
        """Write a compressed Gzip or Bz2 file to disk through a stream."""
        # Remove extension if present.
        self.__single_child_fname = os.path.basename(self.src_filepath.rstrip(strip_ext))
        # Buffered write contents into target file.
        with open(os.path.join(self.dest_filedir, self.__single_child_fname), "wb", buffering=1) as f2:
            while fh.peek(1):
                f2.write(fh.read(65536))

    def _extract(self):
        """Override extracts the contents of the provided file using either tar, gzip or bz2."""
        try:
            with tarfile.open(self.src_filepath) as t:
                t.extractall(self.dest_filedir, members=safemembers(t, self.dest_filedir))  # nosec B202
                self.__metadata_encoding = t.encoding
                self._archive_type = ArchiveType.TAR
                return
        except (tarfile.ReadError, IOError, EOFError):
            # reading as tar failed try as gz/bz2
            pass

        try:
            with gzip.GzipFile(self.src_filepath, "rb") as t:
                self._test_archive(t)
                self.__write_single_compressed_file(t, ".gz")
                self._archive_type = ArchiveType.GZ
                return
        except (IOError, EOFError):
            pass

        # Work around https://github.com/python/cpython/issues/68489#issuecomment-1488203471
        # Handles gzip files which have extra garbage appended to the end.
        try:
            with open(self.src_filepath, "rb") as t:
                data = zlib.decompress(t.read(), wbits=31)
                self.__write_single_compressed_file(io.BufferedRandom(io.BytesIO(data)), ".gz")
                self._archive_type = ArchiveType.GZ
                self.__metadata_extra_content = "true"
                return
        except Exception:  # nosec B110
            pass

        try:
            with bz2.BZ2File(self.src_filepath, "rb") as t:
                self._test_archive(t)
                self.__write_single_compressed_file(t, ".bz2")
                self._archive_type = ArchiveType.BZ2
                return
        except Exception as e:
            raise box_base.NotSupported("Unable to process as tar, gz or bz2") from e

    def _get_all_children(self) -> list[BoxChild]:
        """Gets all of the child objects extracted from the Archive and the associated metadata.

        If the file type is BZ2 or GZ only a single child is present as the original file was simply compressed.
        """
        if self._archive_type == ArchiveType.TAR:
            try:
                children = list()
                with tarfile.open(self.src_filepath) as t:
                    for m in t:
                        fname = m.name
                        if m.isdir():
                            fname += "/"
                        fpath = os.path.join(self.dest_filedir, fname)
                        children.append(BoxChild(fname, fpath))
                return children
            except (tarfile.ReadError, IOError, EOFError) as e:
                raise box_base.NotSupported("Unable to process as tar but was expecting a tar file.") from e
        elif self._archive_type in [ArchiveType.BZ2, ArchiveType.GZ]:
            return [BoxChild(self.__single_child_fname, os.path.join(self.dest_filedir, self.__single_child_fname))]

        else:
            raise box_base.NotSupported("Unable to process as tar, gz or bz2 but extract was successful!")

    @staticmethod
    def _test_archive(stream):
        """Test read an archive to see if it can be decompressed."""
        stream.read(8192)
        stream.seek(0)

    def metadata_encoding(self):
        """Return the character encoding of the tar file or None if not valid."""
        return self.__metadata_encoding

    def metadata_has_extra_content(self) -> None | str:
        """Return if there is extra content in the gzip file."""
        return self.__metadata_extra_content
