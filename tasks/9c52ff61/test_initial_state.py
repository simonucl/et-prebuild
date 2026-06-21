# test_initial_state.py
#
# Pytest suite that validates the pristine OS / filesystem state
# BEFORE the student’s solution code runs.
#
# It checks that
#   • the expected input directory and files exist exactly where they should,
#   • the yet-to-be-created “summary” directory is *absent*,
#   • the contents of the three raw data files match the specification so
#     that downstream unit-tests can rely on them with confidence.
#
# Only stdlib + pytest are used.

import csv
from pathlib import Path

import pytest


HOME = Path("/home/user")
BASE_DIR = HOME / "server_logs"
SUMMARY_DIR = BASE_DIR / "summary"

ACCESS_LOG = BASE_DIR / "access.log"
ERROR_LOG = BASE_DIR / "error.log"
USAGE_CSV = BASE_DIR / "usage.csv"


@pytest.fixture(scope="module")
def access_lines():
    with ACCESS_LOG.open(encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


@pytest.fixture(scope="module")
def error_lines():
    with ERROR_LOG.open(encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


@pytest.fixture(scope="module")
def usage_rows():
    with USAGE_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


# --------------------------------------------------------------------------- #
# Directory / file presence
# --------------------------------------------------------------------------- #
def test_input_directory_and_files_exist():
    assert BASE_DIR.is_dir(), f"Expected directory {BASE_DIR} is missing."
    for fp in (ACCESS_LOG, ERROR_LOG, USAGE_CSV):
        assert fp.is_file(), f"Required input file {fp} is missing."


def test_summary_directory_absent_initially():
    assert not SUMMARY_DIR.exists(), (
        f"Directory {SUMMARY_DIR} should NOT exist before the student's script "
        "is executed."
    )


# --------------------------------------------------------------------------- #
# access.log expectations
# --------------------------------------------------------------------------- #
EXPECTED_IP_HITS = {
    "192.168.1.10": 4,
    "192.168.1.15": 4,
    "192.168.1.20": 2,
    "192.168.1.25": 2,
}


def test_access_log_line_count(access_lines):
    assert len(access_lines) == 12, (
        "access.log must contain exactly 12 lines as per the specification."
    )


def test_access_log_ip_statistics(access_lines):
    hits = {}
    for line in access_lines:
        ip = line.split()[0]
        hits[ip] = hits.get(ip, 0) + 1

    assert hits == EXPECTED_IP_HITS, (
        "IP-address hit counts in access.log do not match the expected values:\n"
        f"  expected: {EXPECTED_IP_HITS}\n"
        f"  found   : {hits}"
    )


# --------------------------------------------------------------------------- #
# error.log expectations
# --------------------------------------------------------------------------- #
EXPECTED_ERROR_TALLY = {
    "2023-10-12": 2,
    "2023-10-13": 2,
    "2023-10-14": 2,
}


def test_error_log_line_count(error_lines):
    assert len(error_lines) == 10, (
        "error.log must contain exactly 10 lines as per the specification."
    )


def test_error_log_daily_error_totals(error_lines):
    tally = {}
    for line in error_lines:
        date_part = line[:10]  # YYYY-MM-DD
        level = line.split()[2]
        if level == "ERROR":
            tally[date_part] = tally.get(date_part, 0) + 1

    assert tally == EXPECTED_ERROR_TALLY, (
        "Daily ERROR counts in error.log do not match the expected values:\n"
        f"  expected: {EXPECTED_ERROR_TALLY}\n"
        f"  found   : {tally}"
    )


# --------------------------------------------------------------------------- #
# usage.csv expectations
# --------------------------------------------------------------------------- #
EXPECTED_CPU_AVG = {
    "srv1": 37.50,
    "srv2": 51.25,
    "srv3": 22.50,
}


def test_usage_csv_header():
    with USAGE_CSV.open(encoding="utf-8") as fh:
        first_line = fh.readline().rstrip("\n")
    assert first_line == "server,date,cpu_percent,mem_percent", (
        "usage.csv header row is incorrect. "
        "Expected exactly: server,date,cpu_percent,mem_percent"
    )


def test_usage_csv_average_cpu(usage_rows):
    sums = {}
    counts = {}
    for row in usage_rows:
        srv = row["server"]
        cpu = float(row["cpu_percent"])
        sums[srv] = sums.get(srv, 0.0) + cpu
        counts[srv] = counts.get(srv, 0) + 1

    avgs = {srv: round(sums[srv] / counts[srv], 2) for srv in sums}

    assert avgs == EXPECTED_CPU_AVG, (
        "Average CPU utilisation per server in usage.csv "
        "does not match the expected values:\n"
        f"  expected: {EXPECTED_CPU_AVG}\n"
        f"  found   : {avgs}"
    )


# --------------------------------------------------------------------------- #
# Sanity cross-checks
# --------------------------------------------------------------------------- #
def test_no_duplicate_servers_in_usage_csv(usage_rows):
    """Ensure each (server, date) tuple appears only once."""
    seen = set()
    for row in usage_rows:
        key = (row["server"], row["date"])
        assert key not in seen, (
            f"Duplicate entry for server-date combination {key} in usage.csv"
        )
        seen.add(key)