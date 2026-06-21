# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student begins the shell-scripting task described in the
# prompt.  The tests deliberately avoid checking for any artefacts that
# are supposed to be created *by* the student (e.g. the summary CSV).
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
REPORT_DIR = HOME / "build_reports"
LOG_FILE = REPORT_DIR / "build_full_2023-09-15.log"

EXPECTED_LOG_CONTENT = (
    "ID;Platform;Start;End;Status;Duration(s)\n"
    "B1021;android;2023-09-15T01:02:03Z;2023-09-15T01:07:10Z;Success;307\n"
    "B1022;ios;2023-09-15T02:10:00Z;2023-09-15T02:24:45Z;Failed;885\n"
    "B1023;android;2023-09-15T03:05:30Z;2023-09-15T03:11:01Z;Success;331\n"
    "B1024;ios;2023-09-15T04:20:10Z;2023-09-15T04:25:35Z;Success;325\n"
)


def test_reports_directory_exists_and_is_directory():
    """Verify that /home/user/build_reports exists and is a directory."""
    assert REPORT_DIR.exists(), (
        f"Required directory {REPORT_DIR} is missing. "
        "Create it or adjust the path."
    )
    assert REPORT_DIR.is_dir(), (
        f"{REPORT_DIR} exists but is not a directory. "
        "Ensure the path is a directory."
    )


def test_log_file_exists():
    """Verify that the full build log file exists before processing."""
    assert LOG_FILE.exists(), (
        f"Required log file {LOG_FILE} is missing. "
        "Make sure the file is present before running the task."
    )
    assert LOG_FILE.is_file(), (
        f"{LOG_FILE} exists but is not a regular file."
    )


def test_log_file_contents_are_exact():
    """
    The build log must contain *exactly* the six expected lines with
    LF line endings.  A final trailing newline **is** part of the spec.
    """
    # Read in binary mode to preserve exact byte sequence.
    data = LOG_FILE.read_bytes()
    try:
        decoded = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"Could not decode {LOG_FILE} as UTF-8: {exc}"
        )

    assert decoded == EXPECTED_LOG_CONTENT, (
        f"Contents of {LOG_FILE} do not match the expected data.\n\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n\n"
        "Found:\n"
        f"{decoded!r}\n"
        "Check for extra/missing lines, incorrect separators, or wrong "
        "line endings."
    )