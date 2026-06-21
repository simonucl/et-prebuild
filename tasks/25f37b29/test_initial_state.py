# test_initial_state.py
#
# Pytest suite to verify the machine’s state _before_ the student
# performs any actions for the “quick spot-check” compliance task.
#
# We assert that:
#   1. The source log file exists exactly where the task description says.
#   2. The log file is a regular file (not a dir / symlink, etc.).
#   3. The log file already contains **exactly seven** “[ERROR]” lines,
#      so that the student can simply count them and record the number 7.
#   4. No audit summary file is already present (the student must create it).
#
# Any failure here means the machine is in an unexpected state *before*
# the student starts the task.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_FILE = HOME / "logs" / "app_2023-09-15.log"
COMPLIANCE_DIR = HOME / "compliance"
AUDIT_FILE = COMPLIANCE_DIR / "audit_2023-09-15.txt"


def test_log_file_exists_and_is_regular_file():
    """
    The application log file must be present and be a regular file.
    """
    assert LOG_FILE.exists(), (
        f"Expected log file {LOG_FILE} is missing. "
        "The task cannot be completed without it."
    )
    assert LOG_FILE.is_file(), (
        f"{LOG_FILE} exists but is not a regular file. "
        "It must be a plain text file that can be read."
    )


def test_log_file_contains_exactly_seven_error_lines():
    """
    The log file should contain exactly seven lines with the literal '[ERROR]'.
    """
    with LOG_FILE.open("r", encoding="utf-8") as fp:
        error_lines = [ln for ln in fp if "[ERROR]" in ln]

    assert len(error_lines) == 7, (
        f"Expected 7 '[ERROR]' lines in {LOG_FILE}, found {len(error_lines)}.\n"
        "The fixture data is incorrect; adjust the test fixture or fix the file."
    )


def test_audit_file_does_not_yet_exist():
    """
    Before the student does anything, the audit summary file must NOT exist.
    Its presence would indicate that the workspace is 'dirty'.
    """
    assert not AUDIT_FILE.exists(), (
        f"Audit file {AUDIT_FILE} already exists, but it should be created by "
        "the student during the exercise."
    )