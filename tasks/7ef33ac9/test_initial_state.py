# test_initial_state.py
#
# Pytest suite that validates the presence and exact contents of the
# three source CSV files that must already exist *before* the student
# runs any commands or scripts.  The tests purposely avoid looking at – or
# even mentioning – any paths inside /home/user/output/ because the
# grading rules forbid that.

import os
import pytest

# ---------------------------------------------------------------------------
# Helper data: the exact, line-by-line contents we expect to find in each CSV
# file (excluding the terminating newline characters).
# ---------------------------------------------------------------------------

EXPECTED_Q1_LINES = [
    "OrderID,Product,Amount,Status",
    "1001,Laptop,1200,Completed",
    "1002,Mouse,25,Completed",
    "1003,Desk,300,Pending",
    "1004,Monitor,200,Cancelled",
    "1005,Phone,800,Completed",
    "1006,Server,2500,Completed",
]

EXPECTED_Q2_LINES = [
    "OrderID,Product,Amount,Status",
    "2001,Tablet,300,Completed",
    "2002,Chair,150,Pending",
    "2003,Headset,70,Completed",
    "2004,Printer,600,Completed",
    "2005,Camera,1100,Completed",
]

EXPECTED_Q3_LINES = [
    "OrderID,Product,Amount,Status",
    "3001,Router,90,Completed",
    "3002,Switch,1200,Completed",
    "3003,Desk,320,Cancelled",
    "3004,Laptop,1400,Completed",
    "3005,Microphone,80,Pending",
]

DATA_DIR = "/home/user/data"
Q1_PATH = f"{DATA_DIR}/Q1_sales.csv"
Q2_PATH = f"{DATA_DIR}/Q2_sales.csv"
Q3_PATH = f"{DATA_DIR}/Q3_sales.csv"


# ---------------------------------------------------------------------------
# Basic presence checks
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "path",
    [DATA_DIR, Q1_PATH, Q2_PATH, Q3_PATH],
)
def test_paths_exist(path):
    """
    Ensure that /home/user/data exists and that the three required CSV files
    are present.  Fail with an informative message if anything is missing.
    """
    assert os.path.exists(
        path
    ), f"Required path is missing: {path}"


def test_data_dir_is_directory():
    """Validate that /home/user/data is in fact a directory."""
    assert os.path.isdir(
        DATA_DIR
    ), f"{DATA_DIR} is expected to be a directory."


# ---------------------------------------------------------------------------
# Content verification
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "path, expected_lines",
    [
        (Q1_PATH, EXPECTED_Q1_LINES),
        (Q2_PATH, EXPECTED_Q2_LINES),
        (Q3_PATH, EXPECTED_Q3_LINES),
    ],
)
def test_csv_contents_exact(path, expected_lines):
    """
    Verify that each CSV file contains exactly the lines defined above and in
    the same order.  Whitespace matters: any deviation will fail the test and
    produce a clear diff in the assertion error.
    """
    with open(path, "r", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()
    assert (
        actual_lines == expected_lines
    ), f"Contents of {path} do not match the expected template."


@pytest.mark.parametrize(
    "path",
    [Q1_PATH, Q2_PATH, Q3_PATH],
)
def test_each_row_has_four_fields(path):
    """
    Extra defensive check: every row must have exactly four comma-separated
    fields.  This ensures the CSVs are well-formed before any processing.
    """
    with open(path, "r", encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            fields = line.rstrip("\n").split(",")
            assert len(fields) == 4, (
                f"{path}, line {line_number} has {len(fields)} fields "
                f"instead of 4: {line!r}"
            )