# test_initial_state.py
#
# Pytest suite that validates the starting (pre-task) filesystem state
# for the “log-summary” exercise.
#
# WHAT WE CHECK
# 1. The directory /home/user/logs exists and is a directory.
# 2. The file /home/user/logs/app.log exists, is a regular file, and its
#    contents match EXACTLY the expected baseline (including the single
#    trailing newline and no extra blank lines).
#
# NOTES
# • We deliberately do NOT check for the presence or absence of the
#   would-be output file (/home/user/logs/2023-08-15-errors.txt) because
#   the rubric forbids assertions on output artefacts in the initial-state
#   tests.
# • Only the Python standard library and pytest are used.

import os
import difflib
import pytest

LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

EXPECTED_LINES = [
    "2023-08-14 10:15:23 INFO User login success\n",
    "2023-08-14 10:17:01 ERROR Failed to connect to DB\n",
    "2023-08-15 07:02:11 WARN Disk usage high\n",
    "2023-08-15 08:33:48 ERROR Timeout while reading configuration\n",
    "2023-08-15 09:01:10 ERROR Invalid user input\n",
    "2023-08-15 14:22:59 ERROR Connection reset by peer\n",
    "2023-08-16 12:45:00 INFO Routine maintenance started\n",
]


def _format_diff(actual: list[str], expected: list[str]) -> str:
    """
    Return a unified diff between expected and actual content that is
    compact yet informative for assertion messages.
    """
    diff = difflib.unified_diff(
        expected,
        actual,
        fromfile="expected",
        tofile="actual",
        lineterm="",
    )
    return "\n".join(diff)


@pytest.mark.describe("Verify that /home/user/logs exists and is a directory")
def test_logs_directory_exists_and_is_dir():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR!r} does not exist "
        f"or is not a directory."
    )


@pytest.mark.describe("Verify that /home/user/logs/app.log exists with correct content")
def test_app_log_exists_and_contents_match():
    # 1. Existence & type
    assert os.path.isfile(LOG_FILE), (
        f"Required log file {LOG_FILE!r} is missing or not a regular file."
    )

    # 2. Read entire file
    with open(LOG_FILE, encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    # 3. Ensure exact match, including trailing newline count
    if actual_lines != EXPECTED_LINES:
        diff_msg = _format_diff(actual_lines, EXPECTED_LINES)
        pytest.fail(
            "Contents of /home/user/logs/app.log do not match expected "
            "initial state.\nUnified diff (expected ⟶ actual):\n"
            f"{diff_msg}"
        )