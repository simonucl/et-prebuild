# test_initial_state.py
#
# This pytest suite validates that the **initial** operating-system / file-system
# state is exactly as described *before* the student performs any actions for
# the “incident triage” exercise.

import os
import calendar
import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")

INCIDENTS_DIR = HOME / "incidents"
ARCHIVE_DIR = HOME / "archived_logs"
SUMMARY_FILE = HOME / "incident_summary_20240315.log"

# --------------------------------------------------------------------------- #
# Reference data describing the expected initial state
# --------------------------------------------------------------------------- #

# Cold logs – must be older than 2024-03-01 00:00:00 and still located
# under /home/user/incidents/
COLD_LOGS = {
    INCIDENTS_DIR / "daily-20240201" / "system.log": [
        "2024-02-01 12:35:01 ERROR: CODE1001 Unable to connect to database",
        "2024-02-01 12:37:22 ERROR: CODE1002 Timeout while reading response",
    ],
    INCIDENTS_DIR / "daily-20240205" / "app.log": [
        "2024-02-05 09:10:11 ERROR: CODE1002 Timeout while reading response",
        "2024-02-05 09:16:45 ERROR: CODE1003 Null pointer exception",
    ],
}

# Hot logs – must have mtime >= 2024-03-01 00:00:00 and live where expected
HOT_LOGS = {
    INCIDENTS_DIR / "daily-20240310" / "system.log": [
        "2024-03-10 10:00:00 ERROR: CODE1004 Disk full",
    ],
    INCIDENTS_DIR / "daily-20240312" / "app.log": [
        "2024-03-12 11:00:00 ERROR: CODE1002 Timeout while reading response",
        "2024-03-12 11:01:00 ERROR: CODE1001 Unable to connect to database",
    ],
}

ALL_LOG_PATHS = set(COLD_LOGS) | set(HOT_LOGS)

# Epoch timestamp for 2024-03-01 00:00:00 UTC (cold / hot cut-off)
CUTOFF_TS = calendar.timegm((2024, 3, 1, 0, 0, 0, 0, 0, 0))


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _file_contains_lines(path: Path, required_substrings):
    """
    Return True iff *every* substring in `required_substrings` appears at least
    once (in any line) inside the file located at `path`.
    """
    with path.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    return all(s in contents for s in required_substrings)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_incidents_directory_exists():
    assert INCIDENTS_DIR.is_dir(), (
        f"Expected directory {INCIDENTS_DIR} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize("log_path", sorted(ALL_LOG_PATHS))
def test_each_expected_log_file_exists(log_path: Path):
    assert log_path.is_file(), f"Expected log file {log_path} to exist, but it does not."


def test_no_extra_log_files_present():
    """
    Ensure there are no '*.log' files under /home/user/incidents/ beyond the
    four that are explicitly defined in the exercise statement.  This guards
    against hidden fixtures or previous runs polluting the initial state.
    """
    discovered_logs = {
        Path(root) / fname
        for root, _dirs, files in os.walk(INCIDENTS_DIR)
        for fname in files
        if fname.endswith(".log")
    }
    assert discovered_logs == ALL_LOG_PATHS, (
        "Unexpected set of .log files found under "
        f"{INCIDENTS_DIR}.\nExpected:\n  "
        + "\n  ".join(map(str, sorted(ALL_LOG_PATHS)))
        + "\nFound:\n  "
        + "\n  ".join(map(str, sorted(discovered_logs)))
    )


@pytest.mark.parametrize("cold_log", sorted(COLD_LOGS))
def test_cold_log_mtime_and_contents(cold_log: Path):
    """
    Cold logs must have a modification time strictly *before* the cut-off and
    must contain the expected ERROR lines.
    """
    mtime = cold_log.stat().st_mtime
    assert mtime < CUTOFF_TS, (
        f"Cold log {cold_log} has mtime {mtime} (epoch) which is not earlier "
        "than 2024-03-01 00:00:00.  It should be classified as 'cold'."
    )

    assert _file_contains_lines(cold_log, COLD_LOGS[cold_log]), (
        f"File {cold_log} is missing one or more expected ERROR lines."
    )


@pytest.mark.parametrize("hot_log", sorted(HOT_LOGS))
def test_hot_log_mtime_and_contents(hot_log: Path):
    """
    Hot logs must have a modification time on or *after* the cut-off date and
    must contain the required ERROR lines.
    """
    mtime = hot_log.stat().st_mtime
    assert mtime >= CUTOFF_TS, (
        f"Hot log {hot_log} has mtime {mtime} (epoch) which is earlier than "
        "2024-03-01 00:00:00.  It should *not* be treated as 'cold'."
    )

    assert _file_contains_lines(hot_log, HOT_LOGS[hot_log]), (
        f"File {hot_log} is missing one or more expected ERROR lines."
    )


def test_archive_directory_does_not_yet_exist():
    assert not ARCHIVE_DIR.exists(), (
        f"Archive directory {ARCHIVE_DIR} must *not* exist before the student "
        "runs their solution."
    )


def test_summary_file_does_not_yet_exist():
    assert not SUMMARY_FILE.exists(), (
        f"Summary file {SUMMARY_FILE} must *not* exist before the student "
        "runs their solution."
    )