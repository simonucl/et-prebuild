# test_initial_state.py
#
# This pytest suite verifies the initial state of the operating system / file
# system *before* the student attempts the task.  It intentionally does NOT
# check for the eventual output file
#     /home/user/reports/backup_integrity.log
# because that file should not exist yet and must be created by the student.
#
# Only stdlib + pytest are used.

import hashlib
from pathlib import Path

DATA_DIR = Path("/home/user/data")
REPORTS_DIR = Path("/home/user/reports")
BACKUP_FILE = DATA_DIR / "backup.tar.gz"

# The known SHA-256 digest of an empty file (0 bytes).
EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb924"
    "27ae41e4649b934ca495991b7852b855"
)


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing or is not a directory."
    )


def test_reports_directory_exists():
    assert REPORTS_DIR.is_dir(), (
        f"Required directory {REPORTS_DIR} is missing or is not a directory."
    )


def test_backup_file_exists():
    assert BACKUP_FILE.is_file(), (
        f"Required backup file {BACKUP_FILE} is missing."
    )


def test_backup_file_is_empty():
    size = BACKUP_FILE.stat().st_size
    assert size == 0, (
        f"Expected {BACKUP_FILE} to be 0 bytes, but it is {size} bytes."
    )


def test_backup_file_sha256_matches_empty_digest():
    sha256 = hashlib.sha256()
    with BACKUP_FILE.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha256.update(chunk)
    digest = sha256.hexdigest()
    assert digest == EMPTY_SHA256, (
        f"Expected SHA-256 digest of {BACKUP_FILE} to be\n"
        f"  {EMPTY_SHA256}\n"
        f"but got\n"
        f"  {digest}"
    )