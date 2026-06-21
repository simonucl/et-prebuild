# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# *before* the student starts working on the “legacy_hello” exercise.
#
# Rules being enforced:
#   1. The legacy source file must already exist.
#   2. The build artefacts (executable and log file) must **not** exist yet.
#   3. The directory hierarchy must be present and correct.
#
# If any of these assumptions are violated, the tests will fail with a clear
# explanation so that the student (or the course tooling) can fix the
# environment before proceeding.

import os
from pathlib import Path

# Constants for full, absolute paths
HOME_DIR = Path("/home/user")
OLD_CODE_DIR = HOME_DIR / "old_code"
SRC_FILE = OLD_CODE_DIR / "legacy_hello.c"
EXECUTABLE = OLD_CODE_DIR / "legacy_hello"
LOG_FILE = OLD_CODE_DIR / "legacy_hello.log"

def test_old_code_directory_exists_and_is_dir():
    """
    The directory /home/user/old_code must already exist and be a directory.
    """
    assert OLD_CODE_DIR.exists(), (
        f"The directory {OLD_CODE_DIR} is missing. "
        "It must be present before any work begins."
    )
    assert OLD_CODE_DIR.is_dir(), (
        f"{OLD_CODE_DIR} exists but is not a directory."
    )

def test_legacy_hello_c_exists_and_is_regular_file():
    """
    The source file legacy_hello.c must exist and be a regular file.
    """
    assert SRC_FILE.exists(), (
        f"The source file {SRC_FILE} is missing. "
        "It must be present so that it can be compiled."
    )
    assert SRC_FILE.is_file(), (
        f"{SRC_FILE} exists but is not a regular file."
    )

def test_no_executable_yet():
    """
    Before the student compiles, the executable should NOT exist.
    """
    assert not EXECUTABLE.exists(), (
        f"The executable {EXECUTABLE} already exists, "
        "but it should not be present before compilation."
    )

def test_no_log_file_yet():
    """
    Before the student runs the program, the log file should NOT exist.
    """
    assert not LOG_FILE.exists(), (
        f"The log file {LOG_FILE} already exists, "
        "but it should not be present before the program is run."
    )