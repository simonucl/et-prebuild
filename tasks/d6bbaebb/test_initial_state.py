# test_initial_state.py
#
# Pytest suite that validates the machine **before** the student performs
# any action for the “active users inventory” exercise.  These tests assert
# that the starting operating-system / filesystem state is exactly what the
# instructions claim.

import os
import stat
import pytest

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "data")
RAW_FILE = os.path.join(RAW_DIR, "raw_users.csv")
OUTPUT_DIR = os.path.join(HOME, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "active_usernames_sorted.txt")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
EXPECTED_RAW_LINES = [
    "user_id,username,status,last_login",
    "1,alice,active,2023-08-01",
    "2,bob,inactive,2023-07-15",
    "3,charlie,active,2023-08-02",
    "4,dave,locked,2023-07-29",
    "5,eve,active,2023-08-03",
    "6,frank,active,2023-07-31",
    "7,grace,inactive,2023-08-01",
]


def _perm_bits(path):
    """Return the permission bits portion of st_mode (e.g., 0o644)."""
    return stat.S_IMODE(os.stat(path).st_mode)


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
def test_raw_directory_exists():
    assert os.path.isdir(RAW_DIR), (
        f"Required directory {RAW_DIR!r} is missing. "
        "The initial dataset directory must be present before you start."
    )


def test_raw_file_exists_and_permissions():
    assert os.path.isfile(RAW_FILE), f"Required file {RAW_FILE!r} does not exist."
    expected_perm = 0o644
    perm = _perm_bits(RAW_FILE)
    assert perm == expected_perm, (
        f"{RAW_FILE} has permissions {oct(perm)}, expected {oct(expected_perm)} "
        "(owner: rw-, group: r--, other: r--)."
    )


def test_raw_file_contents_exact():
    with open(RAW_FILE, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]

    assert lines == EXPECTED_RAW_LINES, (
        f"{RAW_FILE} content mismatch.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_RAW_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(lines)
    )


def test_output_directory_absent_initially():
    assert not os.path.exists(OUTPUT_DIR), (
        f"The directory {OUTPUT_DIR!r} should NOT exist before beginning the task "
        "(it will be created by the student's command)."
    )


def test_output_file_absent_initially():
    assert not os.path.exists(OUTPUT_FILE), (
        f"The file {OUTPUT_FILE!r} should NOT exist before beginning the task."
    )