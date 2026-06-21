# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student generates the daily summary.
#
# Rules enforced:
#   • Uses only Python stdlib + pytest
#   • Verifies that the raw log file exists with the exact expected
#     contents
#   • Verifies that the summary file does NOT yet exist
#
# If any assertion fails, the error message clearly describes the
# missing or unexpected element.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_PATH = HOME / "repo-activity.log"
SUMMARY_PATH = HOME / "daily_summary_2023-08-15.txt"


@pytest.fixture(scope="module")
def expected_log_lines():
    """
    Lines that must be present in /home/user/repo-activity.log
    (exactly and in the same order).
    """
    return [
        "2023-08-14 21:34:11 libs-release com.example:foo:0.9.0 UPLOAD",
        "2023-08-15 00:05:22 libs-snapshot com.example:bar:2.0.0-SNAPSHOT UPLOAD",
        "2023-08-15 01:45:10 libs-release com.example:foo:1.0.0 UPLOAD",
        "2023-08-15 02:10:05 libs-release com.example:foo:1.0.0 DELETE",
        "2023-08-15 08:22:33 plugins-release com.company:plugin:3.1.4 UPLOAD",
        "2023-08-15 09:10:00 plugins-release com.company:plugin:3.1.3 DELETE",
        "2023-08-16 10:00:00 libs-snapshot com.example:bar:2.0.1-SNAPSHOT UPLOAD",
    ]


def test_log_file_exists_and_content(expected_log_lines):
    """
    Ensure the raw log file exists, is readable, and contains the
    exact expected lines (nothing more, nothing less).
    """
    assert LOG_PATH.exists(), f"Required log file not found at: {LOG_PATH}"
    assert LOG_PATH.is_file(), f"Expected a file at {LOG_PATH}, but found something else."

    with LOG_PATH.open("r", encoding="utf-8") as fh:
        contents = [line.rstrip("\n") for line in fh]

    assert (
        contents == expected_log_lines
    ), (
        "The contents of the log file do not match the expected initial state.\n\n"
        "Expected lines:\n"
        + "\n".join(expected_log_lines)
        + "\n\nActual lines:\n"
        + "\n".join(contents)
    )


def test_summary_file_absent_initially():
    """
    The daily summary must NOT exist before the student performs the task.
    """
    assert not SUMMARY_PATH.exists(), (
        f"Summary file '{SUMMARY_PATH}' is present before the task is performed; "
        "it should be created by the student."
    )