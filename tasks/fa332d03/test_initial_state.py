# test_initial_state.py
#
# Pytest test-suite that validates the **initial** filesystem state
# before the student performs any action for the “January 2022
# PostgreSQL backup archiving” task.
#
# The tests ensure that:
#   • The source directory /home/user/db_backups exists.
#   • The expected SQL dump files from the task description are present.
#   • No archive or log files have been created yet.
#
# All paths are absolute, and each assertion provides a clear error
# message so the student instantly knows what is missing or unexpected.

import os
import pytest

DB_BACKUP_DIR = "/home/user/db_backups"
ARCHIVE_DIR = "/home/user/backup_archives"
JAN_FILES = [
    "/home/user/db_backups/backup_20220115.sql",
    "/home/user/db_backups/backup_20220120.sql",
]
FEB_FILES = [
    "/home/user/db_backups/backup_20220201.sql",
    "/home/user/db_backups/backup_20220210.sql",
]
ARCHIVE_FILE = "/home/user/backup_archives/202201_backups.tgz"
LOG_FILE = "/home/user/backup_archives/202201_backups.log"


def test_db_backup_directory_exists():
    assert os.path.isdir(DB_BACKUP_DIR), (
        f"Expected directory {DB_BACKUP_DIR!r} to exist. "
        "Create it or ensure the path is correct."
    )


@pytest.mark.parametrize("file_path", JAN_FILES + FEB_FILES)
def test_expected_sql_dumps_exist(file_path):
    assert os.path.isfile(file_path), (
        f"Expected SQL dump {file_path!r} to exist in the initial state. "
        "Make sure the fixture data are in place."
    )


def test_no_archive_or_log_yet():
    """Verify that the student has not yet created the target files."""
    if os.path.exists(ARCHIVE_FILE):
        pytest.fail(
            f"Archive {ARCHIVE_FILE!r} already exists before the task begins. "
            "The test should start with a clean state."
        )
    if os.path.exists(LOG_FILE):
        pytest.fail(
            f"Log file {LOG_FILE!r} already exists before the task begins. "
            "The test should start with a clean state."
        )