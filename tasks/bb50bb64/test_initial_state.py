# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any actions for the “alert stream” exercise.
#
# Rules checked:
#   1. The source CSV file exists *and* has the exact expected content.
#   2. Neither the target directory (/home/user/alerts) nor the final
#      output file (/home/user/alerts/alert_stream.log) should exist yet.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants for absolute paths used throughout the tests
# ---------------------------------------------------------------------------

CSV_PATH = Path("/home/user/data/event_feed.csv")
ALERTS_DIR = Path("/home/user/alerts")
ALERTS_FILE = ALERTS_DIR / "alert_stream.log"

# Expected contents of /home/user/data/event_feed.csv as supplied
EXPECTED_CSV_LINES = [
    "event_id,timestamp,service,severity,message",
    "1001,2024-01-14T09:15:22Z,auth,INFO,User login successful",
    "1002,2024-01-14T09:18:05Z,database,CRITICAL,Database connection lost",
    "1003,2024-01-14T09:20:47Z,web,WARN,High latency detected",
    "1004,2024-01-14T09:22:10Z,filesystem,CRITICAL,Disk space critically low",
    "1005,2024-01-14T09:25:33Z,auth,INFO,User logout",
    "1006,2024-01-14T09:30:01Z,network,MAJOR,Packet loss above threshold",
    "1007,2024-01-14T09:35:17Z,security,CRITICAL,Multiple failed logins",
    "1008,2024-01-14T09:40:00Z,backup,INFO,Backup completed",
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file_preserve_newlines(path: Path) -> str:
    """
    Read file as text and return its full contents (including the final
    newline, if present).
    """
    with path.open("r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_source_csv_exists():
    """The source CSV must exist at the exact absolute path."""
    assert CSV_PATH.exists(), (
        f"Expected source file '{CSV_PATH}' is missing. "
        "Ensure the initial dataset is in place."
    )
    assert CSV_PATH.is_file(), (
        f"Expected '{CSV_PATH}' to be a regular file, but it is not."
    )


def test_source_csv_contents_are_exact():
    """
    Verify that the CSV file has exactly the nine lines (header + 8 events)
    expected by the exercise, and that it ends with a single newline.
    """
    contents = read_file_preserve_newlines(CSV_PATH)

    # 1. File must end with exactly one newline character.
    assert contents.endswith("\n"), (
        f"'{CSV_PATH}' must end with a single UNIX newline (\\n)."
    )

    # 2. Split lines without keeping the newline characters.
    lines = contents.rstrip("\n").split("\n")

    assert lines == EXPECTED_CSV_LINES, (
        f"The contents of '{CSV_PATH}' differ from the expected initial data.\n"
        "If you have already modified the file, restore it to the original "
        "state before running the solution."
    )

    # 3. There should be exactly 9 lines (header + 8 data rows).
    assert len(lines) == 9, (
        f"'{CSV_PATH}' should contain exactly 9 lines, found {len(lines)}."
    )


def test_alerts_directory_absent_initially():
    """
    Before the student runs their script, the /home/user/alerts directory
    should NOT yet exist.
    """
    assert not ALERTS_DIR.exists(), (
        f"The directory '{ALERTS_DIR}' should NOT exist before the task runs. "
        "The student's solution is responsible for creating it."
    )


def test_alerts_file_absent_initially():
    """
    Before the student runs their script, the alert_stream.log file should
    NOT yet exist.
    """
    assert not ALERTS_FILE.exists(), (
        f"The file '{ALERTS_FILE}' should NOT exist before the task runs. "
        "The student's solution is responsible for creating it."
    )