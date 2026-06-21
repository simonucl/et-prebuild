# test_initial_state.py
#
# This test-suite validates the *starting* filesystem state that must be
# present **before** the learner carries out the task described in the README.
#
# It asserts that:
#   1. The required source directories / files already exist.
#   2. None of the symbolic links the learner is supposed to create exist yet.
#   3. The audit log file does **not** exist yet.
#
# If any assertion fails, the accompanying message will explain what is missing
# or unexpectedly present.

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants: absolute paths used by the task
# --------------------------------------------------------------------------- #

# Directories that must already exist
REQUIRED_DIRS = [
    Path("/home/user/db_data/bigdata"),
    Path("/home/user/db_data/fastdata"),
    Path("/home/user/db_archives/2023_09_prod"),
    Path("/home/user/db_archives/2023_10_maint"),
]

# Regular files that must already exist
REQUIRED_FILES = [
    Path("/home/user/configs/new_config.sql"),
]

# Symbolic links that must *not* exist yet
SYMLINKS_TO_BE_CREATED = [
    Path("/home/user/current_db_data"),
    Path("/home/user/db_archives/latest"),
    Path("/home/user/query_conf_active.sql"),
]

# Log file that must *not* exist yet
AUDIT_LOG = Path("/home/user/symlink_audit.log")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _assert_is_directory(p: Path):
    assert p.exists(), f"Expected directory '{p}' to exist, but it does not."
    assert p.is_dir(), f"Expected '{p}' to be a directory, but it is not."


def _assert_is_regular_file(p: Path):
    assert p.exists(), f"Expected file '{p}' to exist, but it does not."
    assert p.is_file() and not p.is_symlink(), (
        f"Expected '{p}' to be a regular file, but it is not."
    )


def _assert_not_present(p: Path):
    assert not p.exists(), (
        f"'{p}' should NOT exist yet. "
        "The student will create this symbolic link or file during the task."
    )


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_required_directories_exist():
    """All source directories must already be present."""
    for d in REQUIRED_DIRS:
        _assert_is_directory(d)


def test_required_files_exist():
    """All source files must already be present as regular files."""
    for f in REQUIRED_FILES:
        _assert_is_regular_file(f)


def test_symlinks_do_not_exist_yet():
    """Symbolic links specified in the task must not exist before the task."""
    for link in SYMLINKS_TO_BE_CREATED:
        _assert_not_present(link)


def test_audit_log_does_not_exist_yet():
    """Audit log must not exist before the learner generates it."""
    _assert_not_present(AUDIT_LOG)