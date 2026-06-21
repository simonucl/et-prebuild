# test_initial_state.py
#
# This test-suite verifies that the sandbox is in its pristine
# “starting” condition *before* the student begins the exercise.
#
# Expectations:
#   • Exactly one file exists:  /home/user/logs/access.log
#   • That file contains the 15 Apache-style log lines listed in the
#     task description (including trailing newlines).
#   • No output/working artefacts exist yet:
#         /home/user/analysis/
#         /home/user/analysis/ip_count.txt
#         /home/user/analysis/status_count.txt
#         /home/user/analysis/combined_report.txt
#
# If any of these conditions are violated, the tests will fail and the
# error message will make it clear what is wrong.

import os
from pathlib import Path
from collections import Counter

import pytest

# ---------------------------------------------------------------------------
# Static expectations
# ---------------------------------------------------------------------------

ACCESS_LOG_PATH = Path("/home/user/logs/access.log")
ANALYSIS_DIR = Path("/home/user/analysis")

EXPECTED_LOG_LINES = [
    '10.0.0.1 - - [01/Jan/2023:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '10.0.0.2 - - [01/Jan/2023:10:00:02 +0000] "POST /login HTTP/1.1" 302 512\n',
    '10.0.0.1 - - [01/Jan/2023:10:00:03 +0000] "GET /about HTTP/1.1" 200 2048\n',
    '10.0.0.3 - - [01/Jan/2023:10:00:04 +0000] "GET /index.html HTTP/1.1" 404 256\n',
    '10.0.0.2 - - [01/Jan/2023:10:00:05 +0000] "GET /dashboard HTTP/1.1" 200 3072\n',
    '10.0.0.4 - - [01/Jan/2023:10:00:06 +0000] "GET /index.html HTTP/1.1" 500 128\n',
    '10.0.0.1 - - [01/Jan/2023:10:00:07 +0000] "GET /contact HTTP/1.1" 200 1024\n',
    '10.0.0.2 - - [01/Jan/2023:10:00:08 +0000] "GET /profile HTTP/1.1" 404 256\n',
    '10.0.0.3 - - [01/Jan/2023:10:00:09 +0000] "POST /upload HTTP/1.1" 201 512\n',
    '10.0.0.1 - - [01/Jan/2023:10:00:10 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '10.0.0.4 - - [01/Jan/2023:10:00:11 +0000] "GET /error HTTP/1.1" 500 128\n',
    '10.0.0.2 - - [01/Jan/2023:10:00:12 +0000] "GET /dashboard HTTP/1.1" 200 3072\n',
    '10.0.0.2 - - [01/Jan/2023:10:00:13 +0000] "GET /logout HTTP/1.1" 200 1024\n',
    '10.0.0.3 - - [01/Jan/2023:10:00:14 +0000] "GET /index.html HTTP/1.1" 200 1024\n',
    '10.0.0.1 - - [01/Jan/2023:10:00:15 +0000] "GET /cart HTTP/1.1" 500 256\n',
]

# Derived expectations: frequency tables that *should* result from the
# above lines.  We calculate them dynamically to avoid typos.
def _expected_counts():
    ip_counter = Counter()
    status_counter = Counter()
    for line in EXPECTED_LOG_LINES:
        tokens = line.split()
        ip = tokens[0]
        status = tokens[-2]
        ip_counter[ip] += 1
        status_counter[status] += 1
    return ip_counter, status_counter


EXPECTED_IP_COUNTS, EXPECTED_STATUS_COUNTS = _expected_counts()

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_access_log_exists_and_is_file():
    assert ACCESS_LOG_PATH.exists(), f"Expected {ACCESS_LOG_PATH} to exist, but it is missing."
    assert ACCESS_LOG_PATH.is_file(), f"Expected {ACCESS_LOG_PATH} to be a file."


def test_access_log_contents_match_exactly():
    with ACCESS_LOG_PATH.open("r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    # Exact line-for-line equivalence (including \n)
    assert actual_lines == EXPECTED_LOG_LINES, (
        "The contents of /home/user/logs/access.log do not match the expected "
        "15 reference lines.  Please ensure the sandbox starts with the "
        "correct fixture file."
    )


def test_access_log_yields_expected_ip_and_status_counts():
    # Re-compute counts from the *actual* file in case the previous test is
    # skipped or xfailed.
    with ACCESS_LOG_PATH.open("r", encoding="utf-8") as fh:
        ip_counter = Counter()
        status_counter = Counter()
        for line in fh:
            tokens = line.split()
            ip_counter[tokens[0]] += 1
            status_counter[tokens[-2]] += 1

    assert ip_counter == EXPECTED_IP_COUNTS, (
        "IP address frequencies in access.log are not as expected.\n"
        f"Expected: {dict(EXPECTED_IP_COUNTS)}\n"
        f"Found   : {dict(ip_counter)}"
    )

    assert status_counter == EXPECTED_STATUS_COUNTS, (
        "HTTP status code frequencies in access.log are not as expected.\n"
        f"Expected: {dict(EXPECTED_STATUS_COUNTS)}\n"
        f"Found   : {dict(status_counter)}"
    )


@pytest.mark.parametrize(
    "path",
    [
        ANALYSIS_DIR,
        ANALYSIS_DIR / "ip_count.txt",
        ANALYSIS_DIR / "status_count.txt",
        ANALYSIS_DIR / "combined_report.txt",
    ],
)
def test_no_analysis_artifacts_exist_yet(path: Path):
    assert not path.exists(), (
        f"Pre-condition failed: {path} should NOT exist before the student "
        "runs their solution, but it is already present."
    )