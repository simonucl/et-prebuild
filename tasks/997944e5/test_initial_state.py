# test_initial_state.py
#
# This pytest suite validates that the workstation is in the correct
# initial state *before* the student performs any actions.
#
# Checked items
# 1. The log directory /home/user/audit/logs/ exists.
# 2. The file /home/user/audit/logs/access.log exists.
# 3. access.log contains exactly the 12 expected lines (with a trailing
#    newline on the last line).
#
# NOTE: Per the grading rules, we purposefully do NOT look for any file
#       under /home/user/audit/reports/ because that is the artefact the
#       student is asked to create.

import os
from pathlib import Path

import pytest

LOG_DIR = Path("/home/user/audit/logs")
LOG_FILE = LOG_DIR / "access.log"

EXPECTED_LINES = [
    "2023-10-01 12:00:01 userA login success",
    "2023-10-01 12:00:05 userB login success",
    "2023-10-01 12:02:11 userA login success",
    "2023-10-01 12:05:41 userC login success",
    "2023-10-01 12:15:00 userA login success",
    "2023-10-01 12:20:22 userB login success",
    "2023-10-01 12:30:33 userD login success",
    "2023-10-01 12:45:54 userB login success",
    "2023-10-01 12:50:01 userE login success",
    "2023-10-01 13:00:11 userC login success",
    "2023-10-01 13:05:19 userB login success",
    "2023-10-01 13:15:45 userB login success",
]


def test_log_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Required directory '{LOG_DIR}' is missing. "
        "Ensure the audit log directory exists with the correct path."
    )


def test_access_log_exists():
    assert LOG_FILE.is_file(), (
        f"Required file '{LOG_FILE}' is missing. "
        "The initial log file must be present before any processing begins."
    )


def test_access_log_contents():
    """
    The access.log file must contain exactly the 12 provided lines
    (each ending in a newline) and nothing else.
    """
    # Read the file in binary mode first to check for trailing newline
    with LOG_FILE.open("rb") as fh:
        raw = fh.read()
    assert raw.endswith(b"\n"), (
        f"The file '{LOG_FILE}' must have a trailing newline on the last line."
    )

    # Now read line-by-line for textual comparison
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Strip the newline character for comparison convenience
    stripped_lines = [ln.rstrip("\n") for ln in lines]

    assert (
        len(stripped_lines) == len(EXPECTED_LINES)
    ), f"Expected {len(EXPECTED_LINES)} lines in '{LOG_FILE}', found {len(stripped_lines)}."

    for idx, (found, expected) in enumerate(zip(stripped_lines, EXPECTED_LINES), start=1):
        assert (
            found == expected
        ), (
            f"Line {idx} in '{LOG_FILE}' is incorrect.\n"
            f"Expected: '{expected}'\n"
            f"Found:    '{found}'"
        )

    # Ensure no extra lines beyond the expected list
    assert stripped_lines == EXPECTED_LINES, (
        f"The file '{LOG_FILE}' contains unexpected extra or missing lines."
    )