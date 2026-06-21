# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state is exactly
# as expected *before* the student runs any commands.  It intentionally checks
# ONLY the source artefacts that must already exist and never references the
# /home/user/output/ directory or any files that the student is expected to
# create later.

import os
import stat
import pytest
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

BASE_DIR = Path("/home/user/company_logs")
CSV_FILE = BASE_DIR / "policy_violations.csv"
EMP_FILE = BASE_DIR / "active_employees.txt"

EXPECTED_CSV_LINES = [
    "date,user,policy,severity,action,status",
    "2023-06-01,alice,SSH Root Login,Critical,Alert,OPEN",
    "2023-06-02,bob,Password Reuse,High,Block,CLOSED",
    "2023-06-03,carol,Public S3 Bucket,Medium,Alert,OPEN",
    "2023-06-03,dave,Unencrypted S3 Bucket,High,Alert,OPEN",
    "2023-06-04,erin,Insecure Protocol,Critical,Block,CLOSED",
    "2023-06-05,frank,Outdated SSL Cert,Medium,Alert,OPEN",
    "2023-06-06,grace,Open Security Group,High,Alert,OPEN",
    "2023-06-07,heidi,Missing MFA,Critical,Alert,CLOSED",
]

EXPECTED_EMP_LINES = [
    "alice",
    "carol",
    "dave",
    "frank",
    "grace",
    "mallory",
]


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def read_non_empty_lines(path: Path):
    """Return a list of non-empty lines stripped of their trailing newlines."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n\r") for ln in fh if ln.rstrip("\n\r") != ""]


def is_world_readable(path: Path) -> bool:
    """Check that a file is world-readable (mode 0o644 or similar)."""
    mode = path.stat().st_mode
    return bool(mode & stat.S_IROTH)  # world readable


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_company_logs_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} does not exist. "
        "The initial dataset should be present under /home/user/company_logs/."
    )


def test_policy_violations_csv_exists_and_contents():
    assert CSV_FILE.is_file(), f"Expected CSV file missing at {CSV_FILE}."

    actual_lines = read_non_empty_lines(CSV_FILE)
    assert (
        actual_lines == EXPECTED_CSV_LINES
    ), (
        f"Content mismatch in {CSV_FILE}.\n"
        f"Expected {len(EXPECTED_CSV_LINES)} lines but found {len(actual_lines)}.\n"
        "Please ensure the file has the exact initial contents provided in the task."
    )

    assert is_world_readable(
        CSV_FILE
    ), f"{CSV_FILE} should be world-readable (chmod 644 or similar)."


def test_active_employees_txt_exists_and_contents():
    assert EMP_FILE.is_file(), f"Expected text file missing at {EMP_FILE}."

    actual_lines = read_non_empty_lines(EMP_FILE)
    assert (
        actual_lines == EXPECTED_EMP_LINES
    ), (
        f"Content mismatch in {EMP_FILE}.\n"
        f"Expected {len(EXPECTED_EMP_LINES)} lines but found {len(actual_lines)}.\n"
        "Please ensure the file has the exact initial contents provided in the task."
    )

    assert is_world_readable(
        EMP_FILE
    ), f"{EMP_FILE} should be world-readable (chmod 644 or similar)."