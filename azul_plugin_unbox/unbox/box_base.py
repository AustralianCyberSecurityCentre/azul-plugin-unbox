"""Common logic for unboxing file formats."""

import inspect
import os
import shutil
from abc import ABC, abstractmethod
from typing import Any

import wrapt

from .box_child import BoxChild


class PasswordError(Exception):
    """Password was not successful."""


class NotSupported(Exception):
    """The format does not match what is supported by the box type."""


class Corrupted(Exception):
    """The file is corrupted."""


@wrapt.decorator
def guess_password(func, instance, args, kwargs):
    """Evaluate a list of passwords against the specified box instance."""
    # make sure decorator is only called on instance methods
    if instance is None or inspect.isclass(instance):
        raise RuntimeError("guess_password decorator can only be used on instance methods")

    # lets try it with our current password (or no password initially)
    try:
        return func(*args, **kwargs)
    except PasswordError:
        # either the box has a password when 'None' was passed in or the
        # password has somehow changed, lets find a correct one
        pass

    # don't know what the password is, lets guess
    for password in instance.passwords:
        try:
            # have a guess at the password from the list
            instance.password = password
            ret = func(*args, **kwargs)
            # no password error raised, so lets set the correct password
            instance.set_final_password(password)
            return ret
        except PasswordError:
            continue
    raise PasswordError("Failed to guess password")


class Box(ABC):
    """Box is the base class type interface for unboxes' types.

    When adding new unboxers it's expected that _extract and _get_all_children are overridden.

    Also when extracting metadata on either for the box itself or the extracted child objects it's expected you write
    methods with a specific prefix.

    For metadata on the parent: metadata_<expected-key>
    All text after the prefix is expected to be the key for accessing the metadata it emits.
    So the function "def metadata_compression(self)" will automatically be added to the box object when users
    use get_meta() and it will return {"compression": "<value>"}

    For metadata on a child object: child_metadata_ the functions still need to be defined but you are responsible
    For ensuring you append the metadata to each child with the associated key and metadata.
    """

    def __init__(
        self,
        src_filepath: str,
        target_dir: str,
        passwords: list[bytes | str] = None,
    ):
        """Create a new box format unpacker for the given filepath and place extracted content into the target_dir.

        tar_dir is the directory where all Box subclasses will write folder with extracted contents.
        """
        # These three should be set by child class, maybe pass through constructor?
        self._cached_meta = dict()

        # Should be set by overriding _get_all_children
        self._children = list()

        self.has_extracted = False

        # Everything below here is standard
        if passwords is None:
            passwords = []

        self.__passwords: list[str] = [self.__stringy_password(pwd) for pwd in passwords]
        self.__password_guess: str = None
        self.__password: str = None

        self._filepath = os.path.abspath(src_filepath)
        if not os.path.exists(self._filepath):
            raise OSError("File does not exist %s" % self._filepath)

        self._target_dir = os.path.abspath(target_dir)
        if not os.path.exists(self._target_dir):
            raise OSError("Directory does not exist %s" % self._target_dir)
        self._target_dir = os.path.join(self._target_dir, self.__class__.__name__)
        self.cleanup()

    @property
    def passwords(self) -> list[str]:
        """Get the list of potential passwords used for guessing the archives password."""
        return self.__passwords

    def add_password(self, password: str | bytes):
        """Method to allow child classes to append passwords."""
        self.__passwords.insert(0, self.__stringy_password(password))

    @property
    def password(self) -> str | None:
        """Password to use when attempting to unbox."""
        if self.__password is None:
            # don't have a password yet, so return the current guess
            return self.__stringy_password(self.__password_guess)
        return self.__stringy_password(self.__password)

    @password.setter
    def password(self, value: bytes | str):
        """Allows for setting of the password value."""
        self.__password_guess = self.__stringy_password(value)

    def set_final_password(self, value: bytes | str):
        """Set the password to the provided value once the correct password value has been found."""
        self.__password_guess = self.__stringy_password(value)
        self.__password = self.__stringy_password(value)

    @property
    def password_bytes(self) -> bytes | None:
        """Get the current password as a bytes string."""
        pwd = self.password
        if pwd:
            return pwd.encode("utf-8")
        return pwd

    @staticmethod
    def __stringy_password(password: str | bytes | None) -> str | None:
        """Ensure the password is a string even if provided as bytes."""
        if isinstance(password, bytes):
            try:
                password = password.decode("utf-8")
            except UnicodeDecodeError:
                password = str(password)
        return password

    @property
    def src_filepath(self):
        """Get a file path on disk to the box file."""
        return self._filepath

    @property
    def dest_filedir(self):
        """Get a path to the destination directory where child files are being extracted to."""
        return self._target_dir

    @guess_password
    def extract(self):
        """Method used to extract all contents of an archive by a child box class."""
        self._extract()
        self.has_extracted = True
        # fix permissions to remove any readonly files or folders
        for root, dirs, files in os.walk(self.dest_filedir):
            for name in files:
                fullpath = os.path.join(root, name)
                os.chmod(fullpath, 0o600)
            for name in dirs:
                fullpath = os.path.join(root, name)
                os.chmod(fullpath, 0o700)

    @abstractmethod
    def _extract(self):
        """Method to be overridden, the method must extract the archive to the dest_filedir."""
        raise NotImplementedError()

    @guess_password
    def get_children(self) -> list[BoxChild]:
        """Get all child objects for the extracted box."""
        # Ensure that if the archive hasn't been extracted yet, it is extracted now.
        if not self.has_extracted:
            self.extract()

        if len(self._children) == 0:
            self._children = self._get_all_children()
        return self._children

    @abstractmethod
    def _get_all_children(self) -> list[BoxChild]:
        raise NotImplementedError()

    @guess_password
    def get_meta(self) -> dict[str, Any]:
        """Return all of the parent box metadata in a dictionary."""
        # Ensure that if the archive hasn't been extracted yet, it is extracted now.
        if not self.has_extracted:
            self.extract()

        if len(self._cached_meta) == 0:
            self._cached_meta = self._get_full_meta()
        return self._cached_meta

    def _get_full_meta(self) -> dict[str, Any]:
        """Call any method that starts with 'metadata_' and add it to a dictionary in the form function name value.

        e.g function metadata_compression returns the value of "zip" dictionary looks like: {"compression": "zip"}
        Could have multiple or only a single value in the dictionary.
        """
        meta = dict()
        hdr = "metadata_"
        for method in dir(self):
            if method.startswith(hdr):
                method_handle = getattr(self, method, None)
                meta[method[len(hdr) :]] = method_handle()
        return meta

    def list_meta(self):
        """Return a list of all metatypes by getting the function names of all functions that start with _metadata."""
        return self.__get_meta("metadata_")

    def list_child_meta(self):
        """Get a list of all child metatypes by getting function names of functions that start with child_metadata_."""
        return self.__get_meta("child_metadata_")

    def __get_meta(self, method_prefix: str) -> list[str]:
        """Get all of the method names after the provided prefix.

        e.g class with methods
        def prefix_hello
        def prefix_why
        -> returns ["hello", "why"]
        """
        return [a[len(method_prefix) :] for a in dir(self) if a.startswith(method_prefix)]

    def cleanup(self):
        """Delete all files in the directory where archives expect to extract contents to."""
        if os.path.exists(self._target_dir):
            # raise errors if there are still some bad files around
            shutil.rmtree(self._target_dir)
        os.mkdir(self._target_dir)
