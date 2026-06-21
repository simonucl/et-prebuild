# test_initial_state.py
#
# This test-suite verifies the **initial state of the filesystem** before the
# student begins work on the shell task.  Nothing here checks for the presence
# of the *output* files that the student is expected to create later.
#
# DO NOT MODIFY THIS FILE.
#
import os
import re
from collections import Counter

import pytest

HOME = "/home/user"
APP_DIR = os.path.join(HOME, "app")
LOGS_DIR = os.path.join(APP_DIR, "logs")
ACCESS_LOG = os.path.join(LOGS_DIR, "access.log")

# Paths that must **not** exist yet (they will be created by the student later)
REPORTS_DIR = os.path.join(APP_DIR, "reports")
STATUS_CODE_REPORT = os.path.join(REPORTS_DIR, "status_code_frequency.txt")
TOP_500_IPS_REPORT = os.path.join(REPORTS_DIR, "top_500_ips.txt")


@pytest.fixture(scope="session")
def access_log_lines():
    """Return all non-empty lines from the access.log file."""
    with open(ACCESS_LOG, "r", encoding="utf-8") as fh:
        # Keep the original order; strip only the trailing newline
        return [line.rstrip("\n") for line in fh.readlines() if line.strip()]


def test_logs_directory_exists():
    assert os.path.isdir(LOGS_DIR), (
        f"Expected directory {LOGS_DIR!r} to exist but it was not found."
    )


def test_access_log_exists():
    assert os.path.isfile(ACCESS_LOG), (
        f"Expected log file {ACCESS_LOG!r} to exist but it was not found."
    )


def test_reports_directory_does_not_exist_yet():
    assert not os.path.exists(REPORTS_DIR), (
        "The reports directory should NOT exist before the student runs the "
        "solution, but it was found at "
        f"{REPORTS_DIR!r}."
    )


@pytest.mark.parametrize(
    "path",
    [
        STATUS_CODE_REPORT,
        TOP_500_IPS_REPORT,
    ],
)
def test_report_files_do_not_exist_yet(path):
    assert not os.path.exists(path), (
        "Output file should not be present yet: "
        f"{path!r}"
    )


def parse_status_code(line):
    """
    Extract the HTTP status code from an Nginx/Apache-style access-log line.

    The log format in the starter file is known and always contains:
        ... "METHOD URL PROTOCOL" <STATUS_CODE> ...
    """
    parts = line.split('"')
    if len(parts) < 3:
        pytest.fail(f"Malformed log line (no quoted request part): {line!r}")
    trailer = parts[2].strip()  # e.g. 500 0 "-" "curl/7.64.1"
    status = trailer.split()[0]
    if not re.fullmatch(r"\d{3}", status):
        pytest.fail(f"Unable to parse status code from line: {line!r}")
    return status


def parse_client_ip(line):
    """
    Extract the client IP address from the start of the log line.

    The IP is the very first whitespace-separated token on the line.
    """
    ip = line.split(maxsplit=1)[0]
    if not ip or not re.fullmatch(r"[0-9.]+", ip):
        pytest.fail(f"Unable to parse client IP from line: {line!r}")
    return ip


def test_status_code_distribution(access_log_lines):
    """
    Ensure the access.log file has NOT been modified by checking the exact
    occurrence counts for each status code.
    """
    expected_counts = {
        "200": 15,
        "500": 8,
        "403": 5,
        "404": 5,
        "301": 4,
        "302": 3,
    }

    counts = Counter(parse_status_code(l) for l in access_log_lines)

    # First, validate that we saw *only* the expected status codes
    extra_codes = sorted(set(counts) - set(expected_counts))
    missing_codes = sorted(set(expected_counts) - set(counts))
    assert not extra_codes, (
        "Unexpected status codes found in the initial access.log: "
        f"{', '.join(extra_codes)}"
    )
    assert not missing_codes, (
        "Some expected status codes are missing from the initial access.log: "
        f"{', '.join(missing_codes)}"
    )

    # Now compare exact counts
    mismatches = {
        code: (expected_counts[code], counts[code])
        for code in expected_counts
        if expected_counts[code] != counts[code]
    }
    assert not mismatches, (
        "Status-code counts in access.log do not match the expected initial "
        "state:\n"
        + "\n".join(
            f"  {code}: expected {exp}, found {got}"
            for code, (exp, got) in sorted(mismatches.items())
        )
    )


def test_top_500_error_ips(access_log_lines):
    """
    Ensure the distribution of client IPs that generated HTTP 500 responses
    matches the expected initial state.
    """
    expected_top = [
        ("10.0.0.5", 3),
        ("192.168.1.10", 3),
        ("172.16.0.2", 2),
    ]

    # Gather counts for status 500 only
    counts = Counter(
        parse_client_ip(l) for l in access_log_lines
        if parse_status_code(l) == "500"
    )

    # Derive the top three according to the same sort rules that the student
    # will have to follow: count desc, IP lexicographical asc
    top_three_actual = sorted(
        counts.items(),
        key=lambda kv: (-kv[1], kv[0])
    )[:3]

    assert top_three_actual == expected_top, (
        "The set of client IPs responsible for 500 errors in the initial "
        "access.log is not as expected.\n"
        f"Expected: {expected_top}\n"
        f"Found   : {top_three_actual}"
    )