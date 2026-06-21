# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system /
# filesystem before the learner begins the exercise.  It checks that the raw
# Docker logs are present exactly as described and that no output directory
# (/home/user/analysis/) exists yet.
#
# Only the Python standard library and pytest are used, in line with the rules.

import os
import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "container_logs"
ANALYSIS_DIR = HOME / "analysis"

# --------------------------------------------------------------------------- #
# Helpers & shared constants
# --------------------------------------------------------------------------- #
_REGEX_LINE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z [0-9a-f]{12} (INFO|WARN|ERROR) .+$"
)

EXPECTED_FILES = {
    "app_2024-06-01.log": [
        "2024-06-01T10:15:03Z 4a1b2c3d4e5f INFO Container started\n",
        "2024-06-01T10:15:05Z 4a1b2c3d4e5f INFO Health check passed\n",
        "2024-06-01T12:05:47Z 4a1b2c3d4e5f ERROR Connection timeout to database\n",
        "2024-06-01T12:10:03Z ab12cd34ef56 INFO Container started\n",
        "2024-06-01T12:15:47Z ab12cd34ef56 ERROR Connection timeout to database\n",
        "2024-06-01T13:20:10Z 7890abcd1234 INFO Container started\n",
        "2024-06-01T13:25:22Z 7890abcd1234 ERROR Unexpected EOF while reading response\n",
    ],
    "app_2024-06-02.log": [
        "2024-06-02T09:00:00Z 4a1b2c3d4e5f INFO Daily scheduled task started\n",
        "2024-06-02T09:05:00Z 4a1b2c3d4e5f ERROR Failed to pull image\n",
        "2024-06-02T11:45:15Z ab12cd34ef56 WARN Memory usage high\n",
        "2024-06-02T12:00:03Z 4a1b2c3d4e5f ERROR Connection timeout to database\n",
        "2024-06-02T14:30:42Z 7890abcd1234 ERROR Connection timeout to database\n",
    ],
    "app_2024-06-03.log": [
        "2024-06-03T08:10:11Z ab12cd34ef56 INFO Health check passed\n",
        "2024-06-03T10:22:47Z ab12cd34ef56 ERROR Failed to pull image\n",
        "2024-06-03T11:00:00Z 4a1b2c3d4e5f ERROR Connection timeout to database\n",
        "2024-06-03T12:15:17Z 7890abcd1234 ERROR Unexpected EOF while reading response\n",
        "2024-06-03T15:45:55Z 7890abcd1234 ERROR Connection timeout to database\n",
    ],
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_log_directory_exists_and_is_directory():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_expected_log_files_present_and_no_extras():
    present_files = sorted(p.name for p in LOG_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())
    # Presence / absence
    missing = sorted(set(expected_files) - set(present_files))
    extra = sorted(set(present_files) - set(expected_files))

    assert not missing, (
        f"The following expected log file(s) are missing in {LOG_DIR}: {missing}"
    )
    assert not extra, (
        f"Found unexpected file(s) in {LOG_DIR}: {extra}. "
        "Directory must only contain the three provided log files."
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES.items())
def test_each_log_file_contents_exactly_match(filename, expected_lines):
    file_path = LOG_DIR / filename
    assert file_path.exists(), f"Required file {file_path} is missing."

    # Read with universal newlines to preserve '\n' and ensure exact match
    with file_path.open("r", newline="") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected fixtures.\n"
        f"- Expected {len(expected_lines)} lines, got {len(actual_lines)} lines."
    )

    # Additionally make sure every line follows the prescribed format
    for line_num, line in enumerate(actual_lines, 1):
        assert _REGEX_LINE.match(line.rstrip("\n")), (
            f"{file_path}:{line_num} does not match the required log-line format:\n"
            f"    {line}"
        )


def test_analysis_directory_absent_initially():
    assert not ANALYSIS_DIR.exists(), (
        f"The directory {ANALYSIS_DIR} must not exist before the student starts. "
        "It should be created by the learner as part of the task."
    )