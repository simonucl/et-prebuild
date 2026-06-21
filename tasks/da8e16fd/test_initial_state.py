# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student runs any commands for the “backup integrity
# check” task.
#
# The tests purposefully **do not** look for the artefacts that the
# student must create (e.g. /home/user/integrity_checks or the
# daily_check.log); instead they verify that the environment provided by
# the testing harness is exactly as described in the assignment.
#
# Only the Python standard library and pytest are used.

import hashlib
from pathlib import Path

import pytest


ROOT = Path("/home/user")
BACKUP_DIR = ROOT / "backups" / "daily"
DB_FILE = BACKUP_DIR / "sample.db"
MD5_FILE = BACKUP_DIR / "sample.db.md5"
INTEGRITY_DIR = ROOT / "integrity_checks"          # must NOT exist yet
LOG_FILE = INTEGRITY_DIR / "daily_check.log"

EXPECTED_MD5 = "d41d8cd98f00b204e9800998ecf8427e"
EXPECTED_MD5_LINE = f"{EXPECTED_MD5}  sample.db\n"


def test_backup_directory_exists_and_is_directory():
    """The directory /home/user/backups/daily must exist and be a directory."""
    assert BACKUP_DIR.exists(), (
        f"Required directory {BACKUP_DIR} is missing."
    )
    assert BACKUP_DIR.is_dir(), (
        f"{BACKUP_DIR} exists but is not a directory."
    )


def test_sample_db_file_exists_and_is_empty():
    """sample.db must exist, be a regular file, and have zero bytes."""
    assert DB_FILE.exists(), f"Missing backup file {DB_FILE}."
    assert DB_FILE.is_file(), f"{DB_FILE} exists but is not a regular file."
    size = DB_FILE.stat().st_size
    assert size == 0, (
        f"{DB_FILE} should be zero-byte file, found {size} bytes."
    )


def test_sample_db_md5_checksum_matches_expected():
    """The MD5 of sample.db must match the value in the task description."""
    # Calculate md5 of the (empty) file ourselves.
    md5_calculated = hashlib.md5(DB_FILE.read_bytes()).hexdigest()
    assert md5_calculated == EXPECTED_MD5, (
        f"MD5 of {DB_FILE} should be {EXPECTED_MD5}, found {md5_calculated}."
    )


def test_md5_sidecar_file_content():
    """
    /home/user/backups/daily/sample.db.md5 must exist and contain the single
    line with the correct checksum followed by two spaces and the filename,
    terminating in a newline.
    """
    assert MD5_FILE.exists(), f"Missing checksum file {MD5_FILE}."
    assert MD5_FILE.is_file(), f"{MD5_FILE} exists but is not a regular file."
    content = MD5_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_MD5_LINE, (
        f"Content of {MD5_FILE!s} is incorrect.\n"
        f"Expected exactly: {EXPECTED_MD5_LINE!r}\n"
        f"Found:           {content!r}"
    )


def test_integrity_checks_directory_absent():
    """
    Before the student acts, /home/user/integrity_checks *must not* exist.
    Its presence would indicate the environment is already modified.
    """
    assert not INTEGRITY_DIR.exists(), (
        f"Directory {INTEGRITY_DIR} already exists but should not be present "
        f"before the student runs their commands."
    )
    # If the directory is absent, the log file cannot exist either.
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} already exists but should not be present "
        f"before the student runs their commands."
    )