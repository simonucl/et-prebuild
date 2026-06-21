# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student performs any actions for the backup task.
#
# It checks that:
#   • /home/user/data/ exists and is a directory.
#   • /home/user/data/dump.sql exists and contains the exact
#     expected 33-byte content.
#   • The backup directory /home/user/db_backups/ does *not* yet
#     exist and therefore no backup-related files are present.
#
# If any of these assertions fail, the error messages should make
# it clear what is missing or unexpectedly present.
#
# Only Python’s standard library and pytest are used.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user").resolve()
DATA_DIR = HOME / "data"
DUMP_FILE = DATA_DIR / "dump.sql"
BACKUP_DIR = HOME / "db_backups"
BACKUP_ARCHIVE = BACKUP_DIR / "dump_backup.tar.gz"
BACKUP_LOG = BACKUP_DIR / "backup.log"

# Expected byte sequence of the initial dump file.
EXPECTED_DUMP_BYTES = bytes.fromhex(
    "54 68 69 73 20 69 73 20 61 20 73 61 6d 70 6c 65 20 "
    "50 6f 73 74 67 72 65 53 51 4c 20 64 75 6d 70 0a"
    .replace(" ", "")
)

def assert_path_is_dir(path: Path) -> None:
    assert path.exists(), f"Expected directory {path} to exist, but it does not."
    assert path.is_dir(), f"Expected {path} to be a directory, but it is not."
    # Ensure the directory is writable.
    mode = path.stat().st_mode
    assert bool(mode & stat.S_IWUSR), f"Directory {path} is not writable by the user."

def assert_path_is_file(path: Path) -> None:
    assert path.exists(), f"Expected file {path} to exist, but it does not."
    assert path.is_file(), f"Expected {path} to be a regular file, but it is not."


def test_data_directory_exists_and_writable():
    """
    The directory /home/user/data/ must exist and be writable.
    """
    assert_path_is_dir(DATA_DIR)


def test_dump_file_exists_and_has_expected_content():
    """
    The dump.sql file must exist and match the known 33-byte content.
    """
    assert_path_is_file(DUMP_FILE)

    dump_bytes = DUMP_FILE.read_bytes()
    expected_len = len(EXPECTED_DUMP_BYTES)
    assert len(dump_bytes) == expected_len, (
        f"{DUMP_FILE} has {len(dump_bytes)} bytes, expected {expected_len}."
    )
    assert dump_bytes == EXPECTED_DUMP_BYTES, (
        f"{DUMP_FILE} content does not match the expected initial dump content."
    )


def test_backup_directory_does_not_yet_exist():
    """
    No backup directory or related files should exist before the student runs their solution.
    """
    assert not BACKUP_DIR.exists(), (
        f"Backup directory {BACKUP_DIR} should NOT exist yet, but it does."
    )
    # If the directory exists, still check that no files are inside (defensive).
    if BACKUP_DIR.exists():
        assert not BACKUP_ARCHIVE.exists(), (
            f"Archive {BACKUP_ARCHIVE} should not exist before the task starts."
        )
        assert not BACKUP_LOG.exists(), (
            f"Log file {BACKUP_LOG} should not exist before the task starts."
        )