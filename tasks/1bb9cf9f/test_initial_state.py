# test_initial_state.py
#
# This pytest suite validates that the base operating-system / filesystem
# environment is ready *before* the student performs any of the actions
# described in the exercise.  It deliberately avoids checking for the
# presence (or absence) of any files or directories that the student is
# expected to create later, in accordance with the specification.
#
# Only generic, pre-existing conditions are verified.

import os
import subprocess
import tempfile
from pathlib import Path

import pytest


HOME = Path("/home/user")


def test_home_directory_exists():
    """
    The /home/user directory must already exist and be a directory.
    """
    assert HOME.exists(), "The directory /home/user does not exist."
    assert HOME.is_dir(), "/home/user exists but is not a directory."


def test_home_directory_is_writable(tmp_path_factory):
    """
    The current user must be able to create and remove a temporary file
    inside /home/user, proving basic write permissions.
    """
    try:
        tmp_file = tempfile.NamedTemporaryFile(dir=HOME, delete=False)
        tmp_file_path = Path(tmp_file.name)
        tmp_file.write(b"test")
        tmp_file.close()
    finally:
        # Whether the write succeeded or not, attempt to clean up so we
        # do not leave traces behind.
        if "tmp_file_path" in locals() and tmp_file_path.exists():
            tmp_file_path.unlink()

    # If we reached this point without exceptions the directory is writable.
    assert True, "/home/user does not appear to be writable."


def test_python3_is_available_and_version():
    """
    Ensure that `python3` is callable from the shell and that its
    version is at least 3.7 (arbitrary lower bound that comfortably
    covers the features needed for the assignment).
    """
    try:
        output = subprocess.check_output(["python3", "-c", "import sys, json; print(json.dumps(sys.version_info[:3]))"])
    except FileNotFoundError:
        pytest.fail("The `python3` executable is not available in PATH.")

    major, minor, micro = list(map(int, output.decode().strip("[] \n").split(",")))
    assert major == 3, f"Expected Python major version 3, got {major}."
    assert minor >= 7, f"Python >= 3.7 required, found 3.{minor}.{micro}."


def test_uname_command_works():
    """
    The `uname -r` command should return a non-empty string, proving basic
    availability of core utilities needed later.
    """
    kernel_version = subprocess.check_output(["uname", "-r"], text=True).strip()
    assert kernel_version, "The command `uname -r` returned an empty string."