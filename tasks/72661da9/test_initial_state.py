# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# before the student performs any action.
#
# It checks that:
#   1. /home/user/admin/ exists and is a directory with 0755 perms.
#   2. /home/user/admin/user_accounts.txt exists, is a regular file,
#      has 0644 perms, contains exactly the 4-byte string b'test',
#      and its SHA-256 digest is
#      9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
#
# NOTE:  This file purposely does **not** test for the presence or
#        correctness of /home/user/admin/checksums.log, because that
#        file is the *output* students are expected to create.

import os
import stat
import hashlib
import pytest

ADMIN_DIR = "/home/user/admin"
ACCOUNTS_FILE = "/home/user/admin/user_accounts.txt"
EXPECTED_DIR_MODE = 0o755
EXPECTED_FILE_MODE = 0o644
EXPECTED_FILE_CONTENT = b"test"
EXPECTED_SHA256 = (
    "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
)


def _get_mode(path):
    """Return the permission bits of `path` as an int, e.g. 0o755."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_admin_directory_exists_and_permissions():
    assert os.path.isdir(
        ADMIN_DIR
    ), f"Required directory {ADMIN_DIR!r} does not exist or is not a directory."
    mode = _get_mode(ADMIN_DIR)
    assert (
        mode == EXPECTED_DIR_MODE
    ), f"{ADMIN_DIR!r} permissions are {oct(mode)}, expected {oct(EXPECTED_DIR_MODE)}."


def test_user_accounts_file_exists_and_permissions():
    assert os.path.isfile(
        ACCOUNTS_FILE
    ), f"Required file {ACCOUNTS_FILE!r} does not exist or is not a regular file."
    mode = _get_mode(ACCOUNTS_FILE)
    assert (
        mode == EXPECTED_FILE_MODE
    ), f"{ACCOUNTS_FILE!r} permissions are {oct(mode)}, expected {oct(EXPECTED_FILE_MODE)}."


def test_user_accounts_file_content_and_checksum():
    with open(ACCOUNTS_FILE, "rb") as fh:
        data = fh.read()

    assert (
        data == EXPECTED_FILE_CONTENT
    ), f"{ACCOUNTS_FILE!r} content mismatch. Expected 4 bytes b'test'."

    sha256 = hashlib.sha256(data).hexdigest()
    assert (
        sha256 == EXPECTED_SHA256
    ), f"{ACCOUNTS_FILE!r} SHA-256 digest is {sha256}, expected {EXPECTED_SHA256}."