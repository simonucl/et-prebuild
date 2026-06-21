# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state **before**
# any student code is executed.
#
# What we verify here:
#   1. Raw data directory exists at /home/user/data/raw.
#   2. Two source files exist:
#        • customers.json  (must be valid JSON array with the expected 4 items)
#        • purchases.csv   (must have the correct header row and 6 rows)
#   3. File contents conform to the specification given in the task
#      description so that downstream checks can rely on them.
#
# NOTE: We intentionally do *not* test for the presence or absence of the
#       processed directory or any output files, in accordance with the
#       grading-infrastructure rules.

import csv
import json
import os
from pathlib import Path

import pytest

RAW_DIR = Path("/home/user/data/raw")
CUSTOMERS_JSON = RAW_DIR / "customers.json"
PURCHASES_CSV = RAW_DIR / "purchases.csv"


# ---------- Helper functions -------------------------------------------------
def _read_json_file(path: Path):
    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def _read_csv_file(path: Path):
    with path.open(encoding="utf-8") as fp:
        reader = csv.reader(fp)
        return list(reader)  # list[list[str]]


# ---------- Tests ------------------------------------------------------------
def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing. "
        "The raw source data must be located here."
    )


def test_customers_json_exists_and_is_valid():
    assert CUSTOMERS_JSON.is_file(), (
        f"Expected JSON file {CUSTOMERS_JSON} does not exist."
    )

    data = _read_json_file(CUSTOMERS_JSON)
    assert isinstance(data, list), (
        f"{CUSTOMERS_JSON} is not a JSON array as required."
    )

    # Expected number of customers and required keys
    expected_len = 4
    required_keys = {"customer_id", "name", "signup_date"}
    assert len(data) == expected_len, (
        f"{CUSTOMERS_JSON} should contain {expected_len} customers, "
        f"found {len(data)}."
    )
    for idx, customer in enumerate(data, start=1):
        assert required_keys.issubset(customer.keys()), (
            f"Customer object at index {idx-1} is missing one of the required "
            f"keys {sorted(required_keys)}."
        )

    # Confirm the precise IDs we expect; this guards against accidental edits.
    expected_ids = {1, 2, 3, 4}
    actual_ids = {c["customer_id"] for c in data}
    assert actual_ids == expected_ids, (
        f"{CUSTOMERS_JSON} should contain customer_id values "
        f"{sorted(expected_ids)}, found {sorted(actual_ids)}."
    )


def test_purchases_csv_exists_and_is_valid():
    assert PURCHASES_CSV.is_file(), (
        f"Expected CSV file {PURCHASES_CSV} does not exist."
    )

    rows = _read_csv_file(PURCHASES_CSV)
    assert rows, f"{PURCHASES_CSV} is empty."

    # Header validation
    header = rows[0]
    expected_header = [
        "purchase_id",
        "customer_id",
        "amount",
        "date",
    ]
    assert header == expected_header, (
        f"CSV header in {PURCHASES_CSV} is {header!r}, "
        f"but must be exactly {expected_header!r}."
    )

    # Data rows validation
    data_rows = rows[1:]
    expected_num_rows = 6
    assert len(data_rows) == expected_num_rows, (
        f"{PURCHASES_CSV} should contain {expected_num_rows} data rows "
        f"(excluding the header), found {len(data_rows)}."
    )

    # Check that purchase_id column contains the expected IDs
    purchase_ids = [int(r[0]) for r in data_rows]
    expected_ids = [1001, 1002, 1003, 1004, 1005, 1006]
    assert purchase_ids == expected_ids, (
        f"purchase_id column must be {expected_ids}, found {purchase_ids}."
    )