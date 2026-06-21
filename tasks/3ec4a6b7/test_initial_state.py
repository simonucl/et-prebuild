# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
BEFORE the student performs any action for the “slow SQL statements” task.

This file must be placed at the repository root so the autograder can
simply call `pytest` and obtain these assertions.

Only the standard library and pytest are used.
"""

import os
from pathlib import Path

import pytest


# ---------- Constants describing the expected initial state -------------

HOME = Path("/home/user")
DB_DIR = HOME / "db"
LOG_DIR = DB_DIR / "logs"
SLOW_LOG = LOG_DIR / "slow_queries.log"

# The exact, line-by-line contents expected in the slow query log.
EXPECTED_LOG_LINES = [
    "SELECT * FROM users WHERE id = ?;\n",
    "SELECT * FROM users WHERE id = ?;\n",
    "SELECT * FROM users WHERE id = ?;\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "UPDATE users SET last_login = NOW() WHERE id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
]


# ------------------------------ Tests ------------------------------------


def test_log_directory_exists():
    """
    The directory /home/user/db/logs/ must exist prior to student action.
    """
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "Make sure the initial environment contains the log directory."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_slow_log_file_exists_and_is_file():
    """
    The log file /home/user/db/logs/slow_queries.log must exist and be a file.
    """
    assert SLOW_LOG.exists(), (
        f"Required log file {SLOW_LOG} is missing. "
        "Ensure the initial dataset is in place."
    )
    assert SLOW_LOG.is_file(), f"{SLOW_LOG} exists but is not a regular file."


def test_slow_log_contents_are_exact():
    """
    The slow_queries.log file should contain exactly the 10 expected lines,
    each terminated by a single Unix LF (\\n).
    """
    with SLOW_LOG.open("rb") as fp:
        data = fp.read()

    # Verify no Windows CRLF characters are present.
    assert b"\r" not in data, (
        f"{SLOW_LOG} contains CR (\\r) characters; should be plain Unix LF."
    )

    actual_lines = data.decode("utf-8").splitlines(keepends=True)

    assert actual_lines == EXPECTED_LOG_LINES, (
        "The contents of slow_queries.log differ from the expected initial "
        "state.\n\n"
        "Expected lines:\n"
        + "".join(EXPECTED_LOG_LINES)
        + "\nActual lines:\n"
        + "".join(actual_lines)
    )


# Important DO NOT add tests for /home/user/db/reports or any output files.
# The student is responsible for creating those during task execution.