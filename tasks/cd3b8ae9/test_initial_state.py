# test_initial_state.py
#
# This test-suite verifies that the operating-system is in the correct
# initial state *before* the student begins any work on the “daily
# uptime summary” task.
#
# Expectations:
# 1. The source CSV file exists at the precise absolute path and
#    contains the exact, newline-terminated contents described in the
#    spec.
# 2. The destination TXT summary file must **not** exist yet.
# 3. The parent directory /home/user/monitoring/ must exist.
#
# Any deviation from these expectations will cause a test failure with
# a clear, actionable message.
#
# NOTE: Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

MONITORING_DIR = Path("/home/user/monitoring")
SRC_FILE = MONITORING_DIR / "uptime_report.csv"
DST_FILE = MONITORING_DIR / "daily_uptime_summary.txt"

# The exact contents (including the final newline) that must be present
EXPECTED_CSV_CONTENT = (
    "timestamp,service_name,status,response_time_ms\n"
    "2024-04-18T00:00:00Z,auth,UP,120\n"
    "2024-04-18T00:00:00Z,payments,DOWN,0\n"
    "2024-04-18T00:00:00Z,api,UP,95\n"
    "2024-04-18T01:00:00Z,auth,UP,110\n"
    "2024-04-18T01:00:00Z,payments,UP,210\n"
    "2024-04-18T01:00:00Z,api,UP,100\n"
    "2024-04-18T02:00:00Z,auth,DOWN,0\n"
    "2024-04-18T02:00:00Z,payments,UP,190\n"
    "2024-04-18T02:00:00Z,api,UP,98\n"
)


def test_monitoring_directory_exists():
    """The /home/user/monitoring directory must exist."""
    assert MONITORING_DIR.is_dir(), (
        f"Required directory {MONITORING_DIR} is missing. "
        "Create it before proceeding."
    )


def test_source_csv_exists_and_is_readable():
    """The raw probe export CSV must exist and be readable."""
    assert SRC_FILE.exists(), (
        f"Source data file {SRC_FILE} is missing. "
        "It must be present before any processing can begin."
    )
    assert SRC_FILE.is_file(), f"{SRC_FILE} exists but is not a regular file."
    # Ensure it is readable by current user
    assert os.access(SRC_FILE, os.R_OK), f"Source file {SRC_FILE} is not readable."


def test_source_csv_has_expected_content():
    """
    Verify that the CSV file contains exactly the expected lines,
    including the terminal newline.
    """
    with SRC_FILE.open("r", encoding="utf-8") as f:
        actual = f.read()

    assert (
        actual == EXPECTED_CSV_CONTENT
    ), (
        "The contents of the source CSV do not match the expected initial data.\n"
        "If you modified this file by accident, restore it to its original state.\n"
    )

    # Additional sanity checks
    lines = actual.splitlines()
    assert (
        len(lines) == 10
    ), "Source CSV should contain one header plus nine data rows (10 lines total)."

    assert lines[0] == "timestamp,service_name,status,response_time_ms", (
        "The header row of the CSV is incorrect or missing."
    )


def test_destination_file_absent():
    """
    Before the student runs their processing pipeline, the destination
    summary file MUST NOT exist.
    """
    assert not DST_FILE.exists(), (
        f"{DST_FILE} already exists, but it should be created by the student's "
        "solution. Remove it before starting the task."
    )