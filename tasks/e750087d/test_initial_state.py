# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student performs any actions.
#
# It asserts:
#   1. /home/user/logs/ exists and is a directory.
#   2. /home/user/reports/ does NOT yet exist.
#   3. /home/user/logs/webserver.log exists, is a regular file,
#      and its contents match the specification exactly.
#
# Any failure message should clearly indicate what is missing or incorrect.

import os
import stat
import pytest

LOG_DIR = "/home/user/logs"
REPORTS_DIR = "/home/user/reports"
LOG_FILE = os.path.join(LOG_DIR, "webserver.log")

EXPECTED_LOG_LINES = [
    "2024-04-12T10:14:01Z server1.example.com status=UP   response_ms=101\n",
    "2024-04-12T10:15:32Z server1.example.com status=DOWN response_ms=0\n",
    "2024-04-12T10:16:45Z server2.example.com status=UP   response_ms=95\n",
    "2024-04-12T10:17:02Z server2.example.com status=DOWN response_ms=0\n",
    "2024-04-12T10:18:01Z server1.example.com status=UP   response_ms=103\n",
    "2024-04-12T10:19:20Z server1.example.com status=DOWN response_ms=0\n",
    "2024-04-12T10:20:45Z server2.example.com status=UP   response_ms=96\n",
    "2024-04-12T10:21:11Z server3.example.com status=DOWN response_ms=0\n",
]


def _assert_is_dir(path: str) -> None:
    assert os.path.exists(path), f"Expected directory {path!r} to exist, but it does not."
    assert os.path.isdir(path), f"Path {path!r} exists but is not a directory."

    mode = os.stat(path).st_mode
    assert stat.S_IMODE(mode) & stat.S_IRUSR, f"Directory {path!r} is missing read permission for the user."
    assert stat.S_IMODE(mode) & stat.S_IXUSR, f"Directory {path!r} is missing execute permission for the user."


def test_logs_directory_exists_and_is_readable():
    """Verify /home/user/logs exists, is a directory, and is accessible."""
    _assert_is_dir(LOG_DIR)


def test_reports_directory_does_not_exist_yet():
    """Verify /home/user/reports does NOT exist at the start."""
    assert not os.path.exists(REPORTS_DIR), (
        f"Directory {REPORTS_DIR!r} should NOT exist yet, "
        "but it is already present."
    )


def test_webserver_log_file_exists_and_contents_correct():
    """Verify the log file exists and its content matches exactly."""
    assert os.path.exists(LOG_FILE), f"Expected log file {LOG_FILE!r} to exist, but it does not."
    assert os.path.isfile(LOG_FILE), f"Path {LOG_FILE!r} exists but is not a regular file."

    # Read file contents
    with open(LOG_FILE, "r", encoding="utf-8") as fp:
        actual_lines = fp.readlines()

    # Exact length check
    assert len(actual_lines) == len(EXPECTED_LOG_LINES), (
        f"{LOG_FILE!r} should have {len(EXPECTED_LOG_LINES)} lines, "
        f"found {len(actual_lines)}."
    )

    # Line-by-line comparison for precise matching
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LOG_LINES, actual_lines), start=1):
        assert actual == expected, (
            f"Mismatch in {LOG_FILE!r} on line {idx}:\n"
            f"  Expected: {expected!r}\n"
            f"  Found:    {actual!r}"
        )

    # Additional sanity check: exactly four DOWN status lines
    down_lines = [ln for ln in actual_lines if "status=DOWN" in ln]
    assert len(down_lines) == 4, (
        f"Expected 4 lines containing 'status=DOWN' in {LOG_FILE!r}, "
        f"found {len(down_lines)}."
    )