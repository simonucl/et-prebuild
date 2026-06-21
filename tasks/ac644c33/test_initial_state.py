# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the container
# for the “login-success audit” exercise.  These tests intentionally
# FAIL if anything that the student is expected to create already
# exists, or if the provided raw log is missing / malformed.

import os
from pathlib import Path
import re
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
LOG_FILE = LOG_DIR / "auth_2023-01-07.log"

AUDIT_DIR = HOME / "audit"
OUTPUT_CSV = AUDIT_DIR / "login_success_2023-01-07.csv"


@pytest.fixture(scope="module")
def log_lines():
    """Read the raw log file and return a list of its lines (with newlines)."""
    if not LOG_FILE.exists():
        pytest.fail(
            f"Expected log file {LOG_FILE} is missing.  "
            "The exercise requires this file to be present."
        )

    if not LOG_FILE.is_file():
        pytest.fail(f"{LOG_FILE} exists but is not a regular file.")

    # Use universal newline mode to avoid surprises, then normalise to '\n'.
    with LOG_FILE.open("r", newline="") as f:
        raw = f.read()

    # Canonicalise line endings to LF and re-split.
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    # Guarantee final newline-terminated lines for comparison.
    if raw and not raw.endswith("\n"):
        pytest.fail(
            f"{LOG_FILE} does not end with a single LF newline. "
            "All lines—including the last—must be LF-terminated."
        )

    return [ln + "\n" for ln in raw.splitlines()]


def test_log_file_structure(log_lines):
    """The log file must have exactly the seven expected lines."""
    expected_lines = [
        "2023-01-07 09:12:45 | user=jdoe   | action=LOGIN     | status=SUCCESS\n",
        "2023-01-07 09:13:20 | user=jdoe   | action=LOGOUT    | status=SUCCESS\n",
        "2023-01-07 10:05:12 | user=asmith | action=LOGIN     | status=SUCCESS\n",
        "2023-01-07 11:15:55 | user=asmith | action=DOWNLOAD  | file=report.pdf | status=SUCCESS\n",
        "2023-01-07 12:45:06 | user=mbrown | action=LOGIN     | status=SUCCESS\n",
        "2023-01-07 16:02:11 | user=mbrown | action=LOGIN     | status=FAILED\n",
        "2023-01-07 17:00:35 | user=admin  | action=DELETE    | target=userdata | status=SUCCESS\n",
    ]

    assert (
        log_lines == expected_lines
    ), (
        f"{LOG_FILE} content differs from the specification.\n"
        "If the file was modified, restore it exactly as provided in "
        "the task description."
    )


def _extract_successful_logins(lines):
    """
    Helper that parses the raw log and yields (timestamp, username)
    for each ‘LOGIN’ with status SUCCESS, *in order*.
    """
    pattern = re.compile(
        r"""
        ^
        (?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})   # timestamp
        \s+\|\s+user=(?P<user>[^\s|]+)                  # username (no spaces or pipe)
        .*?                                             # anything (non-greedy)
        \|\s+action=LOGIN\s+                            # action must be LOGIN
        .*?                                             # anything
        \|\s+status=SUCCESS                             # status must be SUCCESS
        \s*                                             # optional trailing spaces
        $
        """,
        re.VERBOSE,
    )

    for line in lines:
        m = pattern.match(line.rstrip("\n"))
        if m:
            yield m.group("ts"), m.group("user")


def test_successful_login_events(log_lines):
    """
    Confirm that exactly three successful LOGIN events exist in the
    provided log and that their data match the exercise narrative.
    This protects against tampering before the student starts work.
    """
    expected = [
        ("2023-01-07 09:12:45", "jdoe"),
        ("2023-01-07 10:05:12", "asmith"),
        ("2023-01-07 12:45:06", "mbrown"),
    ]

    found = list(_extract_successful_logins(log_lines))
    assert (
        found == expected
    ), (
        "The successful LOGIN events in the raw log do not match the "
        "expected data.  Ensure the original log file is intact."
    )


def test_output_csv_not_present_yet():
    """
    The CSV the student must create should *not* exist before any
    work is done.  If it is already present, the environment is in an
    unexpected state.
    """
    assert not OUTPUT_CSV.exists(), (
        f"Output file {OUTPUT_CSV} already exists.  "
        "The exercise requires the student to create this file; "
        "it should not be present in the initial state."
    )

    # If the audit directory exists already, it must be a directory.
    if AUDIT_DIR.exists():
        assert AUDIT_DIR.is_dir(), f"{AUDIT_DIR} exists but is not a directory."