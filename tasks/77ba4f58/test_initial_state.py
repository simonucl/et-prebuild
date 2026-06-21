# test_initial_state.py
#
# Pytest suite to verify the initial, pre-task condition of the filesystem
# for the “uptime benchmark” exercise.
#
# The tests confirm that:
#   1. /home/user/services.list exists and contains EXACTLY the three
#      required endpoints, in order, with no stray whitespace.
#   2. No /home/user/logs directory (or file) exists yet.
#   3. Consequently, no /home/user/logs/uptime_report.log file exists.
#
# These checks guarantee that students start from the required clean slate
# and that their subsequent single-command solution has the correct inputs.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
SERVICES_LIST = HOME / "services.list"
LOGS_DIR = HOME / "logs"
UPTIME_LOG = LOGS_DIR / "uptime_report.log"

EXPECTED_ENDPOINTS = [
    "127.0.0.1",
    "192.0.2.1",
    "203.0.113.1",
]


def test_services_list_exists_and_is_file():
    """/home/user/services.list must exist and be a regular file."""
    assert SERVICES_LIST.exists(), (
        f"Missing required file: {SERVICES_LIST}. "
        "The exercise depends on this list of endpoints."
    )
    assert SERVICES_LIST.is_file(), (
        f"{SERVICES_LIST} exists but is not a regular file. "
        "It must be a plain text file containing the endpoints."
    )


def test_services_list_contents_are_correct():
    """
    /home/user/services.list must contain exactly three lines,
    with the expected endpoints in order and no extra whitespace.
    """
    with SERVICES_LIST.open("r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    # Strip trailing newlines for comparison but keep other whitespace to test.
    # Retain original lines for detailed error messages.
    stripped_lines = [line.rstrip("\n") for line in raw_lines]

    assert len(stripped_lines) == 3, (
        f"{SERVICES_LIST} must contain exactly 3 lines but has "
        f"{len(stripped_lines)} line(s): {stripped_lines!r}"
    )

    for idx, (expected, actual) in enumerate(zip(EXPECTED_ENDPOINTS, stripped_lines), 1):
        assert actual == expected, (
            f"Line {idx} of {SERVICES_LIST} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}\n"
            "Ensure there is no leading/trailing whitespace."
        )


def test_logs_directory_does_not_exist():
    """
    No /home/user/logs directory (or file) should be present
    before the student's one-liner runs.
    """
    assert not LOGS_DIR.exists(), (
        f"Found unexpected path {LOGS_DIR}. "
        "The logs directory must NOT exist before the task is executed."
    )


def test_uptime_report_log_does_not_exist():
    """
    The uptime_report.log file must not exist yet,
    as it is to be created by the student's command.
    """
    assert not UPTIME_LOG.exists(), (
        f"Found unexpected file {UPTIME_LOG}. "
        "The report log should be created only by the student."
    )