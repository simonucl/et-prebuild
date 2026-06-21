# test_initial_state.py
"""
Pytest suite that validates the machine state *before* the student performs any
actions for the “backup-integrity” exercise.

What we verify:
1. The raw backup log exists at the expected absolute path.
2. The containing directory hierarchy already exists.
3. The log file’s contents are **exactly** what the downstream tests expect.
   (If the content is even one character off, the student’s later parsing
   logic would produce the wrong report.)

We intentionally do NOT look for the /home/user/backup/reports/ directory or
the summary report file, because they are outputs the student must create.
"""

import os
import pytest
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants describing the canonical initial state.                           #
# --------------------------------------------------------------------------- #
LOG_PATH = Path("/home/user/backup/logs/backup_20230815.log")

EXPECTED_LINES = [
    "[2023-08-15 00:01:02] INFO  Starting backup job id=42",
    "[2023-08-15 00:01:05] INFO  Scanning files to backup",
    "[2023-08-15 00:03:12] WARN  File /var/data/tmp/cache.dat skipped (permission denied)",
    "[2023-08-15 00:05:55] ERROR Unable to open /var/data/important.db (I/O error)",
    "[2023-08-15 00:06:10] INFO  Retrying missing files",
    "[2023-08-15 00:07:25] WARN  Checksum mismatch ignored for /var/data/old.log",
    "[2023-08-15 00:08:30] ERROR Failed to write to backup destination (disk full)",
    "[2023-08-15 00:10:00] INFO  Backup job ended",
]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_log_file_exists():
    """The raw backup log file must be present at the exact path specified."""
    assert LOG_PATH.exists(), (
        f"Required log file not found: {LOG_PATH}. "
        "The exercise cannot proceed without this file."
    )
    assert LOG_PATH.is_file(), f"Expected {LOG_PATH} to be a file, not a directory."


def test_directory_structure():
    """Ensure that the expected parent directories are present."""
    assert LOG_PATH.parent.exists(), (
        f"Directory missing: {LOG_PATH.parent}. "
        "The logs/ directory must exist so the student can read the log."
    )
    assert LOG_PATH.parent.is_dir(), f"{LOG_PATH.parent} exists but is not a directory."


def test_log_file_contents_are_exact():
    """
    Validate that the log file content exactly matches the canonical test data.

    Any deviation—even extra whitespace—would break the downstream parsing
    logic that the exercise is about.
    """
    with LOG_PATH.open("r", encoding="utf-8") as fh:
        file_lines = [line.rstrip("\n") for line in fh]

    assert file_lines == EXPECTED_LINES, (
        "The contents of the backup log do not match the expected fixture.\n"
        "Differences:\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual ({len(file_lines)} lines):\n"
        + "\n".join(file_lines)
    )