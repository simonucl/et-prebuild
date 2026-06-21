# test_initial_state.py
#
# This pytest suite validates the initial filesystem state **before**
# the student starts working on the task.  It purposefully ignores every
# file or directory that the student is expected to create later
# (e.g. /home/user/security_scan/, /home/user/data_sanitized/).
#
# The checks focus on:
#   • the existence of /home/user/data/
#   • the presence of exactly two CSV files inside that directory
#   • the exact, canonical contents of both CSV files
#
# Any failure message should make it immediately clear what is missing
# or incorrect.

import os
from pathlib import Path
import pytest

DATA_DIR = Path("/home/user/data")
CSV_FILES = {
    "sales_q1.csv": [
        "order_id,customer_email,amount",
        "1001,alice@example.com,250.00",
        "1002,bob@gmail.com,175.50",
        "1003,charlie@example.com,300.00",
    ],
    "customer_info.csv": [
        "customer_id,name,email,credit_card",
        "c001,Alice Smith,alice@example.com,4111-1111-1111-1111",
        "c002,Bob Johnson,bob@gmail.com,5500-0000-0000-0004",
        "c003,Charlie Brown,charlie@example.com,6011-0009-9013-9424",
    ],
}


def test_data_directory_exists():
    """/home/user/data/ must exist and be a directory."""
    assert DATA_DIR.exists(), f"Expected directory {DATA_DIR} to exist."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def test_exact_two_csv_files_present():
    """
    Exactly the two expected CSV files must be present *directly* under
    /home/user/data/ and there should be no additional .csv files.
    """
    csv_paths = list(DATA_DIR.glob("*.csv"))
    found_basenames = sorted(p.name for p in csv_paths)

    expected_basenames = sorted(CSV_FILES.keys())
    assert (
        found_basenames == expected_basenames
    ), f"Expected CSV files {expected_basenames}, but found {found_basenames}."


@pytest.mark.parametrize("filename,expected_lines", CSV_FILES.items())
def test_csv_contents_are_exact(filename, expected_lines):
    """
    The contents of each CSV must match the canonical version line-for-line.
    Trailing newlines are ignored for comparison convenience.
    """
    path = DATA_DIR / filename
    assert path.exists(), f"Missing expected file {path}"

    with path.open("r", encoding="utf-8") as fh:
        # Strip only the trailing newline so that CRLF vs LF does not matter.
        actual_lines = [line.rstrip("\r\n") for line in fh.readlines()]

    assert (
        actual_lines == expected_lines
    ), f"File {path} contents do not match expected.\nExpected:\n{expected_lines}\nGot:\n{actual_lines}"