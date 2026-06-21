# test_initial_state.py
#
# This pytest suite confirms that the environment is in the expected
# “before-the-student-starts” state.
#
# It checks that:
#   • The source CSV exists at the exact path and has the exact expected content
#     (both lines and Unix LF line endings).
#   • The finops output directory and its three artefacts are **absent**.
#   • The byte-totals per destination IP inside the CSV match the truth table
#     provided in the exercise text.
#
# Only standard-library modules and pytest are used.

import csv
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants used by all tests
# ---------------------------------------------------------------------------

CSV_PATH = Path("/home/user/logs/egress_traffic.csv")
FIREWALL_DIR = Path("/home/user/finops_firewall")
REPORT_FILE = FIREWALL_DIR / "egress_report.txt"
RULES_FILE = FIREWALL_DIR / "egress_block.rules"
SAVE_FILE = FIREWALL_DIR / "iptables-save.out"

EXPECTED_CSV_LINES = [
    "timestamp,src_ip,dst_ip,bytes_out",
    "2024-05-01T10:00:00Z,10.0.0.5,34.102.120.1,2048",
    "2024-05-01T10:01:00Z,10.0.0.5,44.12.31.5,10240",
    "2024-05-01T10:02:00Z,10.0.0.20,34.102.120.1,4096",
    "2024-05-01T10:03:00Z,10.0.0.20,172.217.3.110,5120",
    "2024-05-01T10:04:00Z,10.0.0.7,44.12.31.5,8192",
    "2024-05-01T10:05:00Z,10.0.0.7,34.102.120.1,1024",
    "2024-05-01T10:06:00Z,10.0.0.7,172.217.3.110,10000",
    "2024-05-01T10:07:00Z,10.0.0.5,34.102.120.1,3072",
    "2024-05-01T10:08:00Z,10.0.0.20,44.12.31.5,2048",
    "2024-05-01T10:09:00Z,10.0.0.5,34.102.120.1,5120",
]

EXPECTED_TOTALS = {
    "44.12.31.5":    20480,
    "34.102.120.1":  15360,
    "172.217.3.110": 15120,
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def read_csv_lines(path: Path):
    """
    Return the CSV file’s lines as a list of *str* without trailing newlines.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


def has_only_lf_endings(path: Path) -> bool:
    """
    Verify that the file uses Unix LF (`\n`) line endings exclusively.
    """
    raw = path.read_bytes()
    return b"\r" not in raw  # Presence of CR implies CRLF or classic Mac.


def compute_byte_totals(path: Path):
    """
    Parse the CSV and return a dict {dst_ip: total_bytes_out}.
    """
    totals = {}
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            dst = row["dst_ip"].strip()
            bytes_out = int(row["bytes_out"])
            totals[dst] = totals.get(dst, 0) + bytes_out
    return totals


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_csv_exists_and_has_expected_contents():
    assert CSV_PATH.exists(), (
        f"Required CSV not found at {CSV_PATH}. "
        "Make sure the log file is pre-provisioned."
    )
    lines = read_csv_lines(CSV_PATH)
    assert (
        lines == EXPECTED_CSV_LINES
    ), "The contents of the CSV do not match the expected 11 lines."
    assert has_only_lf_endings(CSV_PATH), (
        "CSV file should use Unix LF line endings (no CR characters found)."
    )


def test_csv_totals_are_correct():
    totals = compute_byte_totals(CSV_PATH)
    # We compare only the three destination hosts we care about.
    for ip, expected_total in EXPECTED_TOTALS.items():
        assert (
            ip in totals
        ), f"Destination IP {ip} is missing from the CSV (expected to be present)."
        assert (
            totals[ip] == expected_total
        ), f"Byte total for {ip} is {totals[ip]}, expected {expected_total}."


@pytest.mark.parametrize(
    "path_",
    [
        FIREWALL_DIR,
        REPORT_FILE,
        RULES_FILE,
        SAVE_FILE,
    ],
)
def test_firewall_outputs_do_not_yet_exist(path_: Path):
    assert not path_.exists(), (
        f"{path_} already exists, but it should **not** be present before the "
        "student runs their solution."
    )