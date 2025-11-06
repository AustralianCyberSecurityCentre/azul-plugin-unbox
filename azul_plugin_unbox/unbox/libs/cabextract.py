"""Python wrapper for cabextract command-line tool."""

import os
import subprocess  # noqa: S404 # nosec B404

from azul_plugin_unbox.unbox.box_base import NotSupported


class CabExtractException(Exception):
    """Something failed during extraction."""

    def __init__(self, filename, msg):
        """Create a new exception for the given filename."""
        super().__init__(filename, msg)
        self.value = "Error in %s:%s" % (filename, msg)

    def __str__(self):
        """Return human-readable string of the exception."""
        return str(self.value)


class CabKeysError(Exception):
    """Error when parsing key/file metadata."""

    def __init__(self, filename, stdout):
        """Create a new exception for the given filename."""
        super().__init__(filename, stdout)
        self.value = "Error extracting keys in %s:%s" % (filename, stdout)

    def __str__(self):
        """Return human-readable string of the exception."""
        return str(self.value)


class CabExtract(object):
    """Uses CabExtract program to list and extract the items from a cab file."""

    def __init__(self, filepath):
        """Create a new extractor for the given .CAB filepath.

        This method will attempt to list the files in the archive. If it
        is not a cab file it will fail and raise a CabExtractError.
        Otherwise it will populate a list witha the filenames ready for
        box.get_keys() to be called.
        """
        self.filepath = filepath
        self.fileDetails = dict()

        stdout_lines = []
        stderr_lines = []
        proc = subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
            ["cabextract", "-l", filepath],
            env={"TZ": "UTC"},
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()

        for line in stdout.decode("utf-8", errors="backslashreplace").splitlines():
            stdout_lines.append(line.rstrip())

        for line in stderr.decode("utf-8", errors="backslashreplace").splitlines():
            stderr_lines.append(line.rstrip())

        if stderr_lines:
            error = "\n".join(stderr_lines)
            if "no valid cabinets found" in error:
                raise NotSupported(error)
            raise CabExtractException(filepath, error)

        if stdout_lines:
            if stdout_lines[-1].startswith("All done, errors in"):
                raise CabExtractException(filepath, "\n".join(stdout_lines))

        if len(stdout_lines) < 3:
            raise CabExtractException(filepath, stdout_lines)

        # has been a sucess
        for line in stdout_lines[3:-2]:
            split = line.split("|")

            # in case of file names with '|'
            if len(split) > 3:
                raise CabKeysError(filepath, stdout_lines)

            self.fileDetails[split[2].lstrip()] = split[1].lstrip()

    def extract_all(self, dest_dir: str):
        """Extract file's data from cab with file name (key)."""
        stdout_lines = []
        stderr_lines = []
        proc = subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
            ["cabextract", "-d", dest_dir, self.filepath],
            env={"TZ": "UTC"},
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()

        for line in stdout.decode("utf-8", errors="backslashreplace").splitlines():
            stdout_lines.append(line.rstrip())

        for line in stderr.decode("utf-8", errors="backslashreplace").splitlines():
            stderr_lines.append(line.rstrip())

        if stderr_lines:
            raise CabExtractException(self.filepath, "\n".join(stderr_lines))

        if stdout_lines:
            if stdout_lines[-1].startswith("All done, errors in"):
                raise CabExtractException(self.filepath, "\n".join(stdout_lines))

        for file_name in self.fileDetails.keys():
            child_path = os.path.join(dest_dir, file_name)
            if not os.path.exists(child_path):
                raise CabExtractException(child_path, "Child file did not extract.")
