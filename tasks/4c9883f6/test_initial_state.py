# test_initial_state.py
#
# This pytest suite validates that the machine starts in the exact state
# described in the task instructions—BEFORE the student performs any action.
#
# What is checked:
#   1. The directory /home/user/ci_cd/logs/ exists *and* contains exactly
#      three plain-text log files: stage1.log, stage2.log, stage3.log
#   2. Each log file’s content matches the specification.
#   3. No extra files or sub-directories are present inside
#      /home/user/ci_cd/logs/.
#   4. The directory /home/user/backups/ exists and is completely empty.
#
# Nothing related to the deliverables (/home/user/backups/ci_logs_backup.tar.gz
# and /home/user/backups/backup_report.txt) is tested here—only the initial
# state is inspected.

import os
from pathlib import Path
import pytest

LOGS_DIR = Path("/home/user/ci_cd/logs")
BACKUPS_DIR = Path("/home/user/backups")
EXPECTED_LOG_FILES = {
    "stage1.log": "Stage 1 completed\n",
    "stage2.log": "Stage 2 completed\n",
    "stage3.log": "Stage 3 completed\n",
}


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        "Required directory '/home/user/ci_cd/logs/' is missing. "
        "Create it and place the three log files inside."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_LOG_FILES.items())
def test_each_expected_log_file_exists_with_correct_content(filename, expected_content):
    file_path = LOGS_DIR / filename
    assert file_path.is_file(), (
        f"Expected log file '{file_path}' is missing."
    )

    actual_content = file_path.read_text(encoding="utf-8")
    assert actual_content == expected_content, (
        f"Content mismatch in '{file_path}'.\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(actual_content)}"
    )


def test_no_extra_items_in_logs_directory():
    actual_items = {item.name for item in LOGS_DIR.iterdir()}
    expected_items = set(EXPECTED_LOG_FILES.keys())
    assert actual_items == expected_items, (
        "The directory '/home/user/ci_cd/logs/' must contain ONLY the three "
        "specified log files.\n"
        f"Expected items: {sorted(expected_items)}\n"
        f"Found items:    {sorted(actual_items)}"
    )


def test_backups_directory_exists_and_is_empty():
    assert BACKUPS_DIR.is_dir(), (
        "Directory '/home/user/backups/' must exist before the task starts."
    )

    # Gather both files and directories inside /home/user/backups
    entries = [entry.name for entry in BACKUPS_DIR.iterdir()]
    assert entries == [], (
        "Directory '/home/user/backups/' should be empty before the task "
        "starts, but the following items were found:\n"
        f"{entries}"
    )