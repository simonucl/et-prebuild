# test_initial_state.py
#
# This pytest suite verifies that the operating-system state matches the
# expected “starting point” for the student.  It intentionally checks **only**
# the resources that must already exist and explicitly confirms that the
# deliverable file has NOT been created yet.

import os
import re
from pathlib import Path

import pytest

AUDIT_DIR = Path("/home/user/audit")
RAW_LOG = AUDIT_DIR / "raw_login_attempts.log"
REPORT_CSV = AUDIT_DIR / "ip_frequency_report.csv"

# The exact contents the raw log file must contain—one IPv4 address per line.
EXPECTED_RAW_LINES = [
    "192.168.1.10",
    "10.0.0.5",
    "192.168.1.10",
    "8.8.8.8",
    "10.0.0.5",
    "10.0.0.5",
    "203.0.113.1",
    "8.8.8.8",
    "192.168.1.10",
    "198.51.100.2",
    "203.0.113.1",
    "203.0.113.1",
    "127.0.0.1",
    "192.168.1.10",
    "127.0.0.1",
]

_IPV4_RE = re.compile(
    r"""
    ^
    (25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d) \.
    (25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d) \.
    (25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d) \.
    (25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    $
    """,
    re.VERBOSE,
)


def test_audit_directory_exists():
    assert AUDIT_DIR.is_dir(), (
        f"Required directory {AUDIT_DIR} is missing. "
        "The assignment expects all audit files to reside here."
    )


def test_raw_log_exists_and_is_file():
    assert RAW_LOG.is_file(), (
        f"Required raw log file {RAW_LOG} is missing. "
        "Create this file before attempting the task."
    )


def test_raw_log_contents_are_exact_and_valid_ipv4():
    with RAW_LOG.open("r", encoding="utf-8") as fh:
        # Strip the trailing newline from each line for comparison.
        actual_lines = [line.rstrip("\n") for line in fh]

    assert (
        actual_lines == EXPECTED_RAW_LINES
    ), (
        "The contents of the raw log file do not match the expected starter "
        "dataset.\n\n"
        f"Expected ({len(EXPECTED_RAW_LINES)} lines):\n{EXPECTED_RAW_LINES}\n\n"
        f"Found ({len(actual_lines)} lines):\n{actual_lines}"
    )

    # Additional sanity check: every line must be a syntactically valid IPv4 address.
    invalid_lines = [
        ip for ip in actual_lines if not _IPV4_RE.match(ip)
    ]
    assert not invalid_lines, (
        "The raw log contains lines that are not valid IPv4 addresses:\n"
        + "\n".join(invalid_lines)
    )


def test_report_file_does_not_exist_yet():
    # The student has not produced the report yet, so it should be absent.
    assert not REPORT_CSV.exists(), (
        f"Output report {REPORT_CSV} already exists, but it should be created "
        "by the student as part of the assignment and must not be present in "
        "the initial state."
    )