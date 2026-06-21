# test_initial_state.py
#
# This pytest file validates that the initial filesystem **before** the
# student performs any action is exactly as described in the task.
#
# What we check:
#   1. The directory /home/user/container_debug/logs exists and is a directory
#      with permissions 755.
#   2. The log file /home/user/container_debug/logs/app_container_01.log exists,
#      is a regular file with permissions 644, and contains exactly the eight
#      lines specified in the task description (UTF-8, UNIX newlines).
#
# We intentionally DO NOT test for the presence (or absence) of
# /home/user/container_debug/error_summary.log because that is an output file
# the student is expected to create.


import os
import stat
from pathlib import Path

import pytest


LOG_DIR = Path("/home/user/container_debug/logs")
LOG_FILE = LOG_DIR / "app_container_01.log"

EXPECTED_LOG_LINES = [
    "2023-08-01 10:02:15 INFO App started",
    "2023-08-01 10:03:47 WARN Low memory",
    "2023-08-01 10:05:03 ERROR NullPointerException at line 42",
    "2023-08-01 10:07:11 INFO Processing request id=123",
    "2023-08-01 10:08:54 ERROR IndexOutOfBoundsException at line 87",
    "2023-08-01 10:09:33 INFO Request completed id=123",
    "2023-08-01 10:11:22 ERROR Failed to connect to database",
    "2023-08-01 10:12:45 INFO App terminated",
]


def _get_mode_bits(path: Path) -> int:
    """Return the permission bits (e.g., 0o755) for the given path."""
    return path.stat().st_mode & 0o777


def test_log_directory_exists_and_permissions():
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "It should already exist before the task is attempted."
    )
    assert LOG_DIR.is_dir(), (
        f"{LOG_DIR} exists but is not a directory."
    )

    expected_mode = 0o755
    actual_mode = _get_mode_bits(LOG_DIR)
    assert actual_mode == expected_mode, (
        f"{LOG_DIR} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)} instead."
    )


def test_log_file_exists_permissions_and_content():
    assert LOG_FILE.exists(), (
        f"Required log file {LOG_FILE} is missing. "
        "It should already exist before the task is attempted."
    )
    assert LOG_FILE.is_file(), (
        f"{LOG_FILE} exists but is not a regular file."
    )

    expected_mode = 0o644
    actual_mode = _get_mode_bits(LOG_FILE)
    assert actual_mode == expected_mode, (
        f"{LOG_FILE} should have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)} instead."
    )

    # Read file as UTF-8 and split into lines without newline characters
    with LOG_FILE.open("r", encoding="utf-8", newline='') as fh:
        contents = fh.read()
    lines = contents.splitlines()

    # Validate line count
    assert len(lines) == len(EXPECTED_LOG_LINES), (
        f"{LOG_FILE} should contain {len(EXPECTED_LOG_LINES)} lines, "
        f"but contains {len(lines)} lines."
    )

    # Validate exact line content and ordering
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LOG_LINES, lines), start=1):
        assert expected == actual, (
            f"Line {idx} of {LOG_FILE} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Actual  : {actual!r}"
        )