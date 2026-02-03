"""Python wrapper for the command-line unarj tool."""

import datetime
import os
import re
import subprocess  # noqa: S404 # nosec B404


class ArjException(Exception):
    """Base wraper for ARJ command-line exceptions."""

    def __init__(self, *args):
        """Create a new exception for the given filename."""
        super().__init__(*args)
        self.value = ""

    def __str__(self):
        """Human-readable string representation of error."""
        return str(self.value)


class NotFoundArchive(ArjException):
    """The specified ARJ file was not found."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.file = filename
        self.msg = msg
        self.value = "Not found archive: %s, msg = %s" % (filename, msg)


class NotSupportedArchive(ArjException):
    """The specified ARJ file was not a supported version."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.file = filename
        self.msg = msg
        self.value = "Not supported archive: %s" % filename


class ArjHeaderException(ArjException):
    """Exception when reading the file's ARJ header."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.value = "Didn't get correct header %s:%s" % (filename, msg)


class ArjFilePathException(ArjException):
    """Error extracting ARJ file path."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.value = "Didn't get filepath as expected %s:%s" % (filename, msg)


class ArjTimesException(ArjException):
    """Error extracting file time from ARJ."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.value = "Didn't get times as expected %s:%s" % (filename, msg)


class FileCountMisMatchException(ArjException):
    """Mismatch in expected and actual file counts occurred."""

    def __init__(self, filename, extracted_files, total_count, extracted):
        """Create a new exception for the given filename and mismatches."""
        super().__init__(filename, extracted_files, total_count, extracted)
        self.value = "Got %d extracted files but ARJ expects %d: %s" % (extracted_files, total_count, extracted)


class FileCountFormatException(ArjException):
    """Error parsing the command-line output counts from unarj."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.value = "Didn't get file list total %s:%s" % (filename, msg)


class FileInfoFormatException(ArjException):
    """Error parsing the command-line output file info from unarj."""

    def __init__(self, msg):
        """Create a new fileinfo exception."""
        super().__init__(msg)
        self.value = "Can't parsed file info '%s'" % msg


class ExtractNotOK(ArjException):
    """Raised when we don't get Everything is ok in our stderr."""


class PasswordProtectedFile(ArjException):
    """Encrypted ARJ and no password specified."""

    def __init__(self, filename):
        """Create a new exception for the given filename."""
        super().__init__(filename)
        self.file = filename
        self.value = "Password protected file: %s" % filename


class ExtractNotOKErrors(ArjException):
    """Raised at the end of the iter sequence if there are any iter errors."""

    def __init__(self, errors):
        """Create a new exception for the given extraction errors."""
        super().__init__(errors)
        self.value = "\n > " + "\n > ".join([str(error) for error in errors])


class IncorrectPasswordException(ArjException):
    """Encrypted ARJ and wrong password specified."""

    def __init__(self, filename, password):
        """Create a new exception for the given filename and attempted password."""
        super().__init__(filename, password)
        self.file = filename
        self.value = "Incorrect password '%s' for  %s" % (password, filename)


def parse_info(lines):
    """Parse the stdout of the unarj command-line.

    Returns a tuple of parsed dict, count of lines.
    """
    # handle several formats
    m = INFO_PATTERN2.match(lines[0])
    if m is None:
        m = INFO_PATTERN4.match(lines[0])
    if m is not None:
        lines_parsed = 1
        parsed = m.groupdict()  # type: dict        # make checker happy
    else:
        m = INFO_PATTERN.match(lines[1])
        lines_parsed = 2
        if m is None:
            m = INFO_PATTERN3.match(lines[1])
            lines_parsed = 2
            if m is None:
                raise FileInfoFormatException(lines)

        parsed = m.groupdict()
        filename = lines[0]
        parsed["filename"] = filename
    # parse
    parsed["filename"] = parsed["filename"].strip()
    parsed["orig_size"] = int(parsed["orig_size"])
    parsed["compressed_size"] = int(parsed["compressed_size"])
    parsed["mod_time"] = datetime.datetime.strptime(parsed["mod_time"], "%y-%m-%d %H:%M:%S")

    if parsed["attr"][8] == "1":
        parsed["password"] = True

    return parsed, lines_parsed


HEADER_PATTERN = re.compile(r"ARJ32 v [\d.]+, Copyright \(c\) \d{4}-\d{4}, ARJ Software Russia.")

FILEPATH_PATTERN = re.compile("Processing archive: (?P<filepath>.*)")
CANTFIND_PATTERN = re.compile("Can't find (?P<filepath>.*)")

NOT_ARJ_PATTERN = re.compile("(?P<filepath>.*) is not an ARJ archive")

TIMES_PATTERN = re.compile("Archive created: (?P<create_time>.*), modified: (?P<mod_time>.*)")

FILES_HEADER = [
    "Filename       Original Compressed Ratio DateTime modified Attributes/GUA BPMGS",
    "------------ ---------- ---------- ----- ----------------- -------------- -----",
]
FILES_HEADER_LEN = len(FILES_HEADER)

FILE_LIST_FOOTER = "------------ ---------- ---------- -----"

FILE_LIST_TOTALS_PATTERN = re.compile(r"\s*(?P<count>.\d*) files.*")


