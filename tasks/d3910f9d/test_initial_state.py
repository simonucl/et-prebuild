# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state for the “database-backup cleanup” task **before** the student
# begins any work.
#
# The checks deliberately mirror the specification given to the student:
#
#   • Exactly three “*.sql” files must exist in /home/user/db_backups.
#   • No “*.gz” files (or any other files) may be present there yet.
#   • Each .sql file must have its expected byte size.
#   • The directory /home/user/backup_logs must *not* exist at all.
#
# If any of these assertions fail, the error messages should make it
# unambiguous what is wrong.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DB_BACKUPS = HOME / "db_backups"
BACKUP_LOGS = HOME / "backup_logs"

# Expected files and their exact byte sizes *before* compression.
EXPECTED_SQL_FILES = {
    "customers.sql": 68,
    "orders.sql": 71,
    "inventory.sql": 75,
}


@pytest.fixture(scope="module")
def db_backup_contents():
    """
    Return a mapping of {name: Path} for every item inside /home/user/db_backups
    and assert the directory itself exists.
    """
    assert DB_BACKUPS.is_dir(), (
        f"Required directory {DB_BACKUPS} does not exist. "
        "It must be present *before* the student starts."
    )
    return {p.name: p for p in DB_BACKUPS.iterdir()}


def test_only_expected_sql_files_present(db_backup_contents):
    """
    The /home/user/db_backups directory must contain *exactly* the three
    specified .sql files and nothing else.
    """
    present_names = sorted(db_backup_contents)
    expected_names = sorted(EXPECTED_SQL_FILES)

    # 1. File-set equality check.
    assert present_names == expected_names, (
        "Unexpected contents in /home/user/db_backups.\n"
        f"Expected only these files: {expected_names}\n"
        f"Found these files     : {present_names}"
    )

    # 2. Guarantee none of them are already compressed.
    gz_present = [name for name in present_names if name.endswith(".gz")]
    assert not gz_present, (
        "Found pre-existing .gz files inside /home/user/db_backups "
        f"which should **not** be there yet: {gz_present}"
    )


@pytest.mark.parametrize("filename,expected_size", EXPECTED_SQL_FILES.items())
def test_sql_file_sizes(db_backup_contents, filename, expected_size):
    """
    Each .sql file must match the exact byte size promised in the task
    description, ensuring the grader’s 'original size' baseline is correct.
    """
    path = db_backup_contents.get(filename)
    assert path is not None, f"File {filename} is missing from {DB_BACKUPS}"

    actual_size = path.stat().st_size
    assert actual_size == expected_size, (
        f"File size mismatch for {filename}: "
        f"expected {expected_size} bytes, got {actual_size} bytes."
    )


def test_backup_logs_directory_absent():
    """
    The /home/user/backup_logs directory (and thus the eventual
    compression_report.log file) must NOT exist before the student runs
    their solution.
    """
    assert not BACKUP_LOGS.exists(), (
        f"Directory {BACKUP_LOGS} already exists, but it should be created "
        "by the student as part of the task."
    )