# test_initial_state.py
"""
Pytest suite that validates the filesystem **before** the student begins the
exercise described in the prompt.

Expected initial state:

1. The raw input file /home/user/data/uptime_sample.csv must exist and its
   contents must *exactly* match the canonical sample provided in the task
   description (LF line endings, trailing newline).

2. No derivative work directory (/home/user/sre_reports) should exist yet.
   Its absence guarantees the student starts from a clean slate.

Nothing else is verified at this stage so that the student is free to create
the required output directory and files as part of their solution.

Only Python’s stdlib and pytest are used.
"""

import os
from pathlib import Path

import pytest

RAW_FILE_PATH = Path("/home/user/data/uptime_sample.csv")
DERIVATIVE_DIR = Path("/home/user/sre_reports")

# The canonical contents of the raw CSV as specified in the task description.
EXPECTED_RAW_CONTENT = (
    "timestamp,service,status\n"
    "2023-09-01T00:00:00Z,auth-service,UP\n"
    "2023-09-01T00:01:00Z,auth-service,DOWN\n"
    "2023-09-01T00:02:00Z,auth-service,UP\n"
    "2023-09-01T00:00:00Z,api-gateway,UP\n"
    "2023-09-01T00:01:00Z,api-gateway,UP\n"
    "2023-09-01T00:02:00Z,api-gateway,DOWN\n"
    "2023-09-01T00:03:00Z,api-gateway,DOWN\n"
    "2023-09-01T00:04:00Z,api-gateway,UP\n"
)


def test_raw_csv_exists():
    """
    The raw uptime sample CSV must exist at the exact absolute path
    /home/user/data/uptime_sample.csv.
    """
    assert RAW_FILE_PATH.exists(), (
        f"Expected the raw data file {RAW_FILE_PATH} to exist, "
        "but it is missing."
    )
    assert RAW_FILE_PATH.is_file(), (
        f"{RAW_FILE_PATH} exists but is not a regular file."
    )


def test_raw_csv_contents_are_exact():
    """
    Validate that the raw CSV file's contents exactly match the canonical sample
    (including final trailing LF and no CR characters).
    """
    raw_bytes = RAW_FILE_PATH.read_bytes()

    # Ensure LF line endings only and decode as UTF-8
    assert b"\r" not in raw_bytes, (
        f"{RAW_FILE_PATH} contains CR characters; expected LF-only line endings."
    )

    raw_text = raw_bytes.decode("utf-8")
    assert raw_text == EXPECTED_RAW_CONTENT, (
        "The contents of /home/user/data/uptime_sample.csv do not match the "
        "expected canonical sample.\n"
        "If you believe the file is correct, double-check for extra spaces, "
        "missing lines, or missing trailing newline."
    )


def test_sre_reports_directory_does_not_exist_yet():
    """
    The derivative directory (/home/user/sre_reports) should *not* exist before
    the student starts the task. Its presence would indicate leftover state
    from a previous run or manual tampering.
    """
    assert not DERIVATIVE_DIR.exists(), (
        f"Found unexpected directory {DERIVATIVE_DIR}. "
        "The student must create this directory during their solution, so it "
        "should not be present beforehand."
    )