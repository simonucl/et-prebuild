# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student starts solving the exercise.
#
# It checks that:
#   1. The logs directory exists and is writable.
#   2. The raw log file exists and has the exact expected contents
#      (10 LF-terminated lines, no CR characters, no extra blank lines).
#   3. Neither of the required output CSV files is already present.
#
# Only modules from the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "projects" / "logs"
RAW_LOG = LOG_DIR / "raw_events.log"
EVENTS_CSV = LOG_DIR / "login_success_events.csv"
COUNTS_CSV = LOG_DIR / "login_success_counts.csv"


@pytest.fixture(scope="module")
def expected_raw_lines():
    """Return the exact lines expected to be found in raw_events.log."""
    return [
        b"EVENT|2023-09-01T10:12:45Z|alice|LOGIN_SUCCESS\n",
        b"EVENT|2023-09-01T10:15:01Z|bob|LOGIN_FAILURE\n",
        b"EVENT|2023-09-01T10:17:22Z|alice|FILE_UPLOAD\n",
        b"EVENT|2023-09-01T10:20:55Z|carol|LOGIN_SUCCESS\n",
        b"EVENT|2023-09-01T10:25:30Z|bob|LOGIN_SUCCESS\n",
        b"EVENT|2023-09-01T10:30:05Z|alice|LOGIN_SUCCESS\n",
        b"EVENT|2023-09-01T10:35:47Z|dave|FILE_DELETE\n",
        b"EVENT|2023-09-01T10:40:18Z|carol|LOGIN_FAILURE\n",
        b"EVENT|2023-09-01T10:45:00Z|bob|LOGIN_SUCCESS\n",
        b"EVENT|2023-09-01T10:50:10Z|alice|LOGIN_FAILURE\n",
    ]


def test_logs_directory_exists_and_writable():
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "Create it before running the solution."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    # Check write permission for the current user.
    can_write = os.access(LOG_DIR, os.W_OK)
    assert can_write, (
        f"Directory {LOG_DIR} is not writable. "
        "Adjust its permissions so new CSV files can be created."
    )


def test_raw_log_file_exists():
    assert RAW_LOG.exists(), (
        f"Required log file {RAW_LOG} is missing. "
        "It must be present before processing starts."
    )
    assert RAW_LOG.is_file(), f"{RAW_LOG} exists but is not a regular file."


def test_raw_log_file_contents(expected_raw_lines):
    with RAW_LOG.open("rb") as fh:
        actual = fh.readlines()

    # Helpful assertions with detailed error messages
    assert actual, f"{RAW_LOG} is empty—expected 10 lines of data."
    assert len(actual) == len(expected_raw_lines), (
        f"{RAW_LOG} should contain {len(expected_raw_lines)} lines "
        f"but has {len(actual)}."
    )

    for idx, (act, exp) in enumerate(zip(actual, expected_raw_lines), start=1):
        assert act == exp, (
            f"Line {idx} of {RAW_LOG} is incorrect.\n"
            f"Expected: {exp!r}\n"
            f"Found   : {act!r}"
        )

    # Guard against CRLF endings (should be LF only)
    assert all(b"\r" not in line for line in actual), (
        f"{RAW_LOG} contains CR characters; only LF line endings are allowed."
    )


@pytest.mark.parametrize("csv_path", [EVENTS_CSV, COUNTS_CSV])
def test_output_csv_files_do_not_exist_yet(csv_path):
    assert not csv_path.exists(), (
        f"Output file {csv_path} already exists. "
        "The workspace should start without the generated CSV files."
    )