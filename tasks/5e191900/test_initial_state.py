# test_initial_state.py
#
# This pytest suite verifies that the *initial* filesystem state is exactly
# what the exercise statement promises.  It intentionally does **not** look
# for any output produced by the student—only the pre-existing input data.
#
# The following aspects are validated:
#   1. Presence and basic permissions of the two input files.
#   2. Structural correctness of users_full.tsv (header content, column count,
#      number of records, presence of both ACTIVE and non-ACTIVE users).
#   3. Structural correctness of new_roles.tsv (no header, two columns only).
#   4. One-to-one username coverage and identical ordering between the two
#      input files.
#
# If any of these tests fail, the exercise itself cannot be completed
# correctly, so the failure messages aim to be explicit and actionable.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import os
import stat
import pytest


# ---------- Helper utilities -------------------------------------------------

BASE_DIR = Path("/home/user")
INPUT_DIR = BASE_DIR / "input"

USERS_FILE = INPUT_DIR / "users_full.tsv"
ROLES_FILE = INPUT_DIR / "new_roles.tsv"


def assert_world_readable(file_path: Path):
    """
    Assert that the given file is world-readable (other read bit is set).
    """
    mode = file_path.stat().st_mode
    assert mode & stat.S_IROTH, f"{file_path} exists but is **not** world-readable."


def read_tsv(path: Path):
    """
    Return a list of rows, where each row is a list obtained by splitting
    on a single TAB.  Newlines are stripped.  The file is read in binary
    mode and then decoded to ensure we preserve exact byte content.
    """
    with path.open("rb") as fh:
        lines = fh.read().splitlines()
    # Decode each line assuming UTF-8 (TSV usually ASCII/UTF-8)
    return [line.decode("utf-8").split("\t") for line in lines]


# ---------- Tests -------------------------------------------------------------

def test_input_files_exist_and_are_regular_files():
    """
    Both required input files must exist, be regular files, and be world-readable.
    """
    for file_path in (USERS_FILE, ROLES_FILE):
        assert file_path.exists(), f"Missing required input file: {file_path}"
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."
        assert_world_readable(file_path)


def test_users_full_tsv_structure():
    """
    Validate the header, column count, record count, and mixture of statuses
    in users_full.tsv.
    """
    rows = read_tsv(USERS_FILE)
    assert rows, f"{USERS_FILE} is empty."

    header = rows[0]
    expected_header = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "department",
        "role",
        "status",
    ]
    assert header == expected_header, (
        f"{USERS_FILE} header mismatch.\n"
        f"Expected: {expected_header}\n"
        f"Found   : {header}"
    )

    data_rows = rows[1:]
    expected_data_records = 5
    assert (
        len(data_rows) == expected_data_records
    ), f"{USERS_FILE} should contain {expected_data_records} data records, found {len(data_rows)}."

    # Every row must have exactly 8 columns.
    for idx, row in enumerate(data_rows, start=2):  # start=2 accounts for header line number
        assert len(row) == 8, (
            f"{USERS_FILE}: line {idx} has {len(row)} columns instead of 8.\n"
            f"Row content: {row}"
        )

    # There must be at least one ACTIVE and one non-ACTIVE user.
    statuses = [row[7] for row in data_rows]  # column 8 is status (0-indexed 7)
    assert "ACTIVE" in statuses, f"{USERS_FILE} contains no users with status ACTIVE."
    assert any(s != "ACTIVE" for s in statuses), (
        f"{USERS_FILE} should contain some non-ACTIVE users to make the exercise meaningful."
    )


def test_new_roles_tsv_structure():
    """
    new_roles.tsv must have no header and exactly two columns per line.
    It must hold exactly the same number of lines as users_full data records.
    """
    rows = read_tsv(ROLES_FILE)
    assert rows, f"{ROLES_FILE} is empty."

    expected_lines = 5  # must match the number of data rows in users_full.tsv
    assert len(rows) == expected_lines, (
        f"{ROLES_FILE} should contain {expected_lines} lines (no header). "
        f"Found {len(rows)}."
    )

    for idx, row in enumerate(rows, start=1):
        assert len(row) == 2, (
            f"{ROLES_FILE}: line {idx} has {len(row)} columns instead of 2.\n"
            f"Row content: {row}"
        )


def test_username_alignment_between_files():
    """
    The set of usernames and their order must be identical between users_full.tsv
    (data section) and new_roles.tsv.
    """
    user_rows = read_tsv(USERS_FILE)[1:]  # skip header
    role_rows = read_tsv(ROLES_FILE)

    usernames_from_users = [row[1] for row in user_rows]  # column 2
    usernames_from_roles = [row[0] for row in role_rows]  # column 1

    assert usernames_from_users == usernames_from_roles, (
        "Usernames in users_full.tsv data rows do not exactly match the usernames "
        "in new_roles.tsv (either the sets differ or the ordering is inconsistent).\n\n"
        f"users_full.tsv usernames (order): {usernames_from_users}\n"
        f"new_roles.tsv  usernames (order): {usernames_from_roles}"
    )