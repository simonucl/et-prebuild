# test_initial_state.py
#
# This pytest suite verifies that the initial filesystem state required
# for the compliance-operations exercise is present *before* the student
# begins any work.  It checks:
#   • Mandatory directories exist.
#   • Mandatory raw CSV files exist with the exact expected contents.
#   • The target audit directory exists and is EMPTY.
#
# All assertions include clear, actionable failure messages.
#
# NOTE:  This file must be run before the student performs the task.
#        It deliberately does NOT test for any output artefacts
#        (audit_trail_20230630.csv, build_audit_trail.log, etc.).

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

DIR_COMPLIANCE      = HOME / "compliance"
DIR_RAW             = DIR_COMPLIANCE / "raw"
DIR_AUDIT           = DIR_COMPLIANCE / "audit"

FILE_TRANSACTIONS   = DIR_RAW / "transactions_20230630.csv"
FILE_USERS          = DIR_RAW / "users.csv"

EXPECTED_TRANSACTIONS_CONTENT = (
    "timestamp,transaction_id,user_id,amount,status\n"
    "2023-06-30T09:15:44Z,TN001,U1001,250.00,APPROVED\n"
    "2023-06-30T10:05:37Z,TN002,U1002,145.50,DECLINED\n"
    "2023-06-30T11:22:08Z,TN003,U1003,980.00,APPROVED\n"
)

EXPECTED_USERS_CONTENT = (
    "user_id,user_name\n"
    "U1001,Alice Huang\n"
    "U1002,Bob Singh\n"
    "U1003,Charlie Garcia\n"
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def assert_path_exists(path: Path, path_type: str):
    """Assert that a filesystem path exists and is of the expected type."""
    assert path.exists(), f"Missing {path_type}: {path}"
    if path_type == "directory":
        assert path.is_dir(), f"Expected directory but found non-directory: {path}"
    elif path_type == "file":
        assert path.is_file(), f"Expected file but found non-file: {path}"
    else:
        raise ValueError("path_type must be 'file' or 'directory'")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """Verify that all required directories are present."""
    for directory in (DIR_COMPLIANCE, DIR_RAW, DIR_AUDIT):
        assert_path_exists(directory, "directory")


def test_audit_directory_is_empty():
    """The audit directory must exist and be completely empty at the start."""
    # (It should contain the output files only *after* the student’s script runs.)
    assert_path_exists(DIR_AUDIT, "directory")
    contents = list(DIR_AUDIT.iterdir())
    assert not contents, (
        f"The audit directory {DIR_AUDIT} is expected to be empty before the task "
        f"begins, but it already contains: {[p.name for p in contents]}"
    )


@pytest.mark.parametrize(
    "file_path, expected_content",
    [
        (FILE_TRANSACTIONS, EXPECTED_TRANSACTIONS_CONTENT),
        (FILE_USERS, EXPECTED_USERS_CONTENT),
    ],
)
def test_raw_files_exist_with_correct_content(file_path: Path, expected_content: str):
    """Each raw CSV file must exist with the exact expected byte-for-byte content."""
    assert_path_exists(file_path, "file")

    # Read file in text mode with universal newlines disabled to preserve exact bytes
    with file_path.open("r", newline="") as fh:
        actual = fh.read()

    assert actual == expected_content, (
        f"Content mismatch in {file_path}.\n\n"
        f"--- Expected (len={len(expected_content)} bytes) ---\n"
        f"{expected_content}"
        f"--- Actual (len={len(actual)} bytes) ---\n"
        f"{actual}"
    )