INFO_PATTERN = re.compile(
    r"\s+(?P<orig_size>.\d+)\s+(?P<compressed_size>.\d+)\s+(?P<ratio>.[\d.]+)\s+"
    r"(?P<mod_time>.+) (?P<crc32>[0-9A-F]{8}) (?P<attr>.*)"
)
INFO_PATTERN3 = re.compile(
    r"\s+(?P<orig_size>.\d+)\s+(?P<compressed_size>.\d+)\s+(?P<ratio>.[\d.]+)\s+"
    r"(?P<mod_time>.{17}) (?P<attr>[\-tsrwx\s]{14})\s*(?P<bpmgs>.*)"
)
INFO_PATTERN2 = re.compile(
    r"(?P<filename>\S*)\s*(?P<orig_size>\d*)\s*(?P<compressed_size>.\d*)\s*(?P<ratio>."
    r"[\d.]*)\s*(?P<mod_time>.*) (?P<crc32>[0-9A-F]{8}) (?P<attr>.*)"
)
INFO_PATTERN4 = re.compile(
    r"(?P<filename>.+)\s+(?P<orig_size>\d+)\s+(?P<compressed_size>\d+)\s+(?P<ratio>."
    r"[\d.]+)\s+(?P<mod_time>.{17}) (?P<attr>[\-tsrwx\s]{14})\s*(?P<bpmgs>.*)"
)


class Unzip(object):
    """ARJ unzipping class."""

    def __init__(self, filepath, password=None):
        """Create a new ARJ unzipper for the given filepath."""
        self.filepath = filepath
        self.password = password
        self.fileinfo = []

        # ARJ automatically adds on '.ARJ' extension for files without ext
        # get around this by adding  a period to file name

        filename = os.path.basename(filepath)

        if "." not in filename:
            self.filepath += "."

        stdout, _ = subprocess.Popen(  # noqa: S603
            ["arj", "l", self.filepath],  # noqa: S607
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()
        stdout_lines = stdout.decode("utf-8", errors="backslashreplace").splitlines()

        if not HEADER_PATTERN.match(stdout_lines[0]):
            raise ArjHeaderException(filepath, stdout_lines)

        stdout_lines_to_process = stdout_lines[2:]

        m = CANTFIND_PATTERN.match(stdout_lines_to_process[1])
        if m is not None:
            raise NotFoundArchive(filepath, stdout_lines_to_process)

        m = FILEPATH_PATTERN.match(stdout_lines_to_process[0])
        if m is None:
            raise ArjFilePathException(filepath, stdout_lines_to_process)

        stdout_lines_to_process.pop(0)

        m = NOT_ARJ_PATTERN.match(stdout_lines_to_process[0])
        if m is not None:
            raise NotSupportedArchive(filepath, stdout_lines_to_process)

        m = TIMES_PATTERN.match(stdout_lines_to_process[0])
        if m is None:
            raise ArjTimesException(filepath, stdout_lines_to_process)

        self.create_time = m.group("create_time")
        self.mod_time = m.group("mod_time")
        stdout_lines_to_process.pop(0)

        if stdout_lines_to_process[:FILES_HEADER_LEN] != FILES_HEADER:
            raise ArjHeaderException(filepath, stdout_lines_to_process)

        for _ in range(FILES_HEADER_LEN):
            stdout_lines_to_process.pop(0)

        while stdout_lines_to_process[0] != FILE_LIST_FOOTER:
            info, lines_parsed = parse_info(stdout_lines_to_process[0:2])

            self.fileinfo.append(info)
            for _ in range(lines_parsed):
                stdout_lines_to_process.pop(0)

        stdout_lines_to_process.pop(0)
        # now file_list_totals

        m = FILE_LIST_TOTALS_PATTERN.match(stdout_lines_to_process[0])

        if m is None:
            raise FileCountFormatException(filepath, stdout_lines_to_process)

        total_count = int(m.group("count"))
        extracted_files = len(self.fileinfo)
        if total_count != extracted_files:
            raise FileCountMisMatchException(filepath, extracted_files, total_count, self.fileinfo)
        # all good!

    def _extract(self, dest_dir: str, filename: str = None) -> str | list[str]:
        """Extract content for the supplied filename and returns the path to the extracted file."""
        args = ["arj"]
        if self.password:
            args.append("-g%s" % self.password)
        args.extend(["e", "-y", self.filepath, dest_dir])
        if filename:
            args.append(filename)

        p = subprocess.Popen(  # noqa: S603, S607 # noqa: S603 B607
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, _ = p.communicate()
        if stdout.find(b"File is password encrypted, Skipped") != -1:
            # found a file that is password protected, but no password was given
            raise PasswordProtectedFile(filename)
        if filename:
            # try and read back the contents
            path = os.path.join(dest_dir, filename)
            if not os.path.exists(path):
                raise IncorrectPasswordException(self.filepath, self.password)
            return path
        else:
            paths = []
            for f in self.fileinfo:
                name = f["filename"]
                path = os.path.join(dest_dir, name)
                paths.append(path)
                if not os.path.exists(path):
                    raise IncorrectPasswordException(self.filepath, self.password)
            return paths

    def extract(self, dest_dir: str, filename: str) -> str:
        """Extract the contents of a single child file from an arj file and return the path to the extracted file."""
        return self._extract(dest_dir, filename)

    def extract_all(self, dest_dir: str) -> list[str]:
        """Extract the contents of all child object in an arj archive and return the path to all extracted files."""
        return self._extract(dest_dir)

    def __len__(self):
        """Return how many file entries in this ARJ file."""
        return len(self.fileinfo)
