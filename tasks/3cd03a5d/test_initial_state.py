# test_initial_state.py
"""
Pytest suite that validates the pristine filesystem state **before** the student
runs any commands for the “backup integrity” task.

Checked truth:

1. /home/user/data/ exists and is a directory.
2. /home/user/data/backup.tar.gz exists, is a regular file, is exactly
   five bytes long, and contains the ASCII text “hello” with **no** trailing
   newline.
3. The SHA-256 digest of that file is
   2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

NOTE:
• We intentionally do NOT check the output directory (/home/user/reports)
  or any files that the student will create, per the grading-harness rules.
"""

import hashlib
import os
import stat
import pytest

DATA_DIR = "/home/user/data"
BACKUP_FILE = os.path.join(DATA_DIR, "backup.tar.gz")
EXPECTED_DIGEST = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
)
EXPECTED_CONTENT = b"hello"  # exactly five bytes, no trailing newline


def test_data_directory_exists_and_is_directory():
    assert os.path.exists(
        DATA_DIR
    ), f"Required directory {DATA_DIR!r} is missing."
    assert os.path.isdir(
        DATA_DIR
    ), f"{DATA_DIR!r} exists but is not a directory."


def test_backup_file_exists_and_is_regular_file():
    assert os.path.exists(
        BACKUP_FILE
    ), f"Required file {BACKUP_FILE!r} is missing."
    st = os.stat(BACKUP_FILE)
    assert stat.S_ISREG(
        st.st_mode
    ), f"{BACKUP_FILE!r} exists but is not a regular file."


def test_backup_file_size_and_content():
    size = os.path.getsize(BACKUP_FILE)
    assert (
        size == len(EXPECTED_CONTENT)
    ), f"{BACKUP_FILE!r} should be {len(EXPECTED_CONTENT)} bytes, found {size}."
    with open(BACKUP_FILE, "rb") as fp:
        data = fp.read()
    assert (
        data == EXPECTED_CONTENT
    ), f"{BACKUP_FILE!r} contents differ from the expected ASCII text 'hello'."


def test_backup_file_sha256_digest():
    sha256 = hashlib.sha256()
    with open(BACKUP_FILE, "rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            sha256.update(chunk)
    digest = sha256.hexdigest()
    assert (
        digest == EXPECTED_DIGEST
    ), f"SHA-256 digest for {BACKUP_FILE!r} is {digest}, expected {EXPECTED_DIGEST}."