# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating system
# before the student performs any action for the “user-accounts” task.
#
# Rules verified:
# 1. The directory /home/user/data exists.
# 2. The file /home/user/data/user_accounts.csv exists and its contents
#    match exactly the five expected lines (including the header).
# 3. No assertions are made about the yet-to-be-created helper files
#    (usernames.txt and new_userlist.csv), per the grading rules.

from pathlib import Path

import pytest

DATA_DIR = Path("/home/user/data")
CSV_PATH = DATA_DIR / "user_accounts.csv"

EXPECTED_CSV_LINES = [
    "username,email,role",
    "alice,alice@example.com,editor",
    "bob,bob@example.com,admin",
    "carol,carol@example.com,viewer",
    "dave,dave@example.com,editor",
]


def test_data_directory_exists():
    """
    The /home/user/data directory must be present before the student starts.
    """
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} does not exist."
    assert DATA_DIR.is_dir(), f"Expected {DATA_DIR} to be a directory."


def test_user_accounts_csv_exists_with_correct_content():
    """
    Validate that the user_accounts.csv file exists and has the exact
    five-line content (LF endings implied by reading in text mode).
    """
    assert CSV_PATH.exists(), f"Required file {CSV_PATH} is missing."
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."

    # Read the file and strip the universal newline character
    with CSV_PATH.open("r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]

    assert (
        lines == EXPECTED_CSV_LINES
    ), (
        "Content mismatch in user_accounts.csv:\n\n"
        f"Expected:\n{EXPECTED_CSV_LINES}\n\n"
        f"Found:\n{lines}"
    )

    assert (
        len(lines) == 5
    ), "user_accounts.csv should contain exactly 5 lines (including header)."