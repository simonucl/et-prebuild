# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state *before* the student starts the migration task.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Tests rely on absolute paths
#   • Does NOT reference any output files or directories that will be created
#   • Failure messages make it clear what is missing / incorrect

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants – absolute paths and the exact, ground-truth contents expected
# ---------------------------------------------------------------------------

CUSTOMERS_CSV = Path("/home/user/data/raw/customers.csv")
ORDERS_CSV = Path("/home/user/data/raw/orders.csv")

EXPECTED_CUSTOMERS_LINES = [
    "id,name,email",
    "1,Alice Smith,alice@example.com",
    "2,Bob Jones,bob@example.com",
    "3,Charlie Chen,charlie@example.com",
    "4,Diana Prince,diana@example.com",
    "5,Evan Davis,evan@example.com",
]

EXPECTED_ORDERS_LINES = [
    "id,customer_id,product,quantity",
    "1001,1,Keyboard,2",
    "1002,1,Mouse,1",
    "1003,2,Laptop,1",
    "1004,3,Monitor,2",
    "1005,3,USB Cable,5",
    "1006,4,Headset,1",
    "1007,4,Mouse Pad,3",
    "1008,5,Webcam,1",
]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _read_csv_lines(path: Path):
    """
    Read a CSV file and return its lines *without* trailing newline characters.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_customers_csv_exists():
    """Verify /home/user/data/raw/customers.csv is present and is a regular file."""
    assert CUSTOMERS_CSV.is_file(), (
        "Missing required file: "
        f"{CUSTOMERS_CSV}. Ensure the customers CSV is located exactly at this path."
    )


def test_customers_csv_contents():
    """Verify the customers.csv file contains the exact, expected rows."""
    lines = _read_csv_lines(CUSTOMERS_CSV)
    assert lines == EXPECTED_CUSTOMERS_LINES, (
        "Contents of customers.csv do not match the expected ground-truth.\n"
        f"Expected ({len(EXPECTED_CUSTOMERS_LINES)} lines):\n  "
        + "\n  ".join(EXPECTED_CUSTOMERS_LINES)
        + "\n\nActual ({len(lines)} lines):\n  "
        + "\n  ".join(lines)
    )


def test_orders_csv_exists():
    """Verify /home/user/data/raw/orders.csv is present and is a regular file."""
    assert ORDERS_CSV.is_file(), (
        "Missing required file: "
        f"{ORDERS_CSV}. Ensure the orders CSV is located exactly at this path."
    )


def test_orders_csv_contents():
    """Verify the orders.csv file contains the exact, expected rows."""
    lines = _read_csv_lines(ORDERS_CSV)
    assert lines == EXPECTED_ORDERS_LINES, (
        "Contents of orders.csv do not match the expected ground-truth.\n"
        f"Expected ({len(EXPECTED_ORDERS_LINES)} lines):\n  "
        + "\n  ".join(EXPECTED_ORDERS_LINES)
        + "\n\nActual ({len(lines)} lines):\n  "
        + "\n  ".join(lines)
    )