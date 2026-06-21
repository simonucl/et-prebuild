# test_initial_state.py
#
# Pytest suite to validate the PRE-EXISTING filesystem state *before* the
# student performs any action for the “accounts tidy-up” exercise.
#
# What we assert:
#   • Every real user directory already exists under /home/user/userdirs/.
#   • None of the symbolic links that the student must create later
#     (/home/user/accounts/active/*  and  /home/user/accounts/archived/*)
#     should exist yet.
#   • The report file /home/user/symlink_report.log must not exist yet.
#
# We deliberately do *not* require /home/user/accounts/, /active/, or
# /archived/ to exist now, because the task description states that the
# student must (re-)create them if they are missing.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")

USERDIRS = HOME / "userdirs"
REAL_USERS = ["alice", "bob", "carla", "dave", "erin"]

# Symbolic links that must NOT exist yet
ACTIVE_LINKS = ["alice", "carla", "erin"]
ARCHIVED_LINKS = ["bob", "dave"]

ACCOUNTS = HOME / "accounts"
ACTIVE_DIR = ACCOUNTS / "active"
ARCHIVED_DIR = ACCOUNTS / "archived"

REPORT_FILE = HOME / "symlink_report.log"


def _msg(path: Path, expectation: str) -> str:
    """Helper for consistent error messages."""
    return f"Expected {path} {expectation}, but it does not."


def test_real_user_directories_exist():
    """All real user directories must already be present."""
    assert USERDIRS.is_dir(), _msg(USERDIRS, "to exist as a directory")

    for user in REAL_USERS:
        user_path = USERDIRS / user
        assert user_path.is_dir(), _msg(user_path, "to exist as a directory")


@pytest.mark.parametrize("link_name", ACTIVE_LINKS)
def test_active_symlinks_absent_initially(link_name):
    """
    Symbolic links inside /home/user/accounts/active/ must not exist yet.
    They will be created by the student later.
    """
    link_path = ACTIVE_DIR / link_name
    assert not link_path.exists(), (
        f"{link_path} already exists. "
        "The directory should be empty (or absent) before the task starts."
    )


@pytest.mark.parametrize("link_name", ARCHIVED_LINKS)
def test_archived_symlinks_absent_initially(link_name):
    """
    Symbolic links inside /home/user/accounts/archived/ must not exist yet.
    They will be created by the student later.
    """
    link_path = ARCHIVED_DIR / link_name
    assert not link_path.exists(), (
        f"{link_path} already exists. "
        "The directory should be empty (or absent) before the task starts."
    )


def test_report_file_absent():
    """
    The log file /home/user/symlink_report.log should not exist before the task
    is carried out.
    """
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} should not exist yet; "
        "it must be generated only after all symlinks are in place."
    )