# test_initial_state.py
"""
Pytest suite that validates the operating-system / file-system **before** the
student begins the task described in the prompt.

Checks performed:

1. /home/user/logs must exist and be a directory.
2. The file /home/user/logs/credential_events_20240115.log must exist, be a
   regular UTF-8 text file, and contain exactly the nine expected lines.
3. The directory /home/user/rotation_report must **not** exist yet (neither as
   a file nor as a directory).  This guarantees the student has not already
   produced any output artefacts.
"""

import os
from pathlib import Path

import pytest

# ---------- Constants ---------------------------------------------------------------------------

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
EVENT_LOG = LOGS_DIR / "credential_events_20240115.log"
ROTATION_REPORT_DIR = HOME / "rotation_report"

EXPECTED_LOG_LINES = [
    "2024-01-15T14:45:30Z,alice,OLD_KEY",
    "2024-01-15T14:50:42Z,bob,OLD_KEY",
    "2024-01-15T14:59:59Z,alice,NEW_KEY",
    "2024-01-15T15:12:04Z,alice,OLD_KEY",
    "2024-01-15T15:30:10Z,carol,NEW_KEY",
    "2024-01-15T16:45:19Z,bob,OLD_KEY",
    "2024-01-15T16:50:02Z,carol,NEW_KEY",
    "2024-01-15T17:01:54Z,alice,OLD_KEY",
    "2024-01-15T17:15:00Z,carol,NEW_KEY",
]


# ---------- Helper ------------------------------------------------------------------------------

def read_log_lines(path: Path):
    """Read a UTF-8 file and return its lines with trailing newlines stripped."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read().splitlines()


# ---------- Tests -------------------------------------------------------------------------------

def test_logs_directory_exists():
    assert LOGS_DIR.exists(), (
        f"Required directory {LOGS_DIR} is missing. "
        "The raw credential log must be located here."
    )
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."


def test_event_log_exists_and_is_correct():
    assert EVENT_LOG.exists(), (
        f"Expected log file {EVENT_LOG} is missing. "
        "This log is necessary for the upcoming rotation checks."
    )
    assert EVENT_LOG.is_file(), f"{EVENT_LOG} exists but is not a regular file."

    try:
        lines = read_log_lines(EVENT_LOG)
    except UnicodeDecodeError as e:
        pytest.fail(
            f"Could not read {EVENT_LOG} as UTF-8 text: {e}"
        )

    assert lines == EXPECTED_LOG_LINES, (
        f"The contents of {EVENT_LOG} do not match the expected initial state.\n"
        f"Expected {len(EXPECTED_LOG_LINES)} specific lines, got {len(lines)} lines."
    )


def test_rotation_report_does_not_exist_yet():
    assert not ROTATION_REPORT_DIR.exists(), (
        f"{ROTATION_REPORT_DIR} already exists, but it should not be present "
        "before the student carries out the task."
    )