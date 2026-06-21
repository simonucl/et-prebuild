# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state for the “SSH failed-login burst” incident-response task.
#
# This file must be executed *before* the student performs any action.
# It checks that:
#   1. The reduced authentication log exists at the expected absolute path.
#   2. The log’s contents are exactly the eight lines described in the task
#      (including their line-ending structure).
#   3. The output file that the student must eventually create does *not*
#      yet exist.  This guarantees the test validates the pristine state.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_FILE = HOME / "logs" / "incident.log"
OUTPUT_FILE = HOME / "output" / "ip_frequency.txt"

# --------------------------------------------------------------------------- #
# Expected ground-truth contents of /home/user/logs/incident.log
# (The task description guarantees LF line endings, no trailing blank line.)

EXPECTED_LOG_LINES = [
    "Feb  7 10:15:32 server sshd[2234]: Failed password for invalid user admin from 192.168.1.10 port 53422 ssh2\n",
    "Feb  7 10:15:35 server sshd[2235]: Failed password for invalid user root from 203.0.113.55 port 53423 ssh2\n",
    "Feb  7 10:15:38 server sshd[2236]: Failed password for invalid user admin from 192.168.1.10 port 53424 ssh2\n",
    "Feb  7 10:15:40 server sshd[2237]: Failed password for invalid user guest from 198.51.100.23 port 53425 ssh2\n",
    "Feb  7 10:15:42 server sshd[2238]: Failed password for invalid user admin from 192.0.2.44 port 53426 ssh2\n",
    "Feb  7 10:15:45 server sshd[2239]: Failed password for invalid user root from 203.0.113.55 port 53427 ssh2\n",
    "Feb  7 10:15:48 server sshd[2240]: Failed password for invalid user admin from 192.168.1.10 port 53428 ssh2\n",
    "Feb  7 10:15:50 server sshd[2241]: Failed password for invalid user admin from 198.51.100.23 port 53429 ssh2\n",
]
# --------------------------------------------------------------------------- #


def test_log_file_exists():
    """The reduced authentication log must exist at the exact absolute path."""
    assert LOG_FILE.is_file(), (
        f"Required log file not found: {LOG_FILE}. "
        "Verify that the file is present before beginning the task."
    )


def test_log_file_contents_are_exact():
    """
    Validate that the log file contains the exact eight expected lines
    with LF line endings and no extra blank lines.
    """
    with LOG_FILE.open("r", encoding="utf-8") as fp:
        actual_lines = fp.readlines()

    # Helpful debug information if something is wrong.
    assert actual_lines == EXPECTED_LOG_LINES, (
        "The contents of /home/user/logs/incident.log do not match the expected "
        "ground-truth data provided in the assignment description.\n"
        f"Expected {len(EXPECTED_LOG_LINES)} lines, got {len(actual_lines)}.\n"
        "Differences (first mismatch shown below):\n"
        + _first_difference(EXPECTED_LOG_LINES, actual_lines)
    )


def _first_difference(expected, actual):
    """
    Returns a short string describing the first line number where the two
    sequences differ.  Used solely for more helpful assertion messages.
    """
    for idx, (exp, act) in enumerate(zip(expected, actual)):
        if exp != act:
            return (
                f"Line {idx+1} expected:\n    {repr(exp)}\n"
                f"but got:\n    {repr(act)}"
            )
    if len(expected) != len(actual):
        return "File lengths differ."
    return "No differences found (this should not happen)."


def test_output_file_does_not_exist_yet():
    """
    The student has not yet run their solution, so the result file must *not*
    be present.  Its existence would indicate that the environment has already
    been modified.
    """
    assert not OUTPUT_FILE.exists(), (
        f"Output file {OUTPUT_FILE} already exists. "
        "The initial-state test expects the environment to be untouched. "
        "Remove or rename the file before starting the exercise."
    )