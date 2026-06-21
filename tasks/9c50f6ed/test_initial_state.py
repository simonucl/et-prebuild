# test_initial_state.py
#
# This pytest file validates the initial state of the operating system / filesystem
# BEFORE the student performs any action.  It confirms that the raw uptime data file
# is present exactly as described and that the containing directory exists.
#
# NOTE:  We deliberately do NOT check for the presence (or absence) of the output
#        file `/home/user/logs/uptime_summary.csv`, because that file is supposed
#        to be created by the student and the instructions explicitly forbid
#        testing any output artefacts in the initial-state test suite.

import os
from pathlib import Path

import pytest

LOG_DIR = Path("/home/user/logs")
FULL_CSV = LOG_DIR / "uptime_full.csv"

EXPECTED_FULL_CONTENT = (
    "timestamp,status,response_ms\n"
    "2023-05-01T00:00:00Z,UP,123\n"
    "2023-05-01T00:05:00Z,UP,110\n"
    "2023-05-01T00:10:00Z,DOWN,0\n"
    "2023-05-01T00:15:00Z,UP,130\n"
)


def test_logs_directory_exists_and_is_dir():
    """Ensure /home/user/logs/ exists and is a directory."""
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory, but it's not."


def test_uptime_full_csv_exists_and_is_file():
    """Ensure the uptime_full.csv file exists inside /home/user/logs/."""
    assert FULL_CSV.exists(), f"Required file {FULL_CSV} is missing."
    assert FULL_CSV.is_file(), f"Expected {FULL_CSV} to be a regular file, but it's not."


def test_uptime_full_csv_contents_are_exact():
    """
    Verify that /home/user/logs/uptime_full.csv contains exactly the expected bytes,
    including the trailing newline on the last line.
    """
    actual_content = FULL_CSV.read_text(encoding="utf-8")
    assert (
        actual_content == EXPECTED_FULL_CONTENT
    ), (
        f"Contents of {FULL_CSV} do not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_FULL_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{actual_content!r}\n"
    )