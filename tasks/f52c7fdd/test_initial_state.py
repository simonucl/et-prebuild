# test_initial_state.py
"""
Pytest suite that validates the environment **before** the student begins work.

This test file asserts that the required source data file is present and
unchanged.  It deliberately avoids checking for any output artefacts
(/home/user/report, etc.) because those should not exist yet.
"""

import os
import pytest

RAW_CSV_PATH = "/home/user/data/raw_contacts.csv"

EXPECTED_CSV_CONTENT = (
    "id,name,email,department\n"
    "1,Alice Anderson,alice.anderson@example.com,Finance\n"
    "2,Bob Brown,bob.brown@example.com,Engineering\n"
    "3,Charlie Clark,charlie.clark@example.com,Marketing\n"
)


def test_raw_contacts_csv_exists():
    """
    Ensure that the seed CSV file is present at the expected absolute path.
    """
    assert os.path.isfile(
        RAW_CSV_PATH
    ), f"Required source file not found at '{RAW_CSV_PATH}'. Make sure it exists."


def test_raw_contacts_csv_content_is_exact():
    """
    Verify that the CSV file content matches the specification byte-for-byte.
    """
    # The existence check is repeated for clearer failure context
    assert os.path.isfile(
        RAW_CSV_PATH
    ), f"Required source file not found at '{RAW_CSV_PATH}'."

    with open(RAW_CSV_PATH, "r", encoding="utf-8", newline="") as fh:
        actual_content = fh.read()

    assert (
        actual_content == EXPECTED_CSV_CONTENT
    ), (
        "The content of '/home/user/data/raw_contacts.csv' does not match the "
        "expected initial data. If you have modified this file, please restore "
        "it exactly as documented in the task description."
    )


def test_raw_contacts_csv_column_count():
    """
    Confirm that every non-header line has exactly four comma-separated columns.
    """
    with open(RAW_CSV_PATH, "r", encoding="utf-8", newline="") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    # Skip header
    for i, line in enumerate(lines[1:], start=2):
        columns = line.split(",")
        assert len(columns) == 4, (
            f"Line {i} of '{RAW_CSV_PATH}' has {len(columns)} column(s) "
            f"instead of 4: {line!r}"
        )