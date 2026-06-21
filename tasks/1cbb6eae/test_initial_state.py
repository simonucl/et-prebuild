# test_initial_state.py
#
# Pytest suite to validate the *initial* filesystem state
# before the student performs any actions for the credential-rotation drill.
#
# Rules checked:
# 1. The directory /home/user/credentials exists.
# 2. The file /home/user/credentials/old_credentials.txt exists
#    and contains the exact three expected lines (order matters).
# 3. The rotated target file
#       /home/user/credentials/rotated/credentials_2025-01-01.csv
#    must NOT exist yet (the rotation has not been done).
#
# Anything related to rotation.log is deliberately **not** asserted here,
# because it may or may not pre-exist and its contents are outside the
# scope of the initial-state validation.

import os
from pathlib import Path

import pytest

CREDS_DIR = Path("/home/user/credentials")
OLD_FILE = CREDS_DIR / "old_credentials.txt"
ROTATED_FILE = CREDS_DIR / "rotated" / "credentials_2025-01-01.csv"

EXPECTED_OLD_LINES = [
    "serviceA,pass1234",
    "serviceB,mysecret",
    "serviceC,qwerty",
]


def test_credentials_directory_exists():
    """The main credentials directory must be present."""
    assert CREDS_DIR.exists(), (
        f"Expected directory {CREDS_DIR} to exist, "
        "but it was not found."
    )
    assert CREDS_DIR.is_dir(), (
        f"{CREDS_DIR} exists but is not a directory."
    )


def test_old_credentials_file_present_with_correct_contents():
    """Validate the presence and exact contents of old_credentials.txt."""
    assert OLD_FILE.exists(), (
        f"Expected file {OLD_FILE} to exist, "
        "but it was not found."
    )
    assert OLD_FILE.is_file(), (
        f"{OLD_FILE} exists but is not a regular file."
    )

    # Read the file, stripping only the newline characters.
    with OLD_FILE.open("r", encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n\r") for line in f]

    assert actual_lines == EXPECTED_OLD_LINES, (
        f"Contents of {OLD_FILE} do not match the expected initial state.\n"
        f"Expected lines:\n{EXPECTED_OLD_LINES}\n"
        f"Found lines:\n{actual_lines}"
    )


def test_rotated_file_does_not_yet_exist():
    """
    The final rotated credentials file must not pre-exist before the
    student performs the rotation step.
    """
    assert not ROTATED_FILE.exists(), (
        f"Found unexpected file {ROTATED_FILE}. "
        "The rotation step appears to have been run already or the "
        "environment is not clean."
    )