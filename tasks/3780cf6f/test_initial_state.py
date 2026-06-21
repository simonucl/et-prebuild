# test_initial_state.py
#
# This pytest suite validates the *initial* state of the OS / filesystem
# before the learner starts working.  It checks ONLY the prerequisites
# (the raw data directory and CSV file) and **does not** look for any of
# the output artefacts the learner will create later.

import os
from pathlib import Path

import pytest

RAW_DIR = Path("/home/user/data/raw")
CSV_PATH = RAW_DIR / "events.csv"

# --------------------------------------------------------------------------- #
# Helper: expected file contents                                               #
# --------------------------------------------------------------------------- #

EXPECTED_LINES = [
    "id,user,event_type,timestamp",
    "1,user01,login,2023-01-01T08:01:00Z",
    "2,user02,view,2023-01-01T08:02:00Z",
    "3,user03,purchase,2023-01-01T08:03:00Z",
    "4,user04,logout,2023-01-01T08:04:00Z",
    "5,user05,view,2023-01-01T08:05:00Z",
    "6,user06,click,2023-01-01T08:06:00Z",
    "7,user07,view,2023-01-01T08:07:00Z",
    "8,user08,login,2023-01-01T08:08:00Z",
    "9,user09,purchase,2023-01-01T08:09:00Z",
    "10,user10,login,2023-01-01T08:10:00Z",
    "11,user11,purchase,2023-01-01T08:11:00Z",
    "12,user12,view,2023-01-01T08:12:00Z",
    "13,user13,logout,2023-01-01T08:13:00Z",
    "14,user14,click,2023-01-01T08:14:00Z",
    "15,user15,login,2023-01-01T08:15:00Z",
    "16,user16,purchase,2023-01-01T08:16:00Z",
    "17,user17,logout,2023-01-01T08:17:00Z",
    "18,user18,view,2023-01-01T08:18:00Z",
    "19,user19,login,2023-01-01T08:19:00Z",
    "20,user20,view,2023-01-01T08:20:00Z",
    "21,user21,unknown,2023-01-01T08:21:00Z",
]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_raw_directory_exists():
    """The /home/user/data/raw directory must already be present."""
    assert RAW_DIR.exists(), f"Required directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


def test_events_csv_exists_and_is_file():
    """The raw CSV file must exist and be a regular file."""
    assert CSV_PATH.exists(), f"Required file {CSV_PATH} is missing."
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."


def test_events_csv_contents():
    """
    The CSV file must contain exactly the 22 lines specified in the task
    description, each terminated by a single UNIX newline.
    """
    with CSV_PATH.open("r", newline="") as f:
        raw_lines = f.readlines()

    # Check line count first so the message is meaningful
    expected_line_count = len(EXPECTED_LINES)
    actual_line_count = len(raw_lines)
    assert (
        actual_line_count == expected_line_count
    ), f"{CSV_PATH} should contain {expected_line_count} lines, found {actual_line_count}."

    # Iterate and compare each line (stripping the trailing '\n' for comparison)
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, raw_lines), start=1):
        # Strip *one* trailing newline for comparison, but keep other whitespace intact
        actual_stripped = actual.rstrip("\n")
        assert (
            actual_stripped == expected
        ), (
            f"Line {idx} of {CSV_PATH} is incorrect.\n"
            f"Expected: {repr(expected)}\n"
            f"Found   : {repr(actual_stripped)}"
        )

    # Verify every line ended with '\n' (protects against missing final newline)
    for idx, line in enumerate(raw_lines, start=1):
        assert line.endswith("\n"), f"Line {idx} of {CSV_PATH} is missing its final newline."


# --------------------------------------------------------------------------- #
# End of file                                                                 #
# --------------------------------------------------------------------------- #