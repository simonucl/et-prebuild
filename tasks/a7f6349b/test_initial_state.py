# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
*before* the student carries out any actions.

Truth value (expected initial state):
1. The path /home/user exists.
2. /home/user is a writable directory by the current (non-root) user.
No other assumptions are made about the filesystem.
"""

import os
import errno
import pytest


HOME_PATH = "/home/user"


def is_writable(path: str) -> bool:
    """
    Return True if the current process can create a file in `path` without
    altering the filesystem.  Uses os.access with W_OK and, as a fallback,
    attempts to open a file descriptor with os.open in O_WRONLY|O_CREAT mode
    followed by an immediate close/unlink to avoid side effects.
    """
    if os.access(path, os.W_OK):
        return True

    testfile = os.path.join(path, ".pytest_write_test")
    try:
        fd = os.open(testfile, os.O_WRONLY | os.O_CREAT, 0o600)
        os.close(fd)
        os.unlink(testfile)
        return True
    except OSError as exc:
        if exc.errno in (errno.EACCES, errno.EROFS):
            return False
        # Any other error (e.g., ENOENT on parent) means the directory
        # is either missing or not writable—handled by the caller.
        return False


@pytest.fixture(scope="module")
def home_stat():
    """Stat information for /home/user, if it exists."""
    try:
        return os.stat(HOME_PATH)
    except FileNotFoundError:
        pytest.fail(
            f"Required directory '{HOME_PATH}' does not exist. "
            "Create it before running the setup script."
        )


def test_home_is_directory(home_stat):
    assert os.path.isdir(HOME_PATH), (
        f"Expected '{HOME_PATH}' to be a directory, "
        f"but it is not (mode: {oct(home_stat.st_mode)})"
    )


def test_home_is_writable():
    assert is_writable(HOME_PATH), (
        f"Directory '{HOME_PATH}' is not writable by the current user. "
        "Ensure proper permissions before proceeding."
    )