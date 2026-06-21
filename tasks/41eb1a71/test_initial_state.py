# test_initial_state.py
#
# A pytest test-suite that validates the operating-system / filesystem
# *before* the student performs any action for the “Network connectivity
# audit with sort + uniq frequency counting” task.
#
# It checks only the items that must already exist (or not) according to
# the specification.  Nothing related to the yet-to-be-created output
# directories or files is tested here, in compliance with the rules.

import gzip
import os
from pathlib import Path
from collections import Counter

LOG_DIR = Path("/home/user/network/logs")
GZ_FILE = LOG_DIR / "connection_attempts.csv.gz"


def test_log_directory_exists():
    """The /home/user/network/logs/ directory must already exist."""
    assert LOG_DIR.is_dir(), (
        f"Required directory missing: {LOG_DIR}.  "
        "It should have been provided in the starter filesystem."
    )


def test_gz_file_exists():
    """The compressed CSV file must already exist."""
    assert GZ_FILE.is_file(), (
        f"Required file missing: {GZ_FILE}.  "
        "Ensure the initial dataset is present at the correct path."
    )


def _read_gz_lines():
    """Helper: return the decoded lines inside the gzip file."""
    with gzip.open(GZ_FILE, "rt", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]
    return lines


def test_gz_file_has_expected_number_of_records():
    """The gzip file must contain exactly 10 CSV records."""
    lines = _read_gz_lines()
    assert len(lines) == 10, (
        f"{GZ_FILE} should contain 10 lines, found {len(lines)} instead."
    )


def test_each_record_has_six_comma_separated_fields():
    """Basic CSV integrity: every record must have six comma-separated columns."""
    lines = _read_gz_lines()
    bad_lines = [i for i, ln in enumerate(lines, 1) if ln.count(",") != 5]
    assert not bad_lines, (
        f"The following line numbers in {GZ_FILE} do not have 6 columns: "
        f"{', '.join(map(str, bad_lines))}"
    )


def test_status_frequency_is_as_documented():
    """
    The starter dataset should already have the documented distribution:
    ACCEPT 6, DROP 3, REJECT 1.
    """
    lines = _read_gz_lines()
    statuses = [ln.split(",")[5] for ln in lines]
    freq = Counter(statuses)
    expected = {"ACCEPT": 6, "DROP": 3, "REJECT": 1}
    assert freq == expected, (
        "Status frequency mismatch in the initial dataset.\n"
        f"Expected: {expected}\nFound:    {dict(freq)}"
    )


def test_failure_counts_per_ip_are_as_documented():
    """
    For IPs that ever suffered a failure (DROP or REJECT), the counts must be:
      8.8.4.4 -> 2
      8.8.8.8 -> 2
    """
    lines = _read_gz_lines()
    failures = [
        ln.split(",")[2]               # Destination IP is column 3 (index 2)
        for ln in lines
        if ln.split(",")[5] in {"DROP", "REJECT"}
    ]
    freq = Counter(failures)
    expected = {"8.8.4.4": 2, "8.8.8.8": 2}
    assert freq == expected, (
        "Failure count per IP in the initial dataset is not as documented.\n"
        f"Expected: {expected}\nFound:    {dict(freq)}"
    )