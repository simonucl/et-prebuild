# test_initial_state.py
#
# This test-suite validates that the starting operating-system / filesystem
# matches the expected *initial* conditions for the “daily summary” exercise.
#
# DO NOT modify this file.  The student’s solution must make it pass *as is*.
#
# What we check:
#   • /home/user/logs/automation_events.log must exist, be readable and contain
#     exactly the 16 log-lines listed in the task description (plus a single
#     trailing newline).
#
# What we deliberately do NOT check:
#   • Any file or directory under /home/user/analysis
#   • Any output/summary file
#
# Only stdlib and pytest are used, as required.

import difflib
from pathlib import Path

import pytest


LOG_PATH = Path("/home/user/logs/automation_events.log")

# The 16 expected log-lines, *without* the trailing newline characters.
EXPECTED_LOG_LINES = [
    "2024-04-12 08:00:01 INFO TaskScheduler: TASK_START id=120 type=cleanup",
    "2024-04-12 08:00:03 INFO TaskProcessor: TASK_SUCCESS id=120 duration=2s",
    "2024-04-12 09:15:00 INFO TaskScheduler: TASK_START id=121 type=backup",
    "2024-04-12 09:15:20 ERROR TaskProcessor: TASK_FAIL id=121 reason=NO_SPACE",
    "2024-04-12 09:45:10 INFO TaskScheduler: TASK_START id=122 type=deploy",
    "2024-04-12 09:45:45 INFO TaskProcessor: TASK_SUCCESS id=122 duration=35s",
    "2024-04-12 10:05:11 INFO TaskScheduler: TASK_START id=123 type=backup",
    "2024-04-12 10:05:40 ERROR TaskProcessor: TASK_FAIL id=123 reason=TIMEOUT",
    "2024-04-12 11:30:04 INFO TaskScheduler: TASK_START id=124 type=cleanup",
    "2024-04-12 11:30:05 ERROR TaskProcessor: TASK_FAIL id=124 reason=PERMISSION_DENIED",
    "2024-04-12 12:00:22 INFO TaskScheduler: TASK_START id=125 type=backup",
    "2024-04-12 12:00:52 INFO TaskProcessor: TASK_SUCCESS id=125 duration=30s",
    "2024-04-12 13:20:30 INFO TaskScheduler: TASK_START id=126 type=deploy",
    "2024-04-12 13:21:10 INFO TaskProcessor: TASK_SUCCESS id=126 duration=40s",
    "2024-04-12 14:44:55 INFO TaskScheduler: TASK_START id=127 type=cleanup",
    "2024-04-12 14:45:01 ERROR TaskProcessor: TASK_FAIL id=127 reason=NO_SPACE",
]


def _read_log_file():
    """
    Helper: read the full log file and return its
    *raw* text (including the final newline, if any).
    """
    try:
        return LOG_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required log file not found: {LOG_PATH}")
    except PermissionError:
        pytest.fail(f"Log file exists but is not readable: {LOG_PATH}")


def _diff(expected: str, actual: str) -> str:
    """
    Produce a unified diff between expected and actual content,
    to help the student quickly spot the discrepancy.
    """
    exp_lines = expected.splitlines(keepends=True)
    act_lines = actual.splitlines(keepends=True)
    return "".join(difflib.unified_diff(exp_lines, act_lines, fromfile="expected", tofile="actual"))


def test_log_file_exists_and_content_is_correct():
    """
    Verify that /home/user/logs/automation_events.log exists and contains the
    exact 16 lines stipulated in the exercise, followed by a single newline.
    """
    # 1. Read file (this already asserts existence & readability)
    raw_text = _read_log_file()

    # 2. Assert that the file ends with a single trailing newline
    assert raw_text.endswith(
        "\n"
    ), (
        f"{LOG_PATH} must end with a single UNIX newline (\\n). "
        "No CRLF or missing newline is allowed."
    )

    # 3. Split into lines *without* keeping the newline characters
    actual_lines = raw_text.rstrip("\n").split("\n")

    # 4. Compare number of lines first for a quick, helpful error
    assert len(actual_lines) == len(
        EXPECTED_LOG_LINES
    ), (
        f"{LOG_PATH} should contain exactly "
        f"{len(EXPECTED_LOG_LINES)} lines, but {len(actual_lines)} were found."
    )

    # 5. Compare full content
    expected_text = "\n".join(EXPECTED_LOG_LINES) + "\n"
    if raw_text != expected_text:
        diff = _diff(expected_text, raw_text)
        pytest.fail(
            "The content of /home/user/logs/automation_events.log does not match "
            "the expected initial state.\nDiff (expected → actual):\n"
            f"{diff}"
        )