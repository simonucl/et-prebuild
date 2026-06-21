# test_initial_state.py
#
# This pytest suite validates the initial state of the filesystem **before**
# the student runs any solution code.  It checks that the required log
# directory and the two raw Nginx access-log files exist, and that the
# 2023-08-15 log contains exactly the 12 expected lines in the correct order.
#
# NOTE:  Per the task rules, we intentionally do *not* look for any of the
#        output files that the student is expected to create later.
#
# Only Python’s stdlib and pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
LOG_DIR = PROJECT_DIR / "logs"

EXPECTED_15AUG_LINES = [
    '192.168.1.10 - - [15/Aug/2023:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 5320 "-" "Mozilla/5.0"',
    '192.168.1.11 - - [15/Aug/2023:10:16:02 +0000] "POST /api/v1/login HTTP/1.1" 401 298 "-" "curl/7.68.0"',
    '192.168.1.12 - - [15/Aug/2023:10:17:45 +0000] "GET /dashboard HTTP/1.1" 500 1032 "-" "Mozilla/5.0"',
    '192.168.1.13 - - [15/Aug/2023:10:18:01 +0000] "GET /favicon.ico HTTP/1.1" 200 543 "-" "Mozilla/5.0"',
    '192.168.1.14 - - [15/Aug/2023:10:19:27 +0000] "GET /api/v1/data HTTP/1.1" 200 2780 "-" "Mozilla/5.0"',
    '192.168.1.15 - - [15/Aug/2023:10:20:14 +0000] "POST /api/v1/update HTTP/1.1" 503 64 "-" "Python-urllib/3.8"',
    '192.168.1.16 - - [15/Aug/2023:10:21:05 +0000] "GET /hidden HTTP/1.1" 403 232 "-" "curl/7.68.0"',
    '192.168.1.17 - - [15/Aug/2023:10:22:47 +0000] "DELETE /api/v1/data HTTP/1.1" 200 34 "-" "Mozilla/5.0"',
    '192.168.1.18 - - [15/Aug/2023:10:23:55 +0000] "GET /status HTTP/1.1" 200 123 "-" "Mozilla/5.0"',
    '192.168.1.19 - - [15/Aug/2023:10:24:30 +0000] "GET /report HTTP/1.1" 512 67 "-" "Mozilla/5.0"',
    '192.168.1.20 - - [15/Aug/2023:10:25:11 +0000] "GET /index.html HTTP/1.1" 304 0 "-" "Mozilla/5.0"',
    '192.168.1.21 - - [15/Aug/2023:10:26:07 +0000] "GET /unknown HTTP/1.1" 404 88 "-" "Mozilla/5.0"',
]

@pytest.fixture(scope="module")
def aug15_lines():
    """Read and cache the 2023-08-15 access-log lines (stripped of newlines)."""
    file_path = LOG_DIR / "2023-08-15_access.log"
    with file_path.open("r", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]

def test_log_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Required directory missing: {LOG_DIR}. "
        "The directory containing the raw access logs must be present."
    )

@pytest.mark.parametrize(
    "filename",
    ["2023-08-14_access.log", "2023-08-15_access.log"],
)
def test_required_log_files_exist(filename):
    file_path = LOG_DIR / filename
    assert file_path.is_file(), (
        f"Expected log file {file_path} is missing. "
        "Ensure the legacy access-log files are in place."
    )

def test_aug15_line_count(aug15_lines):
    expected_count = len(EXPECTED_15AUG_LINES)
    actual_count = len(aug15_lines)
    assert actual_count == expected_count, (
        f"/home/user/project/logs/2023-08-15_access.log should contain "
        f"{expected_count} lines, but {actual_count} were found."
    )

def test_aug15_exact_contents(aug15_lines):
    for idx, (expected, actual) in enumerate(zip(EXPECTED_15AUG_LINES, aug15_lines), start=1):
        assert actual == expected, (
            "Content mismatch in 2023-08-15_access.log on line "
            f"{idx}.\nExpected: {expected!r}\nFound:    {actual!r}"
        )

def test_aug15_no_extra_lines(aug15_lines):
    # This separate check gives a clearer message if extra lines are present.
    assert aug15_lines == EXPECTED_15AUG_LINES, (
        "The 2023-08-15_access.log file has unexpected extra lines or ordering "
        "issues.  It must match the reference log exactly."
    )