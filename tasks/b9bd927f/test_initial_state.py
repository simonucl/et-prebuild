# test_initial_state.py
#
# This test-suite asserts the *initial* filesystem state that must be
# present before the student runs any commands.  It deliberately ignores
# any expected output artefacts (e.g. /home/user/output/*) because those
# do not yet exist at this stage.
#
# Only the Python standard library and pytest are used.

import os
import csv
import pytest

SALES_CSV_PATH = "/home/user/data/sales.csv"

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------

def read_sales_rows():
    """
    Return (header, data_rows)

    * header        : list of column names
    * data_rows     : list[dict] – each dict is a parsed CSV record
    """
    if not os.path.exists(SALES_CSV_PATH):
        pytest.fail(
            f"Expected source CSV file at {SALES_CSV_PATH!r} but it was not found."
        )

    with open(SALES_CSV_PATH, "r", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        data_rows = list(reader)
    return header, data_rows


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_sales_csv_is_present_and_regular_file():
    """/home/user/data/sales.csv must exist and be a regular file."""
    assert os.path.exists(
        SALES_CSV_PATH
    ), f"File {SALES_CSV_PATH} is missing – it must be provided to the student."
    assert os.path.isfile(
        SALES_CSV_PATH
    ), f"{SALES_CSV_PATH} exists but is not a regular file."


def test_sales_csv_header_and_row_counts():
    """
    Validate the header and the total number of data rows present in
    /home/user/data/sales.csv.
    """
    header, data_rows = read_sales_rows()

    expected_header = ["order_id", "customer", "email", "amount"]
    assert header == expected_header, (
        "CSV header mismatch.\n"
        f"Expected: {expected_header}\n"
        f"Found   : {header}"
    )

    assert len(data_rows) == 10, (
        f"CSV should contain 10 data rows (excluding header) but found {len(data_rows)}."
    )


def test_sales_csv_contains_expected_edu_rows():
    """
    Ensure that exactly 5 rows have an email ending with '.edu'
    (case-insensitive) and that the specific order_ids match the truth.
    """
    _, data_rows = read_sales_rows()

    edu_rows = [
        row for row in data_rows if row["email"].lower().endswith(".edu")
    ]
    edu_order_ids = {int(row["order_id"]) for row in edu_rows}

    expected_order_ids = {1002, 1003, 1005, 1007, 1010}

    assert len(edu_rows) == 5, (
        "Exactly 5 data rows should have an email ending with '.edu' "
        f"(case-insensitive) but found {len(edu_rows)}."
    )

    assert edu_order_ids == expected_order_ids, (
        "The '.edu' rows do not match the expected set of order_ids.\n"
        f"Expected order_ids: {sorted(expected_order_ids)}\n"
        f"Found order_ids   : {sorted(edu_order_ids)}"
    )


def test_sales_csv_lines_are_newline_terminated():
    """
    All lines in the CSV file should be newline-terminated to avoid issues
    with line processing tools.
    """
    with open(SALES_CSV_PATH, "rb") as fh:
        for idx, raw_line in enumerate(fh, 1):
            assert raw_line.endswith(b"\n"), (
                f"Line {idx} in {SALES_CSV_PATH} is not newline-terminated."
            )