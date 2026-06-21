# test_initial_state.py
#
# Pytest suite that verifies the **initial** state of the operating system /
# filesystem _before_ the student carries out any commands for the
# “permission-audit” exercise.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
AUDIT_DIR = HOME / "permission_audit"
RAW_FILE = AUDIT_DIR / "raw_permissions.txt"

# The raw inventory must consist of these 20 lines in this exact order.
EXPECTED_RAW_LINES = [
    "rwxr-xr-x",
    "rw-r--r--",
    "rwxr-xr-x",
    "rw-r--r--",
    "rw-r--r--",
    "rwx------",
    "rwxr-xr-x",
    "rwx------",
    "rwxr-xr-x",
    "rw-r--r--",
    "rwxr-xr-x",
    "rwxr-xr--",
    "rwxr-xr--",
    "rw-r--r--",
    "rwxr-xr--",
    "rwxr-xr-x",
    "rw-r--r--",
    "rw-r--r--",
    "rwxr-xr-x",
    "rwxr-xr-x",
]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _read_raw_file():
    """Return the lines of the raw permission file without trailing new-lines."""
    with RAW_FILE.open("r", encoding="utf-8") as fh:
        # Strip the trailing '\n' from each line, but leave the order intact.
        return [line.rstrip("\n") for line in fh.readlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_audit_directory_exists():
    """`/home/user/permission_audit` must already exist and be a directory."""
    assert AUDIT_DIR.exists(), (
        f"Required directory '{AUDIT_DIR}' is missing. "
        "Create it before running the audit."
    )
    assert AUDIT_DIR.is_dir(), f"'{AUDIT_DIR}' exists but is not a directory."


def test_raw_permissions_file_exists():
    """`raw_permissions.txt` must already exist inside the audit directory."""
    assert RAW_FILE.exists(), (
        f"Input file '{RAW_FILE}' is missing. "
        "The task requires this file to be present _untouched_."
    )
    assert RAW_FILE.is_file(), f"'{RAW_FILE}' exists but is not a regular file."


def test_raw_permissions_file_contents():
    """
    Verify that `raw_permissions.txt` has exactly the expected 20 lines
    in the precise order provided by the exercise.  This ensures that
    students operate on a known, immutable data set.
    """
    actual_lines = _read_raw_file()

    # 1. Correct number of lines
    assert len(actual_lines) == len(
        EXPECTED_RAW_LINES
    ), (
        f"'{RAW_FILE}' should contain {len(EXPECTED_RAW_LINES)} lines, "
        f"but {len(actual_lines)} were found."
    )

    # 2. Exact line-by-line match
    # Pin-point any discrepancies for easier debugging.
    mismatches = [
        (idx + 1, exp, act)
        for idx, (exp, act) in enumerate(zip(EXPECTED_RAW_LINES, actual_lines))
        if exp != act
    ]

    assert not mismatches, (
        "The contents of 'raw_permissions.txt' do not match the expected initial "
        "state.  Differences found on the following line(s):\n" +
        "\n".join(
            f"  line {lineno}: expected '{exp}', found '{act}'"
            for lineno, exp, act in mismatches
        )
    )

    # 3. Optional: check that file ends with a newline character (classic UNIX style).
    with RAW_FILE.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert last_byte == b"\n", (
        f"'{RAW_FILE}' must end with a single UNIX newline (LF). "
        "No extra blank lines or missing newline are allowed."
    )