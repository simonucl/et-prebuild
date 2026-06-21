# test_initial_state.py
"""
Pytest suite to validate the initial, pre-action state of the filesystem for the
“ping summary” task.

The tests assert that:
1. The required directory /home/user/net_tests exists and has sensible (0755)
   permissions.
2. The CSV input file /home/user/net_tests/ping_results.csv exists, has the
   expected (0644) permissions, and its contents match the exact specification
   given in the task description.

Nothing is tested about any output artefacts (e.g. ping_summary.json or
action.log), by explicit requirement.
"""

import os
import stat
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/net_tests")
CSV_PATH = BASE_DIR / "ping_results.csv"

EXPECTED_CSV_LINES = [
    "host,status,latency_ms",
    "8.8.8.8,success,23",
    "1.1.1.1,success,19",
    "192.0.2.1,failed,",
    "example.com,success,45",
]


def _octal_mode(path: Path) -> int:
    """Return a path's permission bits in octal (e.g. 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)


def test_directory_exists_and_permissions():
    assert BASE_DIR.exists(), f"Required directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."

    mode = _octal_mode(BASE_DIR)
    # Directory must be at least 0755; extra bits are tolerated but warn.
    required_mode = 0o755
    assert (mode & required_mode) == required_mode, (
        f"Directory {BASE_DIR} should have permissions 0755; "
        f"found {oct(mode)}."
    )


def test_csv_file_exists_and_permissions():
    assert CSV_PATH.exists(), f"Required CSV file {CSV_PATH} is missing."
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."

    mode = _octal_mode(CSV_PATH)
    required_mode = 0o644
    assert (mode & required_mode) == required_mode, (
        f"CSV file {CSV_PATH} should have permissions 0644; found {oct(mode)}."
    )


def test_csv_contents_exact_match():
    contents = CSV_PATH.read_text(encoding="utf-8")
    # Strip a single trailing newline (POSIX text files usually have one).
    contents_lines = contents.rstrip("\n").split("\n")

    assert contents_lines == EXPECTED_CSV_LINES, (
        f"CSV file {CSV_PATH} contents do not match the expected specification.\n"
        f"Expected lines:\n{EXPECTED_CSV_LINES}\n\n"
        f"Actual lines:\n{contents_lines}"
    )