# test_initial_state.py
"""
Pytest suite that validates the initial operating-system / filesystem state
before the learner begins the exercise.

❗  These tests CONFIRM ONLY THE PRE-EXISTING INPUTS.
   Per the instructions we deliberately do NOT test for the deliverable
   outputs (cleaned CSV, log file, or the /home/user/datasets/clean
   directory).  Those will be checked by a separate rubric once the learner
   has completed their work.
"""

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

RAW_DIR = Path("/home/user/datasets/raw")
RAW_CSV = RAW_DIR / "sales_2023.csv"

EXPECTED_LINES = [
    "OrderID,Date,Product,Quantity,UnitPrice,CustomerEmail",
    "1001,01/03/2023,Widget A,4,25.50,alice@example.com",
    "1002,02/15/2023,Widget B,,30.00,bob@example.com",
    '1003,03/22/2023,Widget C,2,,"charlie@example.com"',
    "1004,04/10/2023,Widget A,1,25.50,dana@example.com",
    "1005,05/18/2023,Widget D,3,40.00,erin@example.com",
    "1006,06/30/2023,Widget B,5,30.00,frank@example.com",
    "1007,07/12/2023,Widget A,2,25.50,grace@example.com",
    "1008,08/25/2023,Widget E,7,55.00,harry@example.com",
]

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #


def test_raw_directory_exists():
    """
    The directory /home/user/datasets/raw must exist and be a directory.
    """
    assert RAW_DIR.exists(), f"Required directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


def test_raw_csv_exists():
    """
    The raw CSV file must exist at the exact absolute path.
    """
    assert RAW_CSV.exists(), f"Required file {RAW_CSV} is missing."
    assert RAW_CSV.is_file(), f"{RAW_CSV} exists but is not a regular file."


def test_raw_csv_contents_exact_match():
    """
    The raw CSV file must match the expected 9-line content exactly
    (header plus 8 data rows), ignoring trailing newlines.
    """
    with RAW_CSV.open("r", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()

    # Helpful diagnostics on mismatch
    assert (
        len(actual_lines) == len(EXPECTED_LINES)
    ), f"{RAW_CSV} should contain {len(EXPECTED_LINES)} lines, found {len(actual_lines)}."

    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, actual_lines), start=1):
        assert (
            expected == actual
        ), (
            f"Line {idx} of {RAW_CSV} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}"
        )