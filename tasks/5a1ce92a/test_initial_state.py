# test_initial_state.py
#
# PyTest suite that verifies the *initial* file-system state for the
# “ACTIVE users report” assignment.  It checks only the pre-existing
# input data that the student must *not* alter.  Nothing is asserted
# about any expected output files.

import os
import stat
import pytest

HOME = "/home/user"
ACCOUNTS_DIR = os.path.join(HOME, "accounts")

INPUT_FILES = {
    os.path.join(ACCOUNTS_DIR, "users_master.csv"): [
        "user_id,username,full_name,email,status\n",
        "1,alice,Alice Walker,alice@example.com,ACTIVE\n",
        "2,bob,Bob Stone,bob@example.com,INACTIVE\n",
        "3,carol,Carol Smith,carol@example.com,ACTIVE\n",
        "4,dave,David Johnson,dave@example.com,ACTIVE\n",
        "5,erin,Erin Brown,erin@example.com,SUSPENDED\n",
        "6,frank,Frank Harris,frank@example.com,ACTIVE\n",
    ],
    os.path.join(ACCOUNTS_DIR, "departments.csv"): [
        "username,department\n",
        "alice,Engineering\n",
        "bob,Sales\n",
        "carol,HR\n",
        "dave,Engineering\n",
        "erin,Marketing\n",
        "frank,Support\n",
    ],
    os.path.join(ACCOUNTS_DIR, "login_counts.csv"): [
        "username,logins\n",
        "alice,345\n",
        "bob,127\n",
        "carol,512\n",
        "dave,98\n",
        "erin,67\n",
        "frank,250\n",
    ],
}


def _check_perms(path, expected_mode=0o644):
    """
    Verify that the file at *path* has exactly *expected_mode* (octal).
    Only the lower 3 octets are compared so that differing file-type
    bits (e.g., regular vs. symlink) are still caught.
    """
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == expected_mode, (
        f"{path} must have permissions {oct(expected_mode)}; "
        f"found {oct(mode)}"
    )


@pytest.mark.parametrize("path", [ACCOUNTS_DIR])
def test_accounts_directory_exists(path):
    assert os.path.isdir(path), f"Required directory missing: {path}"


@pytest.mark.parametrize("path,expected_lines", INPUT_FILES.items())
def test_input_file_presence_and_permissions(path, expected_lines):
    assert os.path.isfile(path), f"Input file missing: {path}"
    _check_perms(path, 0o644)


@pytest.mark.parametrize("path,expected_lines", INPUT_FILES.items())
def test_input_file_content_exact_match(path, expected_lines):
    """
    Compare each input file byte-for-byte (text mode) with its expected
    contents, including newlines.  This guarantees that the student
    starts from the canonical data set.
    """
    with open(path, "r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == expected_lines, (
        f"Contents of {path} do not match the expected initial state.\n"
        f"--- Expected ---\n{''.join(expected_lines)}"
        f"--- Actual ---\n{''.join(actual_lines)}"
    )