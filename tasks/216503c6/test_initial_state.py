# test_initial_state.py
#
# Pytest suite that verifies the initial state of the operating system
# BEFORE the student runs any commands.  It checks only for the assets
# that must already be present and intentionally avoids touching any
# files that will be produced later (e.g., checksum.log).

import os
import hashlib
import pytest


BACKUP_DIR = "/home/user/backups"
BACKUP_FILE = os.path.join(BACKUP_DIR, "project_backup.tar.gz")
EXPECTED_CONTENT = b"hello"
EXPECTED_SHA256 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_backup_directory_exists():
    """
    The directory /home/user/backups must exist and be a directory.
    """
    assert os.path.exists(
        BACKUP_DIR
    ), f"Required directory '{BACKUP_DIR}' is missing."
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Expected '{BACKUP_DIR}' to be a directory, but something else is present."


def test_backup_file_exists_and_is_regular_file():
    """
    The backup file must exist and be a regular file.
    """
    assert os.path.exists(
        BACKUP_FILE
    ), f"Required file '{BACKUP_FILE}' is missing."
    assert os.path.isfile(
        BACKUP_FILE
    ), f"Expected '{BACKUP_FILE}' to be a regular file, but it is not."


def test_backup_file_contents_and_checksum():
    """
    The backup file must contain exactly the bytes `hello` and therefore
    have the known SHA-256 digest.
    """
    with open(BACKUP_FILE, "rb") as f:
        data = f.read()

    # Verify exact content
    assert (
        data == EXPECTED_CONTENT
    ), f"'{BACKUP_FILE}' does not contain the expected bytes. " \
       f"Expected: {EXPECTED_CONTENT!r}, Found: {data!r}"

    # Verify SHA-256 checksum
    digest = hashlib.sha256(data).hexdigest()
    assert (
        digest == EXPECTED_SHA256
    ), f"SHA-256 digest mismatch for '{BACKUP_FILE}'. " \
       f"Expected: {EXPECTED_SHA256}, Found: {digest}"