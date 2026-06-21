# test_initial_state.py
#
# Pytest suite that verifies the initial state of the container *before* the
# student begins working on the assignment.
#
# What we check here:
# 1. Mandatory directory layout already provided by the grader is present.
# 2. Directories that the student is supposed to CREATE do *not* yet exist.
# 3. The three gzip-compressed log files exist in the expected locations.
# 4. The uncompressed *contents* of those files match the canonical truth that
#    the grader will later use for scoring.
# 5. Basic sanity on the data set: there are exactly eight
#    “01/Oct/2023 … 500” lines across all three logs.
#
# NOTE: Only stdlib + pytest are used—no third-party dependencies.

import gzip
from pathlib import Path

import pytest

# ---------
# Constants
# ---------
HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
RAW_DIR = LOGS_DIR / "raw"
PROCESSED_DIR = LOGS_DIR / "processed"
REPORTS_DIR = LOGS_DIR / "reports"

RAW_FILES = {
    RAW_DIR / "raw01.log.gz": [
        '127.0.0.1 - - [30/Sep/2023:23:59:59 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"',
        '192.168.1.10 - - [01/Oct/2023:00:00:01 +0000] "POST /api/login HTTP/1.1" 500 512 "-" "curl/7.68.0"',
        '10.0.0.5 - - [01/Oct/2023:00:05:21 +0000] "GET /api/order HTTP/1.1" 500 256 "-" "Mozilla/5.0"',
        '10.0.0.8 - - [01/Oct/2023:00:10:44 +0000] "GET /contact.html HTTP/1.1" 200 2048 "-" "Mozilla/5.0"',
        '192.168.1.10 - - [01/Oct/2023:01:15:07 +0000] "POST /api/login HTTP/1.1" 500 512 "-" "curl/7.68.0"',
    ],
    RAW_DIR / "raw02.log.gz": [
        '127.0.0.1 - - [01/Oct/2023:02:03:09 +0000] "GET /api/user HTTP/1.1" 500 300 "-" "Mozilla/5.0"',
        '127.0.0.1 - - [01/Oct/2023:02:04:10 +0000] "GET /api/user HTTP/1.1" 500 300 "-" "Mozilla/5.0"',
        '127.0.0.1 - - [01/Oct/2023:02:05:11 +0000] "GET /api/user HTTP/1.1" 500 300 "-" "Mozilla/5.0"',
        '10.0.0.6 - - [01/Oct/2023:03:00:00 +0000] "POST /api/login HTTP/1.1" 500 512 "-" "curl/7.68.0"',
        '10.0.0.7 - - [02/Oct/2023:00:00:01 +0000] "GET /api/user HTTP/1.1" 500 300 "-" "Mozilla/5.0"',
    ],
    RAW_DIR / "raw03.log.gz": [
        '10.0.0.10 - - [01/Oct/2023:04:10:44 +0000] "GET /api/order HTTP/1.1" 500 256 "-" "Mozilla/5.0"',
        '10.0.0.11 - - [01/Oct/2023:05:20:10 +0000] "GET /home HTTP/1.1" 200 1024 "-" "Mozilla/5.0"',
    ],
}

EXPECTED_TOTAL_500_01OCT2023 = 8


# ------------------------
# Helper / Utility Methods
# ------------------------
def read_gzip_lines(path: Path):
    """Return list[str] of lines without their trailing newline chars."""
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# ----------
# Test Suite
# ----------
def test_mandatory_directories_exist():
    """The grader guarantees /home/user/logs/ and /home/user/logs/raw/ exist."""
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} is missing; something is wrong with "
        "the base environment."
    )
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing; something is wrong with "
        "the base environment."
    )


def test_student_should_create_these_directories():
    """Directories that the student has to create MUST NOT exist yet."""
    assert not PROCESSED_DIR.exists(), (
        f"{PROCESSED_DIR} already exists, but it should be created by the "
        "student's solution, not pre-supplied."
    )
    assert not REPORTS_DIR.exists(), (
        f"{REPORTS_DIR} already exists, but it should be created by the "
        "student's solution, not pre-supplied."
    )


@pytest.mark.parametrize("path", list(RAW_FILES.keys()))
def test_raw_gz_files_present_and_non_empty(path: Path):
    assert path.is_file(), f"Expected compressed log file {path} is missing."
    assert path.stat().st_size > 0, f"Compressed log file {path} is empty."


@pytest.mark.parametrize("path, expected_lines", RAW_FILES.items())
def test_raw_gz_files_contents_exact(path: Path, expected_lines):
    """Decompress each file and compare its exact contents line-by-line."""
    actual_lines = read_gzip_lines(path)
    assert actual_lines == expected_lines, (
        f"Contents of {path} do not match the canonical data set. "
        "If you modified the raw logs, please restore them."
    )


def test_sanity_total_500_on_target_date():
    """Verify that the total number of 500-status lines on 01-Oct-2023 is 8."""
    total_500 = 0
    for path in RAW_FILES:
        for line in read_gzip_lines(path):
            # Quick substring checks are sufficient for the guard test.
            if "[01/Oct/2023:" in line and '" 500 ' in line:
                total_500 += 1

    assert total_500 == EXPECTED_TOTAL_500_01OCT2023, (
        "Sanity check failed: expected "
        f"{EXPECTED_TOTAL_500_01OCT2023} matching lines but found {total_500}. "
        "Raw logs may have been altered."
    )


def test_reports_absent():
    """Neither report file should exist prior to the student's processing."""
    log_report = REPORTS_DIR / "500_errors_summary.log"
    csv_report = REPORTS_DIR / "500_errors_summary.csv"

    assert not log_report.exists(), (
        f"Report file {log_report} already exists before processing."
    )
    assert not csv_report.exists(), (
        f"Report file {csv_report} already exists before processing."
    )