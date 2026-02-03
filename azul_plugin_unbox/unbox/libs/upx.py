"""UPX unpacker using command-line tool."""

import io
import os
import re
import subprocess  # noqa: S404 # nosec B404

UPX_EXE = "upx"
# ~1MB max buffer size
MAX_BUFFER_BYTES_SIZE = 1000000


class UpxError(Exception):
    """Base exception for UPX issues."""

    def __init__(self, msg, stderr="", stdout=""):
        """Create a new exception, optionally with the tool's stdout/stderr."""
        super().__init__(msg, stderr, stdout)
        if stdout:
            msg += "\n---stdout---\n%s" % stdout
        if stderr:
            msg += "\n---stderr---\n%s" % stderr
        self.value = msg

    def __str__(self):
        """Human-readable string of exception details."""
        return str(self.value)


class UpxExecutionError(UpxError):
    """Unable to run upx command."""


class UpxRaisedAnError(UpxError):
    """Upx command tool returned an error."""


class NotPackedException(UpxError):
    """Exceutable was not UPX packed."""

    def __init__(self):
        """Create a new exception."""
        UpxError.__init__(self, "not packed by UPX")


class CantUnpackException(UpxError):
    """Error encountered when unpacking."""


class ModifiedHackedProtectedException(UpxError):
    """Upx packing has been modified in some way."""


class NoDataDecompressedError(UpxError):
    """Missing output from upx tool."""

    def __init__(self):
        """Create a new exception."""
        UpxError.__init__(self, "No data was written by the upx.exe")


class NoOutfileFoundError(UpxError):
    """Missing output from upx tool."""

    def __init__(self):
        """Create a new exception."""
        UpxError.__init__(self, "No outfile found")


class CouldntConfirmUnpackError(UpxError):
    """Unknown if upx unpacked correctly."""


def version(file_path: str):
    """If "is upx" returns upx version string, else returns None."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"UPX File path must be an absolute path to file '{file_path}' does not exist.")

    half_buffer = MAX_BUFFER_BYTES_SIZE // 2
    with io.open(file_path, "rb") as s:
        br = io.BufferedReader(s)
        buffer = br.read(half_buffer)

        # If there aren't event 8 bytes, no version will exist
        if len(buffer) < 8:
            return None

        # executable magic headers
        if buffer[:2] != b"MZ" and buffer[:4] != b"\x7fELF" and buffer[:4] != b"\xca\xfe\xba\xbe":
            return None

        # Searches through upx file looking for the version number acquires X bytes at a time.
        # Assumes half of the buffer is longer than any potential matches.
        # This mean if the version number lands in the middle of the buffer read it will still be found.
        while buffer:
            buffer += br.read(half_buffer)
            # search for upx header
            m = re.search(b"([0-9].[0-9]{2})\x00UPX!", buffer)
            if m:
                return m.group(1)

            # try another regex for versions UPX 1.07
            m = re.search(b"\\$Id: UPX ([0-9]\\.[0-9]{2}) Copyright", buffer)
            if m:
                return m.group(1)

            # Drop first half of the buffer.
            buffer = buffer[half_buffer:]

        return None


def unpack(src_path: str, dest_path: str):
    """Use upx to unpack the supplied filepath, from source to destination.

    Any error condition will be raised as an exception.
    """
    # build args for upx execution
    args = [UPX_EXE, "-d", src_path, f"-o{dest_path}"]

    stdout = stderr = b""
    try:
        p = subprocess.Popen(  # noqa: S603, S607 # nosec B603 B607
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = p.communicate()
    except Exception as err:
        msg = "failed to execute upx - %s - %s" % (err, args)
        raise UpxExecutionError(msg, stderr, stdout) from err

    if re.search(b"NotPackedException", stderr):
        raise NotPackedException()

    if re.search(b"modified/hacked/protected", stderr):
        raise ModifiedHackedProtectedException("hacked - %s" % stderr)

    if re.search(b"CantUnpackException", stderr):
        msg = stderr.split(b"CantUnpackException: ")[-1]
        raise CantUnpackException(msg.decode("utf-8", errors="replace"))

    # see if we had any stderr output
    if stderr:
        raise UpxRaisedAnError("output in stderr", stderr=stderr)

    # confirm that we unpacked 1 file
    if b"Unpacked 1 file." not in stdout:
        msg = "Couldn't confirm 'Unpacked 1 file.' message"
        raise CouldntConfirmUnpackError(msg, stderr, stdout)

    if not os.path.exists(dest_path):
        raise NoOutfileFoundError()

    # Ensure the file isn't 0bytes.
    if not os.path.getsize(dest_path):
        raise NoDataDecompressedError()
