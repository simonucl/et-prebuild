# test_initial_state.py
"""
Pytest suite that validates the initial OS / filesystem state *before* the
student starts working on the “unreachable ping” exercise.

This file checks only the prerequisites (inputs) that must already be present.
It intentionally does NOT check for any output artefacts that the student is
supposed to create later (e.g. unreachable_report.txt).
"""

from pathlib import Path
import pytest

# --------------------------------------------------------------------------- #
# Constants describing the canonical initial state.
# --------------------------------------------------------------------------- #

NETWORK_DIR = Path("/home/user/network_logs")
PING_LOG = NETWORK_DIR / "ping_results.log"

EXPECTED_LINES = [
    "[2023-10-01 12:00:01] 192.168.1.1 SUCCESS\n",
    "[2023-10-01 12:00:02] 10.0.0.1 FAILED\n",
    "[2023-10-01 12:00:03] 192.168.1.1 SUCCESS\n",
    "[2023-10-01 12:00:04] 10.0.0.1 FAILED\n",
    "[2023-10-01 12:00:05] 172.16.0.1 FAILED\n",
    "[2023-10-01 12:00:06] 10.0.0.1 FAILED\n",
    "[2023-10-01 12:00:07] 172.16.0.1 FAILED\n",
    "[2023-10-01 12:00:08] 192.168.1.1 SUCCESS\n",
    "[2023-10-01 12:00:09] 10.0.0.2 FAILED\n",
    "[2023-10-01 12:00:10] 10.0.0.2 FAILED\n",
    "[2023-10-01 12:00:11] 192.168.1.2 SUCCESS\n",
]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _read_file_lines(path: Path):
    """
    Return the file contents as a list of lines, preserving newline characters.
    """
    with path.open("r", encoding="utf-8", newline="") as fp:
        return fp.readlines()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_network_logs_directory_exists():
    assert NETWORK_DIR.exists(), (
        f"Required directory {NETWORK_DIR} does not exist."
    )
    assert NETWORK_DIR.is_dir(), (
        f"{NETWORK_DIR} exists but is not a directory."
    )


def test_ping_results_log_exists():
    assert PING_LOG.exists(), (
        f"Required log file {PING_LOG} is missing."
    )
    assert PING_LOG.is_file(), (
        f"{PING_LOG} exists but is not a regular file."
    )


def test_ping_results_log_contains_expected_lines_exactly():
    """
    Verify that the ping_results.log file contains exactly the 11 lines
    specified in the task description, with correct ordering and UNIX newlines.
    """
    actual_lines = _read_file_lines(PING_LOG)

    # First, check line count for an early, clear failure message.
    assert len(actual_lines) == len(EXPECTED_LINES), (
        f"{PING_LOG} should contain {len(EXPECTED_LINES)} lines but "
        f"actually contains {len(actual_lines)}."
    )

    # Then compare each line in order so that pytest's assertion diff is useful.
    assert actual_lines == EXPECTED_LINES, (
        f"Contents of {PING_LOG} do not match the required initial data. "
        "See diff for mismatched lines."
    )


def test_ping_results_log_has_unix_newlines_only():
    """
    Ensure there are no Windows-style CRLF line endings in the file.
    """
    content_bytes = PING_LOG.read_bytes()
    assert b"\r\n" not in content_bytes, (
        f"{PING_LOG} contains Windows-style CRLF line endings; "
        "file must use UNIX LF ('\\n') only."
    )