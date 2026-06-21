# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# *before* the student performs the assignment.  It checks only the
# pre-existing artefacts and deliberately ignores any files or
# directories that the student is supposed to create (e.g.,
# /home/user/output or its contents).

import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "event_stream.txt"

# Exact contents of /home/user/logs/event_stream.txt
EXPECTED_LOG_LINES = [
    "2024-06-01 10:00:00,INFO,UserLogin",
    "2024-06-01 10:00:02,ERROR,PaymentFailure",
    "2024-06-01 10:00:05,INFO,PageView",
    "2024-06-01 10:00:07,WARNING,CacheMiss",
    "2024-06-01 10:00:10,INFO,PageView",
    "2024-06-01 10:00:12,ERROR,PaymentFailure",
    "2024-06-01 10:00:15,ERROR,DBTimeout",
    "2024-06-01 10:00:18,INFO,UserLogout",
    "2024-06-01 10:00:20,WARNING,CacheMiss",
    "2024-06-01 10:00:22,INFO,UserLogin",
]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_logs_directory_exists_and_is_directory():
    """
    The directory /home/user/logs must already exist
    before the student starts.  It must be a directory.
    """
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_event_stream_file_exists_and_is_file():
    """
    The file /home/user/logs/event_stream.txt must already exist.
    """
    assert LOG_FILE.exists(), f"Required file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_event_stream_contents_match_expected():
    """
    Verify that the contents of /home/user/logs/event_stream.txt match
    the fixture provided in the task description.  This serves two
    purposes:
      1. Ensures the grader's environment is as expected.
      2. Protects against accidental modification of the source data.
    """
    contents = LOG_FILE.read_text(encoding="utf-8").splitlines()
    assert contents == EXPECTED_LOG_LINES, (
        "The contents of {path} differ from the expected fixture.\n"
        "Expected lines:\n{expected}\n\nActual lines:\n{actual}".format(
            path=LOG_FILE,
            expected="\n".join(EXPECTED_LOG_LINES),
            actual="\n".join(contents),
        )
    )