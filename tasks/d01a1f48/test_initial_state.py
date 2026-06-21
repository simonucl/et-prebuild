# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must
# be present *before* the student starts working on the task.  It checks:
#   1. Presence, permissions, and exact content of /home/user/data/usage.log
#   2. Absence of /home/user/analysis (the directory that the student
#      will later create)
#
# Any failure means the starting point is not as described in the
# specification and the exercise cannot be graded reliably.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

USAGE_LOG_PATH = Path("/home/user/data/usage.log")
ANALYSIS_DIR_PATH = Path("/home/user/analysis")

EXPECTED_USAGE_LOG_LINES = [
    "serverA 2023-07-01 24\n",
    "serverB 2023-07-01 67\n",
    "serverC 2023-07-01 53\n",
    "serverA 2023-07-02 21\n",
    "serverB 2023-07-02 79\n",
    "serverC 2023-07-02 48\n",
    "serverA 2023-07-03 35\n",
    "serverB 2023-07-03 73\n",
    "serverC 2023-07-03 64\n",
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _get_permission_bits(path: Path) -> int:
    """
    Return the Unix permission bits (e.g., 0o644) for the given path.
    """
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_usage_log_exists_and_has_correct_permissions():
    """/home/user/data/usage.log must exist with 644 permissions."""
    assert USAGE_LOG_PATH.exists(), (
        f"Required file not found: {USAGE_LOG_PATH}"
    )
    assert USAGE_LOG_PATH.is_file(), (
        f"Expected {USAGE_LOG_PATH} to be a file, but it is not."
    )

    perms = _get_permission_bits(USAGE_LOG_PATH)
    expected_perms = 0o644
    assert perms == expected_perms, (
        f"Incorrect permissions on {USAGE_LOG_PATH} — "
        f"expected 0o{expected_perms:o}, found 0o{perms:o}."
    )


def test_usage_log_content_exactly_matches_specification():
    """
    The content of /home/user/data/usage.log must match the 9 lines
    specified in the task description, each terminated by a single LF.
    """
    with USAGE_LOG_PATH.open("rb") as fh:
        content = fh.read()

    # Decode safely assuming ASCII digits/letters/spaces only
    text = content.decode("utf-8")

    # Ensure the file ends with exactly one newline (LF)
    assert text.endswith("\n"), (
        f"{USAGE_LOG_PATH} must end with a single LF newline character."
    )

    # Split lines retaining newline characters for exact comparison
    lines = text.splitlines(keepends=True)
    assert lines == EXPECTED_USAGE_LOG_LINES, (
        f"Content of {USAGE_LOG_PATH} does not match the expected "
        f"9-line specification.\n\nExpected:\n{''.join(EXPECTED_USAGE_LOG_LINES)}\n"
        f"Found:\n{''.join(lines)}"
    )


def test_analysis_directory_does_not_exist_yet():
    """
    The directory /home/user/analysis must NOT exist before the student
    runs their solution.
    """
    assert not ANALYSIS_DIR_PATH.exists(), (
        f"The directory {ANALYSIS_DIR_PATH} should not exist initially. "
        "It will be created by the student's solution."
    )