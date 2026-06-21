# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state **before**
# the student executes any command.  It checks that:
#
#   1.  /home/user/data exists and is a directory.
#   2.  The three required CSV files exist at the expected absolute paths.
#   3.  Each CSV starts with the exact header line 'id,value'.
#   4.  Each CSV contains the expected number of data rows.
#   5.  The combined total number of data rows is 9.
#   6.  The diagnostics file that the student is supposed to create
#       (/home/user/data/row_count_diagnostics.log) does *not* exist yet.
#
# All failures raise concise, actionable error messages so that any
# deviation from the required starting state is obvious.

import os
from pathlib import Path

import pytest

DATA_DIR = Path("/home/user/data").expanduser().resolve()

CSV_SPECS = [
    ("sales_q1.csv", 3),
    ("sales_q2.csv", 2),
    ("sales_q3.csv", 4),
]

DIAGNOSTICS_FILE = DATA_DIR / "row_count_diagnostics.log"


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Expected data directory {DATA_DIR} to exist and be a directory, "
        f"but it was not found."
    )


@pytest.mark.parametrize("filename,expected_rows", CSV_SPECS)
def test_csv_files_exist_and_have_expected_row_counts(filename, expected_rows):
    csv_path = DATA_DIR / filename
    assert csv_path.is_file(), (
        f"Required CSV file {csv_path} is missing."
    )

    # Read file contents
    with csv_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    assert lines, f"{csv_path} is empty; expected at least a header line."

    # Verify header
    header = lines[0].rstrip("\n\r")
    assert header == "id,value", (
        f"First line of {csv_path} should be the header 'id,value' "
        f"but found '{header}'."
    )

    # Count data rows (exclude header)
    data_row_count = len(lines) - 1
    assert data_row_count == expected_rows, (
        f"{csv_path} should contain {expected_rows} data rows "
        f"but contains {data_row_count}."
    )


def test_total_row_count_across_all_files():
    total_rows = 0
    for filename, expected_rows in CSV_SPECS:
        csv_path = DATA_DIR / filename
        assert csv_path.is_file(), (
            f"Cannot compute total rows because {csv_path} is missing."
        )
        with csv_path.open("r", encoding="utf-8") as f:
            # Subtract 1 for header
            total_rows += len(f.readlines()) - 1

    assert total_rows == 9, (
        f"Combined data rows across all CSV files should be 9, "
        f"but found {total_rows}."
    )


def test_diagnostics_file_not_present_yet():
    """
    Before the student runs their solution, the diagnostics file
    should NOT exist.  Its presence would indicate prior execution
    or an incorrect initial state.
    """
    assert not DIAGNOSTICS_FILE.exists(), (
        f"{DIAGNOSTICS_FILE} should NOT exist before the task is attempted, "
        f"but it was found."
    )