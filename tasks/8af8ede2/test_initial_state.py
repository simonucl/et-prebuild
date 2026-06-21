# test_initial_state.py
#
# This test-suite validates that the operating-system state **before** the
# student’s work begins is exactly what the exercise expects.  It checks only
# the *input* artefacts (the logs directory and its access.log file) and does
# NOT look for any of the files the student is asked to create.

import re
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
ACCESS_LOG = LOG_DIR / "access.log"

# The canonical contents of /home/user/logs/access.log
EXPECTED_ACCESS_LOG = (
    "127.0.0.1 - - [15/Sep/2023:10:15:30 +0000] \"GET /api/login HTTP/1.1\" 200 1234 \"-\" \"Mozilla/5.0\"\n"
    "192.168.1.10 - - [15/Sep/2023:11:02:15 +0000] \"POST /api/purchase HTTP/1.1\" 503 542 \"-\" \"curl/7.68.0\"\n"
    "10.0.0.3 - - [15/Sep/2023:11:45:50 +0000] \"GET /dashboard HTTP/1.1\" 500 654 \"-\" \"Mozilla/5.0\"\n"
    "127.0.0.1 - - [14/Sep/2023:09:01:12 +0000] \"GET /index.html HTTP/1.1\" 404 102 \"-\" \"Mozilla/5.0\"\n"
    "192.168.1.11 - - [15/Sep/2023:12:00:00 +0000] \"POST /api/upload HTTP/1.1\" 201 1024 \"-\" \"curl/7.68.0\"\n"
    "10.0.0.4 - - [15/Sep/2023:12:30:25 +0000] \"GET /status HTTP/1.1\" 502 210 \"-\" \"Mozilla/5.0\"\n"
    "127.0.0.1 - - [15/Sep/2023:12:32:01 +0000] \"GET /api/data HTTP/1.1\" 200 321 \"-\" \"Mozilla/5.0\"\n"
    "192.168.1.12 - - [16/Sep/2023:00:10:05 +0000] \"GET /maintenance HTTP/1.1\" 503 333 \"-\" \"curl/7.68.0\"\n"
    "10.0.0.5 - - [15/Sep/2023:13:15:45 +0000] \"POST /api/logout HTTP/1.1\" 500 400 \"-\" \"Mozilla/5.0\"\n"
    "127.0.0.1 - - [15/Sep/2023:14:55:10 +0000] \"GET /nonexistent HTTP/1.1\" 404 98 \"-\" \"Mozilla/5.0\"\n"
)

def test_logs_directory_exists():
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. The exercise expects this "
        "directory to contain the production access log."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_access_log_exists():
    assert ACCESS_LOG.exists(), (
        f"Required file {ACCESS_LOG} is missing. It must be present so that the "
        "student can filter it."
    )
    assert ACCESS_LOG.is_file(), f"{ACCESS_LOG} exists but is not a regular file."


def test_access_log_content_matches_fixture():
    actual = ACCESS_LOG.read_text(encoding="utf-8")
    assert actual == EXPECTED_ACCESS_LOG, (
        f"{ACCESS_LOG} does not contain the expected data.\n"
        "If this file is modified the downstream grading will be incorrect. "
        "Ensure the initial log lines match the fixture exactly, including "
        "whitespace and the trailing newline."
    )


def test_expected_number_of_5xx_lines_present():
    """
    Sanity-check: the log must contain the four specific 5xx entries that the
    exercise asks the student to extract.  We intentionally do NOT check for
    any output files—only that the input offers enough data for the task.
    """
    pattern = re.compile(
        r"""
        ^.*                                # entire line
        \[15/Sep/2023:[^\]]+\]             # the exact date 15/Sep/2023
        \s+"(?:GET|POST)\s+[^"]+"\s+       # request method & URI inside quotes
        5\d{2}\s+                          # 5xx status code
        """,
        re.VERBOSE | re.MULTILINE,
    )
    matches = pattern.findall(ACCESS_LOG.read_text(encoding="utf-8"))
    assert len(matches) == 4, (
        "The access log should contain exactly 4 lines from 15 Sep 2023 with "
        "HTTP 5xx status codes (as described in the task). "
        f"Found {len(matches)} matching lines instead."
    )