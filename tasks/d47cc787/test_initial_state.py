# test_initial_state.py
#
# This pytest suite verifies the “clean-slate” conditions **before**
# the learner creates /home/user/disk_space_summary.txt.
#
# DO NOT EDIT.  These checks guarantee that the operating system is in the
# expected initial state so that subsequent tasks and grading logic work
# reliably.
#
# Requirements verified:
#   1. /home           must exist and be a directory.
#   2. /home/user      must exist and be a directory.
#   3. At least one immediate child directory must be present under /home
#      (otherwise the disk–usage report would be meaningless).
#   4. /home/user/disk_space_summary.txt must *not* yet exist.
#
# If any of these checks fail, the machine image is corrupted or the learner
# has already executed steps that should not have been performed yet.

import os
import stat
import pytest
from pathlib import Path


REPORT_PATH = Path("/home/user/disk_space_summary.txt")
HOME_DIR = Path("/home")
USER_HOME_DIR = HOME_DIR / "user"


def test_home_directory_exists():
    """Ensure /home exists and is a directory."""
    assert HOME_DIR.exists(), "/home does not exist; expected the home root directory to be present."
    assert HOME_DIR.is_dir(), "/home exists but is not a directory."


def test_user_home_directory_exists():
    """Ensure /home/user exists and is a directory."""
    assert USER_HOME_DIR.exists(), "/home/user does not exist; expected the primary user’s home directory."
    assert USER_HOME_DIR.is_dir(), "/home/user exists but is not a directory."


def test_at_least_one_child_directory_under_home():
    """
    Verify that /home contains at least one immediate child directory
    (other than possibly 'user').  The forthcoming disk usage summary
    would be pointless otherwise.
    """
    child_dirs = [
        entry
        for entry in HOME_DIR.iterdir()
        if entry.is_dir() and not entry.is_symlink()
    ]
    assert child_dirs, (
        "/home contains no sub-directories. At least one directory is required "
        "to produce a meaningful disk-usage report."
    )


def test_report_file_absent_initially():
    """
    The disk space report must NOT exist before the learner runs the required
    command.  Its presence would indicate that the task was already attempted
    or the base image is wrong.
    """
    assert not REPORT_PATH.exists(), (
        f"Pre-existing file found: {REPORT_PATH}. "
        "The report should be created *after* completing the task, "
        "so it must be absent at the start."
    )