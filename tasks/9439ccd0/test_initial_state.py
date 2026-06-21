# test_initial_state.py
# -------------------------------------------------
# Pytest suite that validates the machine *before* the
# student starts working on the “CSV-cleaning” task.
#
# It checks that:
#   • The expected raw files are present with the exact
#     initial contents (including the PII columns).
#   • No cleaned-data or scan-log directories/files
#     exist yet.
#
# Only Python stdlib + pytest are used.

import os
import csv
from pathlib import Path

RAW_DIR = Path("/home/user/raw_data")
CLEAN_DIR = Path("/home/user/cleaned_data")
SCAN_DIR = Path("/home/user/scan_logs")

CUSTOMERS_RAW = RAW_DIR / "customers.csv"
TRANSACTIONS_RAW = RAW_DIR / "transactions.csv"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path):
    """Return a list of rows (each a list of strings) from the CSV file."""
    with path.open(newline="") as f:
        reader = csv.reader(f)
        return [row for row in reader]

def assert_not_exists(path: Path, kind: str):
    assert not path.exists(), f"{kind} {path} must NOT exist yet, but it does."

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), f"Required directory {RAW_DIR} is missing."


def test_customers_csv_exists_and_contents():
    assert CUSTOMERS_RAW.is_file(), f"Required file {CUSTOMERS_RAW} is missing."

    expected_rows = [
        ["id", "name", "email", "ssn", "phone", "country"],
        ["1", "Jane Doe", "jane.doe@example.com", "123-45-6789", "555-1234", "US"],
        ["2", "Bob Smith", "bob.smith@example.net", "987-65-4321", "555-2345", "US"],
    ]

    actual_rows = read_csv(CUSTOMERS_RAW)

    # Strip possible trailing blank rows
    actual_rows = [row for row in actual_rows if any(col.strip() for col in row)]

    assert actual_rows == expected_rows, (
        f"{CUSTOMERS_RAW} contents do not match expectation.\n"
        f"Expected:\n{expected_rows}\n\nActual:\n{actual_rows}"
    )


def test_transactions_csv_exists_and_contents():
    assert TRANSACTIONS_RAW.is_file(), f"Required file {TRANSACTIONS_RAW} is missing."

    expected_rows = [
        ["txn_id", "card_number", "cvv", "amount", "email", "ssn"],
        ["T1001", "4242424242424242", "123", "19.99", "alice@data.org", "000-12-3456"],
        ["T1002", "4000056655665556", "999", "7.50", "bob.smith@example.net", "987-65-4321"],
    ]

    actual_rows = read_csv(TRANSACTIONS_RAW)
    actual_rows = [row for row in actual_rows if any(col.strip() for col in row)]

    assert actual_rows == expected_rows, (
        f"{TRANSACTIONS_RAW} contents do not match expectation.\n"
        f"Expected:\n{expected_rows}\n\nActual:\n{actual_rows}"
    )


def test_no_cleaned_or_scan_directories_exist():
    """
    Ensure that the student has not prematurely created output artefacts.
    Both directories (and their expected files) must be absent at this stage.
    """
    for directory in (CLEAN_DIR, SCAN_DIR):
        assert_not_exists(directory, "Directory")

    # Specific files that must not yet exist
    for path in [
        CLEAN_DIR / "customers_clean.csv",
        CLEAN_DIR / "transactions_clean.csv",
        SCAN_DIR / "security_scan.log",
        CLEAN_DIR / "README.txt",
    ]:
        assert_not_exists(path, "File")