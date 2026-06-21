# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state
# before the student executes any solution commands.
#
# What we check:
# 1. The source CSV file exists at the expected absolute path.
# 2. The file is readable as UTF-8.
# 3. The header row is exactly as documented and contains six columns.
# 4. Every subsequent data row also has six comma-separated columns.
# 5. At least one data row has Country == "USA" so that the task is solvable.
#
# We intentionally DO NOT look for (or complain about) any output artefacts
# such as /home/user/output, usa_orders.csv, or us_sales_summary.txt.
#
# Only stdlib + pytest are used.

import csv
from pathlib import Path

import pytest

# Absolute path to the expected source CSV file
SOURCE_CSV = Path("/home/user/data/sales_2023_Q1.csv")

EXPECTED_HEADER = [
    "OrderID",
    "Date",
    "Country",
    "Product",
    "Quantity",
    "UnitPrice",
]


def test_source_csv_exists():
    """
    The starting CSV file must be present so that the student has something
    to work with.
    """
    assert SOURCE_CSV.exists(), (
        f"Required source file not found: {SOURCE_CSV}\n"
        "Make sure the file is present at the exact path given in the "
        "task description."
    )
    assert SOURCE_CSV.is_file(), f"Expected a file at {SOURCE_CSV}, but found something else."


def _read_csv_rows():
    """
    Helper that yields each CSV row as a list, preserving order.
    Raises clear pytest failures if any encoding issues occur.
    """
    try:
        with SOURCE_CSV.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                yield row
    except UnicodeDecodeError as e:
        pytest.fail(
            f"Failed to read {SOURCE_CSV} as UTF-8: {e}\n"
            "Ensure the file is UTF-8 encoded as specified."
        )


def test_header_is_correct():
    """
    Verify that the header row matches the specification exactly, both in
    column names and order.
    """
    rows = list(_read_csv_rows())
    assert rows, f"{SOURCE_CSV} appears to be empty."

    header = rows[0]
    assert header == EXPECTED_HEADER, (
        "CSV header does not match the required schema.\n"
        f"Expected: {EXPECTED_HEADER}\n"
        f"Found:    {header}"
    )


def test_all_rows_have_six_columns():
    """
    Every row—including the header—must contain exactly six comma-delimited
    columns so that simple awk/grep/cut solutions will not break.
    """
    for line_no, row in enumerate(_read_csv_rows(), start=1):
        assert len(row) == 6, (
            f"Row {line_no} in {SOURCE_CSV} has {len(row)} columns; "
            "expected exactly 6."
        )


def test_at_least_one_usa_record_present():
    """
    The task requires isolating U.S. orders.  Ensure there is at least one
    such record so the assignment is feasible.
    """
    usa_rows = [
        row
        for idx, row in enumerate(_read_csv_rows())
        if idx != 0 and row[2] == "USA"  # idx==0 is the header
    ]
    assert usa_rows, (
        f"No rows with Country == 'USA' were found in {SOURCE_CSV}. "
        "The student would have nothing to filter."
    )