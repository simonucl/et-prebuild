# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system and SQLite
# environment before the student runs any solution code.  It confirms that
# the live database is present and correct, while the diagnostic directory
# and log file are *not* yet created.

import os
import sqlite3
import re
import pytest
from datetime import datetime

# ---------- Constants --------------------------------------------------------

HOME_DIR       = "/home/user"
DB_DIR         = f"{HOME_DIR}/support/db"
DB_PATH        = f"{DB_DIR}/shop.db"
DIAG_DIR       = f"{HOME_DIR}/support/diag"
LOG_PATH       = f"{DIAG_DIR}/healthcheck.log"

# Ground-truth values expected on disk
EXPECTED_COUNTS = {
    "Total_Customers": 3,
    "Total_Orders":    5,
    "OPEN":            2,
    "SHIPPED":         2,
    "CANCELLED":       1,
}


# ---------- Helper -----------------------------------------------------------

def _connect_readonly(db_path):
    """
    Open the SQLite database in read-only mode so tests cannot mutate state.
    """
    uri_path = f"file:{db_path}?mode=ro"
    return sqlite3.connect(uri_path, uri=True)


# ---------- Filesystem / Path tests -----------------------------------------

def test_db_directory_exists():
    assert os.path.isdir(DB_DIR), (
        f"Expected database directory '{DB_DIR}' to exist but it does NOT."
    )


def test_db_file_exists():
    assert os.path.isfile(DB_PATH), (
        f"Expected SQLite database file '{DB_PATH}' to exist but it does NOT."
    )


def test_diag_directory_absent():
    assert not os.path.exists(DIAG_DIR), (
        f"Diagnostic directory '{DIAG_DIR}' should NOT exist before the student "
        f"runs their script."
    )


def test_log_file_absent():
    assert not os.path.exists(LOG_PATH), (
        f"Diagnostic log '{LOG_PATH}' should NOT exist before the student "
        f"runs their script."
    )


# ---------- Database content tests ------------------------------------------

def test_tables_present():
    with _connect_readonly(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cur.fetchall()}
    missing = {"customers", "orders"} - tables
    assert not missing, (
        f"Database is missing expected tables: {', '.join(sorted(missing))}"
    )


def test_customer_count():
    with _connect_readonly(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers;")
        count = cur.fetchone()[0]
    assert count == EXPECTED_COUNTS["Total_Customers"], (
        f"Expected {EXPECTED_COUNTS['Total_Customers']} rows in 'customers' "
        f"but found {count}."
    )


def test_order_count():
    with _connect_readonly(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM orders;")
        count = cur.fetchone()[0]
    assert count == EXPECTED_COUNTS["Total_Orders"], (
        f"Expected {EXPECTED_COUNTS['Total_Orders']} rows in 'orders' "
        f"but found {count}."
    )


@pytest.mark.parametrize("status", ["OPEN", "SHIPPED", "CANCELLED"])
def test_order_counts_by_status(status):
    with _connect_readonly(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM orders WHERE status = ?;",
            (status,)
        )
        count = cur.fetchone()[0]
    expected = EXPECTED_COUNTS[status]
    assert count == expected, (
        f"Expected {expected} rows in 'orders' with status '{status}' "
        f"but found {count}."
    )


def test_integrity_check_ok():
    with _connect_readonly(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA integrity_check;")
        result = cur.fetchone()[0]
    assert result == "ok", (
        "PRAGMA integrity_check did not return 'ok' — database might be corrupt."
    )