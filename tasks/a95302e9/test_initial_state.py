# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student starts working on the task.
#
# IMPORTANT:  These tests purposely do NOT touch any of the paths that the
#             student is expected to create / modify (e.g. anything under
#             /home/user/bin or the log file).  We only assert the presence
#             of the source directory and source scripts that the exercise
#             depends on.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
DEV_DIR = HOME / "dev"
DEV_BIN_DIR = DEV_DIR / "bin"
RUN_BACKUP = DEV_BIN_DIR / "run_backup.sh"
CHECK_STATUS = DEV_BIN_DIR / "check_status.sh"

def _assert_is_executable_file(path: Path) -> None:
    """
    Helper that asserts `path` exists, is a regular file,
    and has at least one executable bit set.
    """
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file, but it is not."
    mode = path.stat().st_mode
    assert mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH), (
        f"File {path} is not marked as executable."
    )

def test_dev_directory_structure_exists():
    """
    The source directory hierarchy must already be in place.
    """
    assert DEV_DIR.exists(), f"Directory {DEV_DIR} is missing."
    assert DEV_DIR.is_dir(), f"Expected {DEV_DIR} to be a directory."

    assert DEV_BIN_DIR.exists(), f"Directory {DEV_BIN_DIR} is missing."
    assert DEV_BIN_DIR.is_dir(), f"Expected {DEV_BIN_DIR} to be a directory."

def test_required_source_scripts_present_and_executable():
    """
    Both source scripts must be present and executable in /home/user/dev/bin.
    """
    _assert_is_executable_file(RUN_BACKUP)
    _assert_is_executable_file(CHECK_STATUS)