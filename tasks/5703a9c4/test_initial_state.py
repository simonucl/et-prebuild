# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state **before** the student starts working on the task.
#
# Requirements verified:
#   • /home/user/logs/ exists and is a directory
#   • It contains exactly one file: app.log
#   • /home/user/logs/app.log exists, is a regular file and its contents
#     match the seven expected log lines (including trailing "\n")
#   • /home/user/output/ does NOT exist yet
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
APP_LOG = LOGS_DIR / "app.log"
OUTPUT_DIR = HOME / "output"


EXPECTED_APP_LOG_LINES = [
    "2023-07-15 13:59:58,123 INFO auth - User login successful: user_id=15\n",
    "2023-07-15 14:00:02,456 ERROR db - Connection timeout to replica set\n",
    "2023-07-15 14:05:34,789 WARNING cache - Cache miss for key=session_42\n",
    "2023-07-15 14:15:03,101 CRITICAL api - Null pointer dereference in handler /api/data\n",
    "2023-07-15 14:45:00,000 INFO scheduler - Task completed: daily_sync\n",
    "2023-07-15 15:00:01,987 ERROR auth - Token expired for user_id=38\n",
    "2023-07-15 15:05:22,333 INFO api - Request processed in 120ms\n",
]


def test_logs_directory_exists_and_is_correct():
    assert LOGS_DIR.exists(), f"Required directory '{LOGS_DIR}' is missing."
    assert LOGS_DIR.is_dir(), f"'{LOGS_DIR}' exists but is not a directory."

    entries = sorted(p.name for p in LOGS_DIR.iterdir())
    assert entries == ["app.log"], (
        f"'{LOGS_DIR}' should contain exactly one file named 'app.log'. "
        f"Found: {entries}"
    )


def test_app_log_file_exists_and_contents_are_exact():
    assert APP_LOG.exists(), f"Required file '{APP_LOG}' is missing."
    assert APP_LOG.is_file(), f"'{APP_LOG}' exists but is not a regular file."

    # Read the file, preserving newlines
    with APP_LOG.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Verify the content matches exactly (order, number of lines, and trailing '\n')
    assert (
        lines == EXPECTED_APP_LOG_LINES
    ), (
        f"Contents of '{APP_LOG}' do not match the expected initial log lines.\n"
        f"Expected ({len(EXPECTED_APP_LOG_LINES)} lines):\n{''.join(EXPECTED_APP_LOG_LINES)}\n"
        f"Actual ({len(lines)} lines):\n{''.join(lines)}"
    )


def test_output_directory_absent():
    assert not OUTPUT_DIR.exists(), (
        f"Output directory '{OUTPUT_DIR}' should NOT exist before the student "
        "performs any actions."
    )