# test_initial_state.py
#
# Pytest suite that validates the system state *before* the student carries
# out the API-key-rotation task.

import os
import stat
import pytest

CREDENTIALS_DIR = "/home/user/credentials"
USERS_CSV = os.path.join(CREDENTIALS_DIR, "users.csv")

EXPECTED_CSV_CONTENT = (
    "user_id,username,old_key\n"
    "1,alice,akjdh231\n"
    "2,bob,98dfjKsl\n"
    "3,charlie,QWERTY999\n"
)


def test_credentials_directory_exists_and_is_writable():
    """
    The directory /home/user/credentials/ must exist and be writable
    by the current (normal) user.
    """
    assert os.path.isdir(CREDENTIALS_DIR), (
        f"Required directory {CREDENTIALS_DIR!r} is missing."
    )
    assert os.access(CREDENTIALS_DIR, os.W_OK), (
        f"Directory {CREDENTIALS_DIR!r} exists but is not writable by the current user."
    )


def test_users_csv_exists():
    """
    The seed file users.csv must exist inside the credentials directory.
    """
    assert os.path.isfile(USERS_CSV), (
        f"Required file {USERS_CSV!r} is missing."
    )


def test_users_csv_permissions():
    """
    users.csv must have mode 0644 (rw-r-r-).
    """
    perms = stat.S_IMODE(os.stat(USERS_CSV).st_mode)
    expected_perms = 0o644
    assert perms == expected_perms, (
        f"{USERS_CSV!r} has permissions {oct(perms)}, expected {oct(expected_perms)}."
    )


def test_users_csv_exact_contents():
    """
    users.csv must contain exactly the four lines specified in the task
    description, each terminated by a single LF (\\n).
    """
    with open(USERS_CSV, "r", newline="") as fh:
        content = fh.read()

    assert content == EXPECTED_CSV_CONTENT, (
        f"{USERS_CSV!r} contents do not match the expected seed data.\n"
        "Expected:\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "Found:\n"
        f"{content!r}"
    )