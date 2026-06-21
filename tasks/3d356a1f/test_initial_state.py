# test_initial_state.py
"""
Pytest suite that validates the **initial** filesystem state for the
“cleaning log” exercise.

The tests assert:
1. /home/user/project exists, is a directory, and is writable.
2. The directory contains exactly one regular file: cleaning.log.
3. cleaning.log has permissions 0644.
4. cleaning.log’s contents are byte-for-byte identical to the expected
   8-line log supplied in the task description.

If any assertion fails the accompanying message pin-points what is
missing or incorrect.
"""
import os
import stat
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
LOG_FILE = PROJECT_DIR / "cleaning.log"

# Expected log content (each line ends with '\n')
EXPECTED_LINES = [
    "2023-09-01 09:15:21,123 INFO Removed duplicate row id=3\n",
    "2023-09-01 09:15:22,456 INFO Replaced null price in row id=2 with mean=1.07\n",
    "2023-09-01 09:15:23,789 INFO Replaced null quantity in row id=4 with mean=8.25\n",
    "2023-09-01 09:15:24,012 INFO Replaced null price in row id=5 with mean=1.07\n",
    "2023-09-01 09:15:25,345 INFO Removed duplicate row id=7\n",
    "2023-09-01 09:15:26,678 INFO Replaced null price in row id=8 with mean=1.07\n",
    "2023-09-01 09:15:27,901 INFO Replaced null quantity in row id=9 with mean=8.25\n",
    "2023-09-01 09:15:29,234 INFO Replaced null quantity in row id=10 with mean=8.25\n",
]
EXPECTED_CONTENT = "".join(EXPECTED_LINES)


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected {PROJECT_DIR} to exist and be a directory, "
        "but it is missing or not a directory."
    )


def test_project_directory_writable():
    assert os.access(PROJECT_DIR, os.W_OK), (
        f"The directory {PROJECT_DIR} must be writable by the current user."
    )


def test_only_cleaning_log_present():
    files_in_dir = sorted(
        p.name for p in PROJECT_DIR.iterdir() if p.is_file()
    )
    assert files_in_dir == ["cleaning.log"], (
        f"Expected exactly one regular file 'cleaning.log' in {PROJECT_DIR}; "
        f"found: {files_in_dir}"
    )


def test_cleaning_log_permissions():
    mode = LOG_FILE.stat().st_mode & 0o777
    assert mode == 0o644, (
        f"{LOG_FILE} should have permissions 0644, but has {oct(mode)} instead."
    )


def test_cleaning_log_contents():
    actual_content = LOG_FILE.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_CONTENT, (
        f"The contents of {LOG_FILE} do not match the expected initial log.\n\n"
        "---- Expected ----\n"
        f"{EXPECTED_CONTENT}\n"
        "---- Actual ----\n"
        f"{actual_content}"
    )