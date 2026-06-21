# test_initial_state.py
#
# Pytest suite that validates the expected *initial* filesystem state for
# the “Compliance Officer” exercise _before_ the student has performed any
# actions.  It intentionally checks only for the presence and exact contents
# of the staged source data under /home/user/audit_data/ and—per project
# rules—does **not** make any assertions about the yet-to-be-created
# /home/user/audit_output/ directory or its files.

import os
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

AUDIT_DATA_DIR = Path("/home/user/audit_data")
HOSTS_CSV = AUDIT_DATA_DIR / "hosts.csv"
VULNS_CSV = AUDIT_DATA_DIR / "vulnerabilities.csv"

EXPECTED_HOSTS_CSV = (
    "host_id,hostname,ip,owner\n"
    "1,db-prod-01,10.0.0.11,finance\n"
    "2,web-prod-02,10.0.0.21,marketing\n"
    "3,db-test-01,10.0.1.11,finance\n"
    "4,ci-server,10.0.2.5,devops\n"
)

EXPECTED_VULNS_CSV = (
    "host_id,cve_id,severity,fix_available\n"
    "1,CVE-2022-0001,Critical,Yes\n"
    "1,CVE-2022-0002,High,Yes\n"
    "2,CVE-2021-1111,Critical,No\n"
    "3,CVE-2020-2222,Medium,Yes\n"
    "4,CVE-2019-3333,Low,No\n"
)

# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #

def _read_file_normalized(path: Path) -> str:
    """
    Read *path* and normalise all line endings to LF so comparisons are
    platform-independent.  The exercise itself is Linux-based, but this
    makes the test more robust.
    """
    with path.open("r", encoding="utf-8", newline="") as fh:
        data = fh.read()
    return data.replace("\r\n", "\n")


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_audit_data_directory_exists():
    assert AUDIT_DATA_DIR.is_dir(), (
        f"Required directory not found: {AUDIT_DATA_DIR}"
    )


def test_hosts_csv_present_and_exact():
    assert HOSTS_CSV.is_file(), f"Missing file: {HOSTS_CSV}"
    actual = _read_file_normalized(HOSTS_CSV)
    assert actual == EXPECTED_HOSTS_CSV, (
        "Contents of hosts.csv do not match the expected fixture.\n"
        "Expected:\n"
        f"{EXPECTED_HOSTS_CSV!r}\n\n"
        "Actual:\n"
        f"{actual!r}"
    )


def test_vulnerabilities_csv_present_and_exact():
    assert VULNS_CSV.is_file(), f"Missing file: {VULNS_CSV}"
    actual = _read_file_normalized(VULNS_CSV)
    assert actual == EXPECTED_VULNS_CSV, (
        "Contents of vulnerabilities.csv do not match the expected fixture.\n"
        "Expected:\n"
        f"{EXPECTED_VULNS_CSV!r}\n\n"
        "Actual:\n"
        f"{actual!r}"
    )