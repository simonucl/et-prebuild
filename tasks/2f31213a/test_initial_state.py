# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state needed
# for the “cloud migration” exercise is present and correct **before**
# the student starts working.  It checks only the required source log
# files/directories and intentionally ignores any of the output files
# that the student will generate later.
#
# If a check fails the assertion message will explain exactly what is
# missing or incorrect.
#
# Requirements enforced here:
#   • /home/user/cloud_migration/logs directory exists
#   • Three specific *.log files exist inside that directory
#   • Each log file contains the precise, line-for-line content that
#     the assignment description declares.
#
# The tests rely solely on Python’s stdlib plus pytest.


import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Expected directory and file layout
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/cloud_migration")
LOG_DIR = BASE_DIR / "logs"

LOG_CONTENTS = {
    LOG_DIR / "2023-10-01.log": [
        "2023-10-01T12:00:00Z serviceA MIGRATE START",
        "2023-10-01T12:05:00Z serviceA MIGRATE SUCCESS",
        "2023-10-01T13:00:00Z serviceB MIGRATE START",
        "2023-10-01T13:03:00Z serviceB MIGRATE FAIL Error: Disk quota exceeded",
        "2023-10-01T14:00:00Z serviceC MIGRATE START",
        "2023-10-01T14:04:00Z serviceC MIGRATE SUCCESS",
    ],
    LOG_DIR / "2023-10-02.log": [
        "2023-10-02T09:00:00Z serviceA MIGRATE START",
        "2023-10-02T09:04:30Z serviceA MIGRATE SUCCESS",
        "2023-10-02T10:00:10Z serviceB MIGRATE START",
        "2023-10-02T10:05:00Z serviceB MIGRATE FAIL Error: Network unreachable",
        "2023-10-02T11:00:00Z serviceC MIGRATE START",
        "2023-10-02T11:05:40Z serviceC MIGRATE SUCCESS",
    ],
    LOG_DIR / "2023-10-03.log": [
        "2023-10-03T15:00:00Z serviceA MIGRATE START",
        "2023-10-03T15:07:00Z serviceA MIGRATE SUCCESS",
        "2023-10-03T16:00:00Z serviceB MIGRATE START",
        "2023-10-03T16:09:15Z serviceB MIGRATE SUCCESS",
        "2023-10-03T17:00:00Z serviceC MIGRATE START",
        "2023-10-03T17:08:50Z serviceC MIGRATE FAIL Error: Timeout contacting datastore",
    ],
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file_lines(path: Path):
    """
    Return the contents of *path* as a list of text lines with trailing
    newlines stripped.  If the file is missing, an IOError will propagate.
    """
    with path.open("r", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_log_directory_exists():
    """
    The main log directory must exist and be a directory.
    """
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


@pytest.mark.parametrize("log_path, expected_lines", LOG_CONTENTS.items())
def test_individual_log_files_exist_and_match_content(log_path: Path, expected_lines):
    """
    Each required log file must exist, be a regular file, and contain the exact
    lines defined in LOG_CONTENTS (order matters; no extra or missing lines).
    """
    # Presence checks
    assert log_path.exists(), f"Required file {log_path} is missing."
    assert log_path.is_file(), f"{log_path} exists but is not a regular file."

    # Content checks
    actual_lines = read_file_lines(log_path)
    assert actual_lines == expected_lines, (
        f"Contents of {log_path} do not match expected data.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        f"  " + "\n  ".join(expected_lines) + "\n"
        f"Found ({len(actual_lines)} lines):\n"
        f"  " + "\n  ".join(actual_lines)
    )