# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem is
# in the correct *initial* state **before** the student begins work on
# the “suspicious login failures” assignment.
#
# The checks performed are intentionally limited to the pre-exercise
# artifacts—primarily the presence and exact content of the input log
# file—and the absence of any output directories or files that the
# student will be expected to create later.
#
# If any test in this file fails, the accompanying assertion message
# will make it clear what is missing or unexpectedly present.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user").expanduser()

# Full paths used in the assignment
LOG_DIR = HOME / "site" / "logs"
LOG_FILE = LOG_DIR / "account_activity.log"
REPORTS_DIR = HOME / "site" / "reports"
REPORT_FILE = REPORTS_DIR / "failed_login_report.txt"

# The exact, line-for-line contents that the initial log file MUST have.
# Each line ends with a single '\n'; the file itself therefore ends with
# one trailing newline (no extra blank lines).
EXPECTED_LOG_CONTENT = (
    "2023-08-01T09:00:01Z user=john ip=192.168.1.10 action=LOGIN status=OK\n"
    "2023-08-01T09:05:43Z user=alice ip=203.0.113.17 action=LOGIN status=FAIL\n"
    "2023-08-01T09:07:12Z user=bob ip=198.51.100.23 action=LOGIN status=FAIL\n"
    "2023-08-01T09:11:58Z user=carol ip=10.0.0.5 action=LOGIN status=FAIL\n"
    "2023-08-01T09:15:22Z user=dave ip=172.20.10.8 action=LOGIN status=FAIL\n"
    "2023-08-01T09:20:30Z user=erin ip=203.0.113.17 action=LOGIN status=FAIL\n"
    "2023-08-01T09:25:44Z user=frank ip=192.0.2.55 action=LOGIN status=OK\n"
    "2023-08-01T09:30:01Z user=grace ip=198.51.100.23 action=LOGIN status=FAIL\n"
    "2023-08-01T09:35:29Z user=heidi ip=192.168.1.15 action=LOGIN status=FAIL\n"
)


def test_log_directory_exists():
    """The directory /home/user/site/logs must exist and be a directory."""
    assert LOG_DIR.exists(), (
        f"Required directory missing: {LOG_DIR} — "
        "the log directory must be present before starting the exercise."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_log_file_exists_with_exact_content():
    """
    The log file must exist, be a regular file, and contain exactly the
    expected nine lines (including the final newline).
    """
    assert LOG_FILE.exists(), (
        f"Required log file missing: {LOG_FILE} — "
        "the assignment cannot be completed without this input file."
    )
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."

    # Read the entire file as bytes then decode, so we do not silently
    # ignore any encoding or newline issues.
    data = LOG_FILE.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{LOG_FILE} is not valid UTF-8: {exc}")  # pragma: no cover

    assert (
        text == EXPECTED_LOG_CONTENT
    ), (
        f"The contents of {LOG_FILE} do not match the expected initial "
        "state.\n\nExpected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n\nFound:\n{text!r}"
    )


def test_reports_directory_and_file_absent():
    """
    The reports directory and the failed_login_report.txt file should NOT
    exist before the student starts the task. Their creation is part of
    the assignment.
    """
    assert not REPORTS_DIR.exists(), (
        f"The directory {REPORTS_DIR} already exists, but it should NOT be "
        "present before the assignment is carried out. Please remove it so "
        "the student can demonstrate directory creation."
    )
    assert not REPORT_FILE.exists(), (
        f"The report file {REPORT_FILE} already exists, but it should NOT be "
        "present before the assignment is carried out."
    )