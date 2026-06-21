# test_initial_state.py
"""
Pytest suite that validates the OS / filesystem state *before* the student
performs any action for the “failed authentication” investigation exercise.

Checks performed (and only these):
1. /home/user/logs/failed_logins.csv exists and is a regular file.
2. The file’s exact byte-for-byte contents match the canonical fixture that
   the task description guarantees.

Nothing related to the output artefacts (/home/user/analysis/…) is tested here,
per the problem-authoring rules.
"""

import os
import pytest

FILE_PATH = "/home/user/logs/failed_logins.csv"

# The canonical content, including the single trailing newline.
EXPECTED_CONTENT = (
    "user,timestamp,ip,reason\n"
    "alice,2023-08-21T12:05:34Z,192.168.1.45,invalid_password\n"
    "bob,2023-08-21T12:06:02Z,192.168.1.45,invalid_password\n"
    "carol,2023-08-21T12:10:11Z,10.0.0.3,account_locked\n"
    "dan,2023-08-21T12:11:47Z,10.0.0.3,invalid_password\n"
    "erin,2023-08-21T12:12:33Z,192.168.1.100,invalid_password\n"
    "frank,2023-08-21T12:13:01Z,10.0.0.3,invalid_password\n"
)


def test_failed_logins_csv_exists():
    """
    The source log CSV must already be present; otherwise the exercise
    instructions cannot be followed.
    """
    assert os.path.isfile(
        FILE_PATH
    ), f"Required log file not found at expected path: {FILE_PATH!r}"


def test_failed_logins_csv_contents_are_exact():
    """
    Verify the log file still matches the pristine fixture.  Any deviation
    indicates accidental modification or corruption, both of which would
    invalidate subsequent grading.
    """
    with open(FILE_PATH, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == EXPECTED_CONTENT
    ), (
        f"Contents of {FILE_PATH} do not match the expected fixture.\n"
        "Ensure the file is unmodified before proceeding."
    )