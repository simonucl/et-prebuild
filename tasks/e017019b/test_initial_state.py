# test_initial_state.py
"""
pytest suite that asserts the *initial* filesystem state for the Nessus-style
CSV exercise, **before** the student begins working on the solution.

The tests purposefully check only for artefacts that must already exist
(/home/user/scan_results/raw_scan.csv and its exact contents) and do **not**
look for any output files that the student is expected to create.
"""

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the required initial state
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/scan_results")
RAW_CSV = BASE_DIR / "raw_scan.csv"

EXPECTED_LINES = [
    "target_ip,hostname,port,service,cve_id,cvss_score,severity,description",
    "192.168.1.10,webserver1,80,http,CVE-2021-1234,7.5,HIGH,Some description",
    "192.168.1.11,db1,3306,mysql,CVE-2020-9999,5.3,MEDIUM,Some description",
    "192.168.1.12,ftp1,21,ftp,CVE-2019-2222,9.8,CRITICAL,Some description",
    "192.168.1.10,webserver1,443,https,CVE-2021-5678,4.3,LOW,Some description",
    "192.168.1.13,app1,8080,http,CVE-2022-1111,8.0,HIGH,Some description",
    "192.168.1.12,ftp1,21,ftp,CVE-2019-3333,6.1,MEDIUM,Some description",
    "192.168.1.14,mail,25,smtp,CVE-2021-0001,10.0,CRITICAL,Some description",
    "192.168.1.10,webserver1,80,http,CVE-2021-7777,9.0,CRITICAL,Some description",
    "192.168.1.13,app1,8080,http,CVE-2022-2222,9.5,CRITICAL,Some description",
    "192.168.1.11,db1,3306,mysql,CVE-2020-8888,7.0,HIGH,Some description",
]
EXPECTED_LINE_COUNT = len(EXPECTED_LINES)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_scan_results_directory_exists():
    """The /home/user/scan_results directory must already exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} is missing. "
        "It should be present before the student starts."
    )


def test_raw_scan_csv_exists():
    """The CSV file with the raw Nessus export must be present."""
    assert RAW_CSV.is_file(), (
        f"Required file {RAW_CSV} is missing. "
        "Provide the CSV so the student can work on it."
    )
    # Quick sanity check on size: it shouldn't be empty.
    assert RAW_CSV.stat().st_size > 0, f"{RAW_CSV} exists but is empty."


def test_raw_scan_csv_exact_contents():
    """
    The CSV file must have the exact, byte-for-byte contents specified in the
    task description.  This protects the student from starting with incorrect
    or corrupt data.
    """
    # Read in binary mode so we can check final newline accurately
    raw_bytes = RAW_CSV.read_bytes()
    assert raw_bytes.endswith(b"\n"), (
        f"{RAW_CSV} must end with a single LF newline character."
    )

    # Decode assuming UTF-8 and split into lines (strip the final LF first)
    csv_text = raw_bytes.decode("utf-8")
    lines = csv_text.rstrip("\n").split("\n")

    # 1. Line count
    assert len(lines) == EXPECTED_LINE_COUNT, (
        f"{RAW_CSV} should contain {EXPECTED_LINE_COUNT} lines "
        f"(1 header + 10 data rows) but has {len(lines)}."
    )

    # 2. Exact line-by-line content
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        assert actual == expected, (
            f"Mismatch on line {idx} of {RAW_CSV}.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )