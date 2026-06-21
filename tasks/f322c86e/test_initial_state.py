# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the filesystem
before the student performs any actions for the backup-checksum task.

It checks that:
1. The weekly backup directory exists and is writable.
2. The full backup archive exists at the expected absolute path.
3. The archive is exactly 0 bytes (as specified in the task description).
4. The SHA-256 checksum of the empty archive matches the well-known
   digest for an empty file/string.

Nothing in this file checks for, or depends on, the presence (or absence)
of the output file `full_backup.sha256`, in accordance with the grading
rules that forbid testing output artefacts at this stage.
"""

import hashlib
import os
import stat

import pytest

# Absolute paths used throughout the tests
BACKUP_DIR = "/home/user/backup/weekly"
BACKUP_FILE = os.path.join(BACKUP_DIR, "full_backup.tar.gz")

# The SHA-256 digest for an empty file/string
EMPTY_FILE_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


def test_backup_directory_exists_and_writable():
    """
    The weekly backup directory must already exist and be writable by the
    current user so that the student can add the .sha256 file later.
    """
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Expected directory {BACKUP_DIR!r} to exist, but it is missing."
    # Check write permission
    assert os.access(
        BACKUP_DIR, os.W_OK
    ), f"Directory {BACKUP_DIR!r} exists but is not writable by the current user."


def test_full_backup_file_exists():
    """The full backup archive must already be present at the exact path."""
    assert os.path.isfile(
        BACKUP_FILE
    ), f"Expected backup file {BACKUP_FILE!r} to exist, but it is missing."


def test_full_backup_file_is_empty():
    """The provided backup file should be exactly 0 bytes as per the task."""
    size = os.path.getsize(BACKUP_FILE)
    assert (
        size == 0
    ), f"Backup file {BACKUP_FILE!r} should be 0 bytes, but its size is {size} bytes."


def test_full_backup_sha256_matches_empty_file_digest():
    """The SHA-256 hash of the empty backup file must match the known digest."""
    with open(BACKUP_FILE, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    assert (
        digest == EMPTY_FILE_SHA256
    ), (
        f"SHA-256 digest of {BACKUP_FILE!r} was {digest}, "
        f"but expected {EMPTY_FILE_SHA256} for an empty file."
    )