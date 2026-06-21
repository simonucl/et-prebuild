# test_initial_state.py
#
# Pytest suite that validates the machine **before** the student performs the task.
# It asserts that:
#   1. The directory /home/user/config_audit already exists.
#   2. The file  /home/user/config_audit/first_snapshot.log does NOT yet exist.
#
# If either expectation is violated, the test fails with a clear, actionable message.
#
# Only stdlib and pytest are used.

import os
import stat
import pwd
import pytest
from pathlib import Path

CONFIG_AUDIT_DIR = Path("/home/user/config_audit")
SNAPSHOT_LOG = CONFIG_AUDIT_DIR / "first_snapshot.log"


def _mode_str(path: Path) -> str:
    """
    Return an octal string representation of a file's mode (e.g., '0o755').
    """
    return oct(path.stat().st_mode & 0o777)


def _owner_name(path: Path) -> str:
    """
    Return the username of the file's owner.
    """
    return pwd.getpwuid(path.stat().st_uid).pw_name


def test_directory_exists_and_is_directory():
    """
    The parent directory /home/user/config_audit must already exist and be a directory
    so the student can create the snapshot file inside it.
    """
    assert CONFIG_AUDIT_DIR.exists(), (
        f"Expected directory {CONFIG_AUDIT_DIR} to pre-exist, "
        "but it is missing. Create the directory before proceeding."
    )
    assert CONFIG_AUDIT_DIR.is_dir(), (
        f"Expected {CONFIG_AUDIT_DIR} to be a directory, "
        "but it exists as some other file type."
    )


def test_directory_is_writable_by_user():
    """
    Ensure the directory is owned by the current user and writable,
    so the student can create files inside it without elevated privileges.
    """
    current_uid = os.getuid()
    dir_stat = CONFIG_AUDIT_DIR.stat()
    assert dir_stat.st_uid == current_uid, (
        f"Directory {CONFIG_AUDIT_DIR} is owned by '{_owner_name(CONFIG_AUDIT_DIR)}', "
        "but it should be owned by the current user to allow file creation."
    )
    assert bool(dir_stat.st_mode & stat.S_IWUSR), (
        f"Directory {CONFIG_AUDIT_DIR} is not writable by its owner "
        f"(mode is {_mode_str(CONFIG_AUDIT_DIR)}). Adjust permissions accordingly."
    )


def test_snapshot_log_absent_initially():
    """
    The log file must NOT exist yet. Its presence would indicate that the task has
    already been performed or that a residue from a previous run is present.
    """
    assert not SNAPSHOT_LOG.exists(), (
        f"File {SNAPSHOT_LOG} already exists, but the task requires creating it "
        "from scratch. Remove or rename the file before starting the exercise."
    )