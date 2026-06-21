# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct **initial** state before the student begins the task.
# Only standard-library modules and pytest are used.

from pathlib import Path
import textwrap
import pytest

# Base paths used throughout the tests
BASE_DIR = Path("/home/user/cloud_costs")
RAW_DIR = BASE_DIR / "raw"
CSV_PATH = RAW_DIR / "march_2024_spend.csv"

# The exact CSV content that must already be present (including final newline)
EXPECTED_CSV_CONTENT = textwrap.dedent("""\
    Date,Account,Service,CostUSD
    2024-03-01,Dev,Compute,15.50
    2024-03-02,Prod,Compute,25.00
    2024-03-03,Dev,Storage,5.25
    2024-03-04,Prod,Storage,12.75
    2024-03-05,Dev,Database,20.00
    2024-03-06,Prod,Database,30.00
    2024-03-07,Dev,Networking,7.00
    2024-03-08,Prod,Networking,14.00
""")  # pytest will strip nothing; dedent keeps the trailing newline


def test_directories_exist():
    """Verify that /home/user/cloud_costs and /home/user/cloud_costs/raw both exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory '{BASE_DIR}' is missing. "
        "Create it before running the solution."
    )
    assert RAW_DIR.is_dir(), (
        f"Required directory '{RAW_DIR}' is missing. "
        "Create it before running the solution."
    )


def test_csv_file_exists_and_is_regular():
    """Verify the raw CSV file exists and is a regular file (not a directory or symlink)."""
    assert CSV_PATH.exists(), (
        f"Required CSV file '{CSV_PATH}' does not exist. "
        "Place the raw usage-and-spend export in this location."
    )
    assert CSV_PATH.is_file(), (
        f"'{CSV_PATH}' exists but is not a regular file. "
        "Ensure it is a normal CSV file."
    )


def test_csv_file_contents_exact_match():
    """
    Confirm the CSV file's contents match the expected dataset exactly,
    including header order, numeric precision, and final newline.
    """
    actual = CSV_PATH.read_text(encoding="utf-8")
    # Enforce presence of the final newline in the expected string
    if not EXPECTED_CSV_CONTENT.endswith("\n"):
        pytest.fail(
            "Internal test error: EXPECTED_CSV_CONTENT is missing the trailing newline."
        )
    assert actual == EXPECTED_CSV_CONTENT, (
        "The contents of the CSV file do not match the expected initial dataset.\n"
        "If this file was modified, please restore it to the exact original contents:\n"
        f"{CSV_PATH}"
    )