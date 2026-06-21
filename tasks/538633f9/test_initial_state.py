# test_initial_state.py
"""
Pytest suite that verifies the **initial** state of the operating system / filesystem
before the student performs any action for the “capacity-planner” exercise.

Checks performed:
1. The working directory /home/user/capacity_tasks exists.
2. /home/user/capacity_tasks/resource_usage.csv exists and contains the exact
   expected 4-line CSV (including trailing newline at the end of each line).
3. The files that the student is supposed to create **do not** exist yet:
   - /home/user/capacity_tasks/resource_usage.csv.gpg
   - /home/user/capacity_tasks/gpg_result.log
"""

import os
import pathlib
import pytest

HOME_DIR = pathlib.Path("/home/user")
TASK_DIR = HOME_DIR / "capacity_tasks"

CSV_FILE = TASK_DIR / "resource_usage.csv"
GPG_FILE = TASK_DIR / "resource_usage.csv.gpg"
LOG_FILE = TASK_DIR / "gpg_result.log"

EXPECTED_CSV_CONTENT = (
    "timestamp,cpu_usage_percent,memory_usage_mb\n"
    "2024-06-01T00:00:00Z,32,2048\n"
    "2024-06-01T01:00:00Z,45,3072\n"
    "2024-06-01T02:00:00Z,29,1984\n"
)


def test_task_directory_exists():
    assert TASK_DIR.is_dir(), (
        f"Required directory missing: {TASK_DIR!s}\n"
        "Create the directory structure exactly as specified."
    )


def test_csv_file_exists_with_correct_content():
    assert CSV_FILE.is_file(), (
        f"Required CSV file missing: {CSV_FILE!s}\n"
        "Make sure the plain-text data file is present before proceeding."
    )

    # Read as text with default UTF-8; content is ASCII only.
    with CSV_FILE.open("r", encoding="utf-8") as f:
        content = f.read()

    assert content == EXPECTED_CSV_CONTENT, (
        f"Contents of {CSV_FILE!s} do not match the expected 4-line CSV.\n"
        "Ensure the file has exactly the following lines (with trailing newlines):\n"
        + EXPECTED_CSV_CONTENT
    )


def test_encrypted_file_not_present_yet():
    assert not GPG_FILE.exists(), (
        f"Encrypted file {GPG_FILE!s} already exists before the task starts.\n"
        "The .gpg file should be created only after running the encryption command."
    )


def test_log_file_not_present_yet():
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE!s} already exists before the task starts.\n"
        "The log should be generated only after successful encryption."
    )