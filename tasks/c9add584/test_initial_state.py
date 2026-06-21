# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating
# system / filesystem *before* the student performs any action for the
# “weekly_backup.sha256sum” task.
#
# Truth-source (from the exercise description):
#   • /home/user/backups            — must exist and be a directory.
#   • /home/user/backups/weekly_backup.img
#       – must exist, be a regular file, size 0 bytes,
#         and have the SHA-256 digest of an empty file:
#         e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
#   • /home/user/logs               — must *not* exist yet.
#   • /home/user/logs/weekly_backup.sha256sum
#       – must *not* exist yet.
#
# Only stdlib + pytest are used.  Each assertion provides a clear failure
# message so that any deviation from the expected initial state is obvious.

import hashlib
import os
from pathlib import Path

import pytest

BACKUPS_DIR = Path("/home/user/backups")
BACKUP_IMG = BACKUPS_DIR / "weekly_backup.img"
LOGS_DIR = Path("/home/user/logs")
LOG_FILE = LOGS_DIR / "weekly_backup.sha256sum"

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


def sha256_of_file(path: Path) -> str:
    """Return the SHA-256 hex digest of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_backups_directory_exists_and_is_directory():
    assert BACKUPS_DIR.exists(), (
        f"Expected directory {BACKUPS_DIR} to exist, "
        "but it is missing."
    )
    assert BACKUPS_DIR.is_dir(), (
        f"Expected {BACKUPS_DIR} to be a directory, "
        "but it is not."
    )


def test_backup_image_file_properties():
    assert BACKUP_IMG.exists(), (
        f"Expected backup image {BACKUP_IMG} to exist, but it is missing."
    )
    assert BACKUP_IMG.is_file(), (
        f"Expected {BACKUP_IMG} to be a regular file, but it is not."
    )

    size = BACKUP_IMG.stat().st_size
    assert size == 0, (
        f"Expected {BACKUP_IMG} to be 0 bytes, but it is {size} bytes."
    )

    digest = sha256_of_file(BACKUP_IMG)
    assert digest == EMPTY_SHA256, (
        f"SHA-256 digest mismatch for {BACKUP_IMG}.\n"
        f"  Expected: {EMPTY_SHA256}\n"
        f"  Found:    {digest}"
    )


def test_logs_directory_absent():
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should NOT exist before the task is performed."
    )


def test_sha256sum_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"File {LOG_FILE} should NOT exist before the task is performed."
    )