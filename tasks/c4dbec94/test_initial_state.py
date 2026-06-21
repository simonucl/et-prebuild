# test_initial_state.py
#
# Pytest suite that validates the starting state of the filesystem
# BEFORE the student performs any actions for the “API stability
# problems” exercise.
#
# Only the initial log file and its parent directories are checked,
# as per the task requirements.  No assertions are made about any
# output artefacts that the student is expected to create later.

import os
from pathlib import Path

import pytest

# Constants -------------------------------------------------------------------

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
LOGS_DIR = PROJECT_DIR / "logs"
ACCESS_LOG = LOGS_DIR / "api_access.log"

EXPECTED_LINES = [
    "2023-04-15T09:59:12Z [REQ0001] GET /health 200 23\n",
    "2023-04-15T10:00:01Z [REQ0002] POST /login 200 345\n",
    "2023-04-15T10:15:32Z [REQ0003] GET /users 200 134\n",
    "2023-04-15T10:16:05Z [REQ0004] GET /users/42 404 56\n",
    "2023-04-15T10:20:45Z [REQ0005] POST /orders 500 678\n",
    "2023-04-15T10:21:12Z [REQ0006] GET /orders/99 200 2451\n",
    "2023-04-15T10:22:30Z [REQ0007] GET /metrics 200 78\n",
    "2023-04-15T11:03:19Z [REQ0008] PUT /users/42 200 3120\n",
    "2023-04-15T11:10:00Z [REQ0009] DELETE /orders/12 204 89\n",
    "2023-04-16T08:00:01Z [REQ0010] GET /health 200 25\n",
    "2023-04-16T08:05:45Z [REQ0011] POST /login 400 48\n",
    "2023-04-16T09:30:22Z [REQ0012] POST /orders 201 92\n",
    "2023-04-16T09:45:12Z [REQ0013] GET /users 503 158\n",
]

# Tests -----------------------------------------------------------------------


def test_directories_exist():
    """Ensure the expected directory hierarchy is present."""
    assert PROJECT_DIR.is_dir(), (
        f"Required directory {PROJECT_DIR} is missing."
    )
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} is missing."
    )


def test_access_log_exists_and_has_expected_content():
    """
    Validate that api_access.log exists, ends with a newline, has exactly
    13 lines, and every line matches the canonical fixture provided in the
    task description.
    """
    assert ACCESS_LOG.is_file(), (
        f"Expected log file {ACCESS_LOG} is missing."
    )

    # Read file in binary to make newline check unambiguous
    data = ACCESS_LOG.read_bytes()
    assert data.endswith(b"\n"), (
        f"{ACCESS_LOG} must end with a single LF (\\n)."
    )

    # Decode safely; ASCII is enough for the given content
    content = data.decode("ascii")
    lines = content.splitlines(keepends=True)

    assert len(lines) == 13, (
        f"{ACCESS_LOG} must contain exactly 13 lines; found {len(lines)}."
    )

    # Compare line-by-line so the assertion reports the first mismatch
    for idx, (found, expected) in enumerate(zip(lines, EXPECTED_LINES), start=1):
        assert found == expected, (
            f"Mismatch on line {idx} of {ACCESS_LOG}:\n"
            f"  expected: {expected.rstrip()!r}\n"
            f"  found   : {found.rstrip()!r}"
        )