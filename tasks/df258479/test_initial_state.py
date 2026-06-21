# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before**
# the student runs their processing script.  It checks only the raw input
# that must already be present under /home/user/scan_data/ and deliberately
# avoids looking for – or mentioning – any output artefacts or directories.

import csv
import os
from pathlib import Path

import pytest

SCAN_DATA_DIR = Path("/home/user/scan_data")

# --------------------------------------------------------------------------- #
# 1.  Directory-level sanity
# --------------------------------------------------------------------------- #


def test_scan_data_directory_exists_and_is_dir():
    """
    /home/user/scan_data must exist and be a directory that the agent can read.
    """
    assert SCAN_DATA_DIR.exists(), (
        f"Required directory {SCAN_DATA_DIR} does not exist."
    )
    assert SCAN_DATA_DIR.is_dir(), (
        f"{SCAN_DATA_DIR} exists but is not a directory."
    )
    # Basic read permission check: try to list the directory
    try:
        list(SCAN_DATA_DIR.iterdir())
    except PermissionError as exc:  # pragma: no cover
        pytest.fail(f"Read permission is missing on {SCAN_DATA_DIR}: {exc}")


# --------------------------------------------------------------------------- #
# 2.  File presence tests (parametrised)
# --------------------------------------------------------------------------- #

INPUT_FILES = [
    SCAN_DATA_DIR / "segment_a.csv",
    SCAN_DATA_DIR / "segment_b.csv",
    SCAN_DATA_DIR / "segment_c.csv",
]


@pytest.mark.parametrize("path", INPUT_FILES)
def test_input_file_exists(path: Path):
    """
    Every expected CSV must already exist as a *file* and be readable.
    """
    assert path.exists(), f"Expected input file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    try:
        path.read_bytes()
    except PermissionError as exc:  # pragma: no cover
        pytest.fail(f"Read permission is missing on {path}: {exc}")


# --------------------------------------------------------------------------- #
# 3.  Exact CSV-content verification
# --------------------------------------------------------------------------- #

# Ground-truth rows for each CSV (all columns are strings).
EXPECTED_ROWS = {
    INPUT_FILES[0]: [
        ["ip", "port", "service", "version", "vuln_status", "cvss_score", "cve"],
        ["192.168.10.2", "22", "ssh", "OpenSSH_7.2p2", "no", "0", ""],
        ["192.168.10.5", "80", "http", "Apache 2.4.18", "yes", "7.5", "CVE-2017-15710"],
        ["192.168.10.7", "443", "https", "nginx 1.10.3", "no", "0", ""],
        ["192.168.10.9", "3306", "mysql", "5.7.29", "yes", "9.8", "CVE-2020-14825"],
    ],
    INPUT_FILES[1]: [
        ["ip", "port", "service", "version", "vuln_status", "cvss_score", "cve"],
        ["192.168.20.4", "21", "ftp", "vsftpd 3.0.3", "no", "0", ""],
        ["192.168.20.8", "445", "smb", "Samba 4.3.11", "yes", "8.1", "CVE-2017-7494"],
        ["192.168.20.12", "25", "smtp", "Postfix 3.1.0", "no", "0", ""],
        ["192.168.20.15", "80", "http", "Apache 2.4.6", "yes", "6.5", "CVE-2014-0226"],
    ],
    INPUT_FILES[2]: [
        ["ip", "port", "service", "version", "vuln_status", "cvss_score", "cve"],
        ["10.0.0.3", "53", "dns", "BIND 9.10.3-P4", "yes", "7.8", "CVE-2016-2776"],
        ["10.0.0.5", "22", "ssh", "OpenSSH_7.4", "yes", "5.3", "CVE-2018-15473"],
        ["10.0.0.8", "3389", "rdp", "FreeRDP 2.0.0", "no", "0", ""],
        ["10.0.0.10", "8080", "http", "Tomcat 9.0.31", "yes", "9.8", "CVE-2020-1938"],
    ],
}


@pytest.mark.parametrize("path,expected", EXPECTED_ROWS.items())
def test_csv_contents_match_ground_truth(path: Path, expected):
    """
    Open each CSV and compare every row against the canonical ground-truth.
    Parsing with the csv module allows for uniform treatment of newline
    variations (LF vs CRLF) and surrounding whitespace.
    """
    with path.open(newline="") as fp:
        reader = csv.reader(fp)
        actual_rows = [row for row in reader]

    # Use assert equality for a clean diff if pytest --showlocals is used.
    assert (
        actual_rows == expected
    ), f"Contents of {path} do not match the expected initial data."