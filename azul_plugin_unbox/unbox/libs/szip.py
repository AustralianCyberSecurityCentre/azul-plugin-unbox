"""Python wrapper for 7z command-line tool."""

import os
import re
import stat
import subprocess  # noqa: S404 # nosec B404

"""
Path = pdfid_v0_0_7.zip
Folder = -
Size = 4471
Packed Size = 4471
Modified = 2009-07-10 08:26:06
Created =
Accessed =
Attributes = ....A
Encrypted = -
Comment =
CRC = B1832CEC
Method = Store
Host OS = FAT

"""


class BaseSevenZipException(Exception):
    """Base exception for seven zip."""

    def __init__(self, *args):
        """Create an exception for the specified filename."""
        super().__init__(*args)
        self.value = ""

    def __str__(self):
        """Human-readable exception message string."""
        return f"{self.value}"


class SevenZipException(BaseSevenZipException):
    """General error trying unzip using 7zip."""

    def __init__(self, filename, msg):
        """Create an exception for the specified filename."""
        super().__init__(filename, msg)
        self.value = "Error in %s: %s" % (filename, msg)
        self.cause = msg


class NotSupportedArchive(BaseSevenZipException):
    """Not a valid archive format that 7z accepts."""

    def __init__(self, filename, stdout):
        """Create an exception for the specified filename."""
        super().__init__(filename, stdout)
        self.file = filename
        self.stdout = stdout
        self.value = "Not supported archive: %s" % filename


class WeirdFileBug(Exception):
    """Info for this file meets the requirements for the WeirdFileBug."""


class ExtractNotOK(Exception):
    """Raised when we don't get Everything is ok in our stderr."""


class NoPathEquals(BaseSevenZipException):
    """Parsing error for filepath information."""


class PasswordProtectedFile(BaseSevenZipException):
    """Encrypted zip and no password or incorrect password supplied."""

    def __init__(self, filename):
        """Create an exception for the specified filename."""
        super().__init__(filename)
        self.file = filename
        self.value = "Password protected file: %s" % filename


class FailedToConvertSize(Exception):
    """Unexpected size string parsed from output."""


class ExtractNotOKErrors(BaseSevenZipException):
    """Raised at the end of the iter sequence if there are any iter errors."""

    def __init__(self, errors):
        """Create an exception, wrapping the supplied error list."""
        super().__init__(errors)
        self.errors = errors
        self.value = "\n > " + "\n > ".join(["%s" % e for e in errors])


class FailedToExtractError(Exception):
    """Raised when 7zip failed to extract a file to the target directory."""


PATTERN_DETAILS = re.compile("(.*?) = (.*)")

EVERYTHING_OK = re.compile("Everything is Ok")


