# test_initial_state.py
#
# This test-suite verifies the *initial* state of the operating system
# before the student starts working on the task.  It checks that the
# expected log directory and log file already exist **and** that the
# summary artefacts have **not** yet been created.

import os
import stat
from pathlib import Path

import pytest


LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "ping_results.log"

SUMMARY_DIR = Path("/home/user/summary")
SUMMARY_FILE = SUMMARY_DIR / "uptime_summary.txt"

EXPECTED_LOG_LINES = [
    "2024-08-12 10:00 server1.example.com UP",
    "2024-08-12 10:00 server2.example.com DOWN",
    "2024-08-12 10:01 server3.example.com UP",
    "2024-08-12 10:02 server1.example.com UP",
    "2024-08-12 10:03 server2.example.com UP",
    "2024-08-12 10:04 server3.example.com DOWN",
    "2024-08-12 10:05 server1.example.com UP",
    "2024-08-12 10:06 server3.example.com UP",
    "2024-08-12 10:07 server1.example.com UP",
    "2024-08-12 10:08 server2.example.com DOWN",
]


def _mode(path: Path) -> int:
    """Return the unix permission bits (e.g., 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)


def test_log_directory_exists_and_permissions():
    assert LOG_DIR.exists(), f"Directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."
    expected_mode = 0o755
    actual_mode = _mode(LOG_DIR)
    assert (
        actual_mode == expected_mode
    ), f"Directory {LOG_DIR} should have permissions 755 (0o755) but has {oct(actual_mode)}."


def test_log_file_exists_and_contents_are_correct():
    assert LOG_FILE.exists(), f"Log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."
    # Read the file, stripping the trailing newline if present
    with LOG_FILE.open("r", encoding="ascii") as fh:
        contents = fh.read().splitlines()

    assert (
        contents == EXPECTED_LOG_LINES
    ), (
        f"Contents of {LOG_FILE} do not match the expected 10 records.\n"
        f"Expected:\n{EXPECTED_LOG_LINES}\n\nActual:\n{contents}"
    )


def test_summary_directory_does_not_exist_yet():
    assert not SUMMARY_DIR.exists(), (
        f"Summary directory {SUMMARY_DIR} should not exist before the student starts the task. "
        "Remove it and re-run the tests."
    )


def test_summary_file_does_not_exist_yet():
    assert not SUMMARY_FILE.exists(), (
        f"Summary file {SUMMARY_FILE} should not exist before the student starts the task. "
        "Remove it and re-run the tests."
    )