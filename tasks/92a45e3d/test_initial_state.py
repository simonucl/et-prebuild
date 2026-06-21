# test_initial_state.py
#
# Pytest suite to verify the **initial** filesystem state for
# the “Lightweight on-call log backup” exercise.
#
# These tests assert that:
#   1. /home/user/capacity/logs/ exists and is correctly populated.
#   2. The three expected *.log files are present with the exact
#      sizes and contents stated in the task description.
#   3. No backup artefacts are present yet
#      (/home/user/capacity/backup/ directory or its files).

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
CAPACITY_DIR = HOME / "capacity"
LOGS_DIR = CAPACITY_DIR / "logs"
BACKUP_DIR = CAPACITY_DIR / "backup"

EXPECTED_FILES = {
    "app.log": b"APP_LOG_SAMPLE\n",
    "db.log": b"DB_LOG_SAMPLE\n",
    "sys.log": b"SYS_LOG_SAMPLE\n",
}


def _read_bytes(path: Path) -> bytes:
    """Utility: read file as raw bytes."""
    with path.open("rb") as fh:
        return fh.read()


def test_logs_directory_exists():
    assert LOGS_DIR.exists(), (
        f"Required directory {LOGS_DIR} is missing. "
        "It should exist before students start the exercise."
    )
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory."


def test_expected_log_files_present_and_correct():
    actual_log_files = {p.name for p in LOGS_DIR.glob("*.log")}
    expected_set = set(EXPECTED_FILES)
    missing = expected_set - actual_log_files
    unexpected = actual_log_files - expected_set

    assert not missing, (
        "The following required log files are missing in "
        f"{LOGS_DIR}: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        f"Unexpected .log files found in {LOGS_DIR}: "
        f"{', '.join(sorted(unexpected))}. Only "
        f"{', '.join(sorted(expected_set))} should be present."
    )

    # Validate size and content of each file
    for filename, expected_bytes in EXPECTED_FILES.items():
        path = LOGS_DIR / filename
        assert path.is_file(), f"Expected {path} to be a regular file."
        actual_size = path.stat().st_size
        expected_size = len(expected_bytes)
        assert (
            actual_size == expected_size
        ), f"{filename} size mismatch: expected {expected_size} bytes, got {actual_size} bytes."
        actual_bytes = _read_bytes(path)
        assert (
            actual_bytes == expected_bytes
        ), f"Contents of {filename} do not match expected placeholder text."


def test_no_backup_directory_yet():
    assert not BACKUP_DIR.exists(), (
        f"Directory {BACKUP_DIR} should NOT exist before the student runs "
        "their solution, but it does."
    )

    tar_file = BACKUP_DIR / "logs_backup.tar.gz"
    report_file = BACKUP_DIR / "capacity_report.txt"

    # Even if the backup dir accidentally exists, ensure no artefacts exist.
    assert not tar_file.exists(), f"Backup archive {tar_file} should not exist yet."
    assert not report_file.exists(), f"Report file {report_file} should not exist yet."