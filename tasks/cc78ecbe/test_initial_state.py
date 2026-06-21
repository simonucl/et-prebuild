# test_initial_state.py
#
# This test-suite validates the _initial_ condition of the operating-system
# before the student runs their solution.  It checks that the log file that
# drives the exercise is present and has the exact expected content, **and**
# that no output artefacts have been created yet.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the required initial state
# --------------------------------------------------------------------------- #

LOG_PATH = Path("/home/user/logs/server_uptime.log")
REPORTS_DIR = Path("/home/user/reports")
DAILY_AVAIL_FILE = REPORTS_DIR / "daily_availability.txt"
SLOW_RESP_FILE = REPORTS_DIR / "slow_responses.txt"

EXPECTED_LOG_LINES = [
    "2023-07-10T00:00:00Z OK 110\n",
    "2023-07-10T00:05:00Z OK 105\n",
    "2023-07-10T00:10:00Z DOWN -\n",
    "2023-07-10T00:15:00Z OK 250\n",
    "2023-07-10T00:20:00Z OK 700\n",
    "2023-07-10T00:25:00Z DOWN -\n",
    "2023-07-10T00:30:00Z OK 95\n",
    "2023-07-10T00:35:00Z OK 900\n",
    "2023-07-10T00:40:00Z OK 430\n",
    "2023-07-10T00:45:00Z OK 510\n",
    "2023-07-10T00:50:00Z DOWN -\n",
    "2023-07-10T00:55:00Z OK 130\n",
    "2023-07-10T01:00:00Z OK 140\n",
    "2023-07-10T01:05:00Z DOWN -\n",
    "2023-07-10T01:10:00Z OK 200\n",
]


# --------------------------------------------------------------------------- #
# Helper(s)
# --------------------------------------------------------------------------- #

def read_file_with_newlines(path: Path):
    """
    Read a text file and return a list of lines **including** their newline
    terminators.
    """
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_log_file_exists():
    """Verify that the source log file exists at the precise location."""
    assert LOG_PATH.exists(), f"Required log file not found: {LOG_PATH}"
    assert LOG_PATH.is_file(), f"Expected {LOG_PATH} to be a regular file"


def test_log_file_content_exact_match():
    """
    The log file must contain exactly the 15 predefined lines, each terminated
    by a single `\\n`, and have exactly one trailing newline at EOF.
    """
    # Ensure the file ends with a single trailing newline
    raw_bytes = LOG_PATH.read_bytes()
    assert raw_bytes.endswith(b"\n"), (
        "Log file must end with a single trailing newline (\"\\n\")"
    )

    lines = read_file_with_newlines(LOG_PATH)

    # Verify line count first for a clearer error message
    assert len(lines) == 15, (
        f"Expected 15 lines in {LOG_PATH}, found {len(lines)}"
    )

    # Now check exact content
    assert lines == EXPECTED_LOG_LINES, (
        "Contents of server_uptime.log do not match the expected initial state"
    )


def test_no_preexisting_report_files():
    """
    Before the student’s solution runs, the /home/user/reports directory and the
    expected output files must not yet exist.
    """
    if REPORTS_DIR.exists():
        assert not DAILY_AVAIL_FILE.exists(), (
            f"Output file should not exist yet: {DAILY_AVAIL_FILE}"
        )
        assert not SLOW_RESP_FILE.exists(), (
            f"Output file should not exist yet: {SLOW_RESP_FILE}"
        )
    else:
        # Directory does not exist, which is also acceptable
        assert not REPORTS_DIR.exists(), (
            f"Directory '{REPORTS_DIR}' should not pre-exist; "
            "it will be created by the student’s script."
        )