# test_initial_state.py
#
# Pytest suite to verify the operating‐system / filesystem *before*
# the student performs any actions for the “compliance analyst” task.
#
# Expectations for the pristine state:
# 1. Directory /home/user/audit/reports      MUST exist and be a directory.
# 2. File      /home/user/audit/reports/annual_2024.txt
#              MUST exist and contain exactly the two lines documented
#              in the task description (including trailing newline).
# 3. Symlink   /home/user/audit/latest_report       MUST NOT yet exist.
# 4. File      /home/user/audit/audit_trail.csv     MUST NOT yet exist.
#
# The tests below enforce these requirements and provide clear, actionable
# failure messages if the state differs.

import os
from pathlib import Path

import pytest

AUDIT_DIR          = Path("/home/user/audit")
REPORTS_DIR        = AUDIT_DIR / "reports"
REPORT_FILE        = REPORTS_DIR / "annual_2024.txt"
EXPECTED_CONTENTS  = (
    "Compliance Report 2024\n"
    "All systems passed baseline checks.\n"
)

SYMLINK_PATH       = AUDIT_DIR / "latest_report"
AUDIT_LOG_PATH     = AUDIT_DIR / "audit_trail.csv"


def test_reports_directory_exists_and_writable():
    """The directory /home/user/audit/reports must exist and be writable."""
    assert REPORTS_DIR.exists(), (
        f"Required directory missing: {REPORTS_DIR}"
    )
    assert REPORTS_DIR.is_dir(), (
        f"Expected {REPORTS_DIR} to be a directory."
    )
    # Confirm we can at least list its contents (read) and have write access.
    assert os.access(REPORTS_DIR, os.W_OK), (
        f"Directory {REPORTS_DIR} exists but is not writable by the user."
    )


def test_annual_report_file_correct():
    """annual_2024.txt must exist with the exact expected contents."""
    assert REPORT_FILE.exists(), (
        f"Required report file missing: {REPORT_FILE}"
    )
    assert REPORT_FILE.is_file(), (
        f"{REPORT_FILE} exists but is not a regular file."
    )

    actual = REPORT_FILE.read_text(encoding="utf-8")
    assert (
        actual == EXPECTED_CONTENTS
    ), (
        f"Contents of {REPORT_FILE} do not match the expected text.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CONTENTS}"
        "---- Actual ----\n"
        f"{actual}"
        "-----------------\n"
    )


def test_latest_report_symlink_absent():
    """The symlink /home/user/audit/latest_report must NOT yet exist."""
    assert not SYMLINK_PATH.exists(), (
        f"Symlink or file {SYMLINK_PATH} should not exist before the task is run."
    )
    # Also ensure no dangling symlink
    assert not SYMLINK_PATH.is_symlink(), (
        f"{SYMLINK_PATH} is unexpectedly present as a symlink."
    )


def test_audit_trail_csv_absent():
    """The audit_trail.csv file must NOT yet exist."""
    assert not AUDIT_LOG_PATH.exists(), (
        f"Audit log {AUDIT_LOG_PATH} should not exist before the task is run."
    )