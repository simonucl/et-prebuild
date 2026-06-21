# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the filesystem
# before the student runs any commands for the “nightly SQL dump
# compression” task.
#
# These tests purposefully FAIL if required directories/files are
# missing **or** if the archive/log that the student must create
# already exist.  Clear assertion messages guide the student on
# what is wrong in the starting environment.
#
# Only stdlib + pytest are used, in accordance with the rules.

import os
import pytest

HOME = "/home/user"

# --- Paths that MUST exist -------------------------------------

REQUIRED_DIRS = [
    f"{HOME}/backups",
    f"{HOME}/backups/daily",
    f"{HOME}/archives",
    f"{HOME}/backup_logs",
]

REQUIRED_DUMP_FILES = [
    f"{HOME}/backups/daily/users.sql",
    f"{HOME}/backups/daily/orders.sql",
    f"{HOME}/backups/daily/products.sql",
]

# --- Paths that MUST *NOT* exist yet ---------------------------

ARCHIVE_PATH = f"{HOME}/archives/db_backup_2025-01-15.tar.gz"
LOG_PATH     = f"{HOME}/backup_logs/backup_log_2025-01-15.txt"


# ----------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------
def _assert_exists(path: str, is_dir: bool):
    if is_dir:
        assert os.path.isdir(path), (
            f"Required directory missing: {path}\n"
            "Create the directory with correct permissions before proceeding."
        )
    else:
        assert os.path.isfile(path), (
            f"Required file missing: {path}\n"
            "Ensure the SQL dump file exists and is readable."
        )


def _assert_not_exists(path: str):
    assert not os.path.exists(path), (
        f"{path} already exists.\n"
        "It should NOT be present before the task is performed.\n"
        "Remove or rename it, then re-run your solution."
    )


# ----------------------------------------------------------------
# Tests
# ----------------------------------------------------------------
@pytest.mark.parametrize("dir_path", REQUIRED_DIRS)
def test_required_directories_exist(dir_path):
    """All prerequisite directories must be present."""
    _assert_exists(dir_path, is_dir=True)


@pytest.mark.parametrize("file_path", REQUIRED_DUMP_FILES)
def test_required_dump_files_exist(file_path):
    """SQL dump files must be present before archiving."""
    _assert_exists(file_path, is_dir=False)


def test_archive_absent_initially():
    """The target .tar.gz archive must NOT exist yet."""
    _assert_not_exists(ARCHIVE_PATH)


def test_log_absent_initially():
    """The log file must NOT exist yet."""
    _assert_not_exists(LOG_PATH)