class Unzip(object):
    """Unpacker for archive formats supported by 7Zip."""

    def __init__(self, filepath, dest_dir=None, password="", except_on_password=True):  # nosec B107
        """Create a new unzipper for the sepecified filepath."""
        self.filepath = filepath
        self.password = password
        if not self.password:
            self.password = ""  # nosec B105
        self.except_on_password = except_on_password

        self.dest_dir = dest_dir

        stdout_lines = []
        stderr_lines = []

        # NOTE: this can get into a weird state when 7zip prompts for a
        # password in this case, 7zip will wait on input from stdin
        args = ["7zzs", "l", "-sccUTF-8", "-p%s" % (self.password or ""), "-slt", filepath]
        proc = subprocess.run(  # noqa: S603, S607 # nosec B603 B607
            args,
            env={"TZ": "UTC"},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            encoding="utf-8",
            errors="surrogateescape",  # Handle unicode encoding errors
        )

        for pipe, lines in [(proc.stdout, stdout_lines), (proc.stderr, stderr_lines)]:
            # Strip all additional whitespace up until the info structure
            reached_info_structure = False
            for line in pipe.splitlines():
                stripped = line.rstrip()
                if stripped == "--":
                    reached_info_structure = True
                if len(stripped) > 0 or reached_info_structure:
                    lines.append(stripped)

        # check for a not supported archive error. notes on formats:
        #   'is not supported archive' was the format used in old windows 7z
        #   'Cannot open file as archive' is used 2010 ubuntu 7z
        # Version 16.02 (Ubuntu 18.04) uses a slightly different error message, sent to stderr
        for err_msg in (
            "Error: %s: is not supported archive" % filepath,
            "Error: %s: Cannot open file as archive" % filepath,
            "ERROR: %s : Cannot open the file as archive" % filepath,
        ):
            if err_msg in stdout_lines or err_msg in stderr_lines:
                raise NotSupportedArchive(filepath, err_msg)

        if ("Error: %s: Cannot open encrypted archive. Wrong password?" % filepath) in stdout_lines or (
            "ERROR: %s : Cannot open encrypted archive. Wrong password?" % filepath
        ) in stderr_lines:
            raise PasswordProtectedFile(filepath)

        # check for any other error
        next_line_error = False
        for line in stdout_lines:
            if next_line_error or line.startswith("Error"):
                raise SevenZipException(filepath, line)
            elif line.startswith("ERRORS"):
                # The next line will contain an error message
                next_line_error = True

        # remove the header from our filepath list
        try:
            while not stdout_lines[0].startswith("Path ="):
                stdout_lines.pop(0)
        except IndexError as e:
            raise NoPathEquals(filepath, "No archive found or path for file does not exist") from e

        # pull out each info element
        self.fileinfo = []
        self._filenames = set()

        info_lines = []

        for line in stdout_lines:
            if line == "":
                file_info = self._get_file_info(info_lines)

                if self._validate_info(file_info):
                    self.fileinfo.append(file_info)
                    self._filenames.add(file_info["Path"])

                info_lines = []
            else:
                info_lines.append(line)
        # handle special case of Listing archive BUG
        self._check_if_listing_archive_bug()

    @staticmethod
    def _parse_info_line(line):
        """Return a file info dictionary from the first few params of info."""
        m = PATTERN_DETAILS.match(line)
        if m:
            name, val = m.groups()
            # assert not name in info
            return {name: val}

        return None

    def _get_file_info(self, lines):
        """Return a file info dictionary from the first few params of info."""
        file_info = dict()

        for line in lines:
            info = self._parse_info_line(line)
            if info:
                file_info.update(info)

        return file_info

    def _check_if_listing_archive_bug(self):
        """Return if encountered unexplainable file perm bug on Windows.

        Check for the following output:

        7-Zip 4.57  Copyright (c) 1999-2007 Igor Pavlov  2007-12-06
        p7zip Version 4.57 (locale=C,Utf16=off,HugeFiles=on,8 CPUs)
        Can't load '/usr/lib/p7zip/Codecs/.keep-p7zip' (Permission denied)


        ----------
        Path = file
        Size = 4096
        Packed Size = 4096

        7-Zip 4.57  Copyright (c) 1999-2007 Igor Pavlov  2007-12-06
        p7zip Version 4.57 (locale=C,Utf16=off,HugeFiles=on,8 CPUs)
        Can't load '/usr/lib/p7zip/Codecs/.keep-p7zip' (Permission denied)
        """
        if len(self.fileinfo) != 1:
            return

        info = self.fileinfo[0]

        if info["Path"] != "file":
            return

        filesize = os.stat(self.filepath)[stat.ST_SIZE]
        if info["Size"] != filesize:
            return

        raise WeirdFileBug()

    def _validate_info(self, info):
        """Validate we have the correct keys and details for a valid file."""
        # ensure we've got the minimum keys
        required_keys = {"Path", "Size"}
        if required_keys - set(info.keys()):
            return False

        # make sure we can convert size into an int
        try:
            info["Size"] = int(info["Size"], 10)
        except ValueError:
            return False

        if self._is_directory(info):
            return False

        if self._is_symbolic_link(info):
            return False

        return True

    @staticmethod
    def _is_symbolic_link(info):
        """Ensure that we don't add a symbolic link that can be a file or a directory as a file."""
        attrib = info.get("Attributes", "").strip()
        if attrib.startswith("l"):
            return True
        return False

    @staticmethod
    def _is_directory(info):
        """Ensure that we don't add a directory as a file."""
        attrib = info.get("Attributes", "")
        if attrib.startswith("D"):
            return True
        if info.get("Folder") == "+":
            return True
        if attrib == "D....":
            return True
        if attrib.startswith("D_ d"):
            return True
        return False

    def __len__(self):
        """Unzip length is the number of file entries."""
        return len(self.fileinfo)

    def extract(self, filename: str, output_dir: str) -> str:
        """Extract specified filename from archive, using 7z.

        Will use supplied password or default to any supplied during init.
        """
        if filename not in self._filenames:
            # Some versions of 7z report no error if you try to extract a nonexistent file
            raise ExtractNotOK("No such file in archive: '%s'" % filename)

        args = [
            "7zzs",
            "x",
            "-aoa",  # 7zzs creates file paths before unpacking. Then prompting to overwrite. Set to overwrite all.
            "-sccUTF-8",
            f"-o{output_dir}",
            "-p%s" % self.password,
            self.filepath,
            filename,
        ]
        # execute seven zip
        # We always use -p arg so we are never prompted for password
        proc = subprocess.run(  # noqa: S603, S607 # nosec B603 B607
            args,
            env={"TZ": "UTC", "LANG": "C.UTF-8"},
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="surrogateescape",  # Handle unicode encoding errors
        )

        if proc.stderr and not EVERYTHING_OK.search(proc.stderr):
            # Some versions return 'everything ok', others return an empty stderr on success
            msg = "failed to extract %s" % filename
            raise ExtractNotOK(msg)

        output_path = os.path.join(output_dir, filename)
        if not os.path.exists(output_path):
            raise FailedToExtractError()

        return output_path

    def extractall(self, output_dir: str) -> str:
        """Extract all files from archive, using 7z.

        Will use supplied password or default to any supplied during init.
        """
        args = [
            "7zzs",
            "x",
            "-aoa",  # 7zzs creates file paths before unpacking. Then prompting to overwrite. Set to overwrite all.
            "-sccUTF-8",
            f"-o{output_dir}",
            "-p%s" % self.password,
            self.filepath,
        ]
        # execute seven zip
        # We always use -p arg so we are never prompted for password
        proc = subprocess.run(  # noqa: S603, S607 # nosec B603 B607
            args,
            env={"TZ": "UTC", "LANG": "C.UTF-8"},
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="surrogateescape",  # Handle unicode encoding errors
        )

        if proc.stderr and not EVERYTHING_OK.search(proc.stderr):
            # Some versions return 'everything ok', others return an empty stderr on success
            if "Wrong password" in proc.stderr:
                raise PasswordProtectedFile("Password provided was invalid.")
            msg = "failed to extract files"
            raise ExtractNotOK(msg)

        for file_path in self.fileinfo:
            path = os.path.join(output_dir, file_path["Path"])
            if not os.path.exists(path):
                raise FailedToExtractError()

    def __iter__(self):
        """Loop through file entries, yielding tuple of filepath, abs_file_path."""
        extract_errors = []
        if self.dest_dir is None or self.dest_dir == "":
            raise Exception("Destination directory not set for iteration.")
        for info in self.fileinfo:
            file_path = None
            try:
                file_path = self.extract(info["Path"], self.dest_dir)
            except ExtractNotOK as err:
                if info.get("Encrypted", "-") == "+":
                    if self.password is not None and self.password != "":  # nosec B105
                        raise PasswordProtectedFile(info["Path"]) from err
                    extract_errors.append(PasswordProtectedFile(info["Path"]))
                else:
                    extract_errors.append(err)
            if file_path is not None:
                # return the tuple of filename and filedata
                yield info["Path"], file_path
        if extract_errors:
            raise ExtractNotOKErrors(extract_errors)
