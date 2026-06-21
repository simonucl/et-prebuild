# test_initial_state.py
#
# This pytest suite verifies that the operating-system state is correct
# *before* any student action is taken.  It checks that the original
# weekly report is present exactly as described and that no compressed
# copy exists yet.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
CAPACITY_DIR = HOME / "capacity"
CSV_FILE = CAPACITY_DIR / "weekly_report.csv"
GZ_FILE = CAPACITY_DIR / "weekly_report.csv.gz"

EXPECTED_CSV_CONTENT = (
    "week,start,end,cpu_usage_pct,mem_usage_pct\n"
    "23,2024-06-03,2024-06-09,57.3,62.1\n"
    "24,2024-06-10,2024-06-16,59.8,63.7\n"
    "25,2024-06-17,2024-06-23,61.2,65.4\n"
    "26,2024-06-24,2024-06-30,60.0,64.0\n"
)  # Note: final newline is significant.


def test_capacity_directory_exists_and_permissions():
    """Directory /home/user/capacity must exist and be a directory."""
    assert CAPACITY_DIR.exists(), f"Missing directory: {CAPACITY_DIR}"
    assert CAPACITY_DIR.is_dir(), f"{CAPACITY_DIR} exists but is not a directory"

    # Check that directory permissions are at least 0o755.
    # Exact permissions can vary by environment; we ensure user read/write/execute
    mode = stat.S_IMODE(CAPACITY_DIR.stat().st_mode)
    required_bits = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR  # 0o700 essential bits
    assert mode & required_bits == required_bits, (
        f"Directory {CAPACITY_DIR} permissions are {oct(mode)}, "
        "expected user read/write/execute (>= 0o700)."
    )


def test_weekly_report_csv_exists_and_content_and_permissions():
    """Verify the weekly_report.csv file exists, permissions are sane, and content matches exactly."""
    assert CSV_FILE.exists(), f"Missing file: {CSV_FILE}"
    assert CSV_FILE.is_file(), f"{CSV_FILE} exists but is not a regular file"

    # Check file permissions are at least 0o644 (readable by everyone, writable by owner)
    mode = stat.S_IMODE(CSV_FILE.stat().st_mode)
    required_bits = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH  # 0o644
    assert mode & required_bits == required_bits, (
        f"File {CSV_FILE} permissions are {oct(mode)}, "
        "expected at least read/write for owner and read for group/others (>= 0o644)."
    )

    # Read and compare content exactly (including final newline)
    data = CSV_FILE.read_text(encoding="utf-8")
    assert data == EXPECTED_CSV_CONTENT, (
        f"Content of {CSV_FILE} does not match expected template.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{data!r}"
    )


def test_gzip_file_does_not_exist_yet():
    """Before running the student's command, the compressed file must NOT exist."""
    assert not GZ_FILE.exists(), (
        f"Compressed file {GZ_FILE} already exists before the exercise starts. "
        "It should be created by the student's command."
    )