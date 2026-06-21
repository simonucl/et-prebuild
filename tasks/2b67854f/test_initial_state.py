# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system /
# filesystem before the student begins work on the “firewall change-bundle”
# exercise.  The tests assert that none of the artefacts the student is
# supposed to create already exist.  If any of them are found, the tests will
# fail with a clear, actionable message.
#
# Do *not* modify these tests.

import os
import stat
import pytest

HOME_DIR = "/home/user"
LOG_DIR = os.path.join(HOME_DIR, "firewall_logs")
LOG_FILE = os.path.join(LOG_DIR, "firewall_commands.log")
SCRIPT_FILE = os.path.join(HOME_DIR, "firewall_setup.sh")


def _exists(path):
    """Return True if *path* exists in the filesystem."""
    return os.path.exists(path)


def _is_executable(path):
    """Return True if *path* is executable by the owner."""
    if not _exists(path):
        return False
    mode = os.stat(path).st_mode
    return bool(mode & stat.S_IXUSR)


def test_home_directory_present():
    """Sanity-check that /home/user itself exists."""
    assert os.path.isdir(HOME_DIR), (
        f"Expected home directory {HOME_DIR!r} to exist. "
        "The test environment looks broken."
    )


def test_firewall_logs_directory_absent():
    """
    The directory /home/user/firewall_logs should NOT exist before the student
    runs their solution.
    """
    assert not _exists(LOG_DIR), (
        f"Directory {LOG_DIR!r} already exists. "
        "The student is expected to create it, so the starting state must be clean."
    )


def test_firewall_commands_log_absent():
    """
    The file /home/user/firewall_logs/firewall_commands.log should NOT exist
    before the student runs their solution.
    """
    assert not _exists(LOG_FILE), (
        f"File {LOG_FILE!r} already exists. "
        "The student must create this file; it should not be present beforehand."
    )


def test_firewall_setup_script_absent_or_not_executable():
    """
    The script /home/user/firewall_setup.sh should either not exist or, if it
    does, must *not* be executable yet.  The student is responsible for
    creating the script and making it executable.
    """
    if not _exists(SCRIPT_FILE):
        # Ideal situation: file is completely absent.
        return

    # If it does exist, ensure it is not yet executable.
    assert not _is_executable(SCRIPT_FILE), (
        f"File {SCRIPT_FILE!r} is already present and executable. "
        "The student must create and chmod this script themselves."
    )