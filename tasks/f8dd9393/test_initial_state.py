# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem
state **before** the student performs any steps for the diagnostic
snapshot task.

Rules respected:
  • Uses only the Python standard library + pytest.
  • Checks *only* pre-existing resources (no output files / directories).
  • All paths are absolute and rooted at /home/user.
"""

import os
import sqlite3
import textwrap
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = "/home/user"
DB_PATH = os.path.join(HOME, "app", "data", "service.db")

EXPECTED_CUSTOMERS = [
    (1, "Alice",   "London"),
    (2, "Bob",     "Paris"),
    (3, "Charlie", "Berlin"),
    (4, "Dana",    "London"),
]

EXPECTED_ORDERS = [
    (1, 1, 100.50),
    (2, 2, 200.00),
    (3, 1,  50.00),
    (4, 3,  75.25),
]

EXPECTED_CUSTOMERS_COLUMNS = ["id", "name", "city"]
EXPECTED_ORDERS_COLUMNS = ["id", "customer_id", "amount"]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _connect_db():
    """Return a sqlite3.Connection to the service.db database."""
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as exc:
        pytest.fail(f"Unable to connect to SQLite database at {DB_PATH}: {exc}")
    return conn


def _get_column_names(cursor, table_name):
    """Return a list of column names for a given table (preserving order)."""
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [row[1] for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_database_file_exists_and_is_not_empty():
    """Ensure the SQLite DB file exists and is non-empty."""
    assert os.path.isfile(DB_PATH), (
        f"Expected database file at {DB_PATH} does not exist."
    )
    assert os.path.getsize(DB_PATH) > 0, (
        f"Database file {DB_PATH} exists but is empty (size == 0 bytes)."
    )


def test_customers_table_schema():
    """Verify the 'customers' table exists with the expected columns."""
    conn = _connect_db()
    cur = conn.cursor()

    # Ensure table exists
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='customers';"
    )
    assert cur.fetchone(), (
        "Table 'customers' was not found in the SQLite database."
    )

    # Verify column layout
    actual_columns = _get_column_names(cur, "customers")
    assert actual_columns == EXPECTED_CUSTOMERS_COLUMNS, textwrap.dedent(
        f"""
        'customers' table has unexpected column definitions.
        Expected order  : {EXPECTED_CUSTOMERS_COLUMNS}
        Actual order    : {actual_columns}
        """
    )


def test_orders_table_schema():
    """Verify the 'orders' table exists with the expected columns."""
    conn = _connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='orders';"
    )
    assert cur.fetchone(), "Table 'orders' was not found in the SQLite database."

    actual_columns = _get_column_names(cur, "orders")
    assert actual_columns == EXPECTED_ORDERS_COLUMNS, textwrap.dedent(
        f"""
        'orders' table has unexpected column definitions.
        Expected order  : {EXPECTED_ORDERS_COLUMNS}
        Actual order    : {actual_columns}
        """
    )


def test_customers_table_seed_data():
    """Validate that the 'customers' table contains the expected seed data."""
    conn = _connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name, city FROM customers ORDER BY id;")
    rows = cur.fetchall()

    assert rows == EXPECTED_CUSTOMERS, textwrap.dedent(
        f"""
        'customers' table contents differ from expectations.
        Expected rows (ordered by id):
        {EXPECTED_CUSTOMERS}

        Actual rows:
        {rows}
        """
    )


def test_orders_table_seed_data():
    """Validate that the 'orders' table contains the expected seed data."""
    conn = _connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, customer_id, amount FROM orders ORDER BY id;")
    rows = cur.fetchall()

    # Convert numeric values exactly as stored
    # SQLite returns REALs as float; formatting isn't important here
    assert rows == EXPECTED_ORDERS, textwrap.dedent(
        f"""
        'orders' table contents differ from expectations.
        Expected rows (ordered by id):
        {EXPECTED_ORDERS}

        Actual rows:
        {rows}
        """
    )


def test_customers_by_city_counts():
    """Verify distinct city counts match the seed data."""
    conn = _connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT city, COUNT(*) AS cnt
        FROM customers
        GROUP BY city
        ORDER BY city;
    """)
    rows = cur.fetchall()

    expected = [
        ("Berlin", 1),
        ("London", 2),
        ("Paris", 1),
    ]

    assert rows == expected, textwrap.dedent(
        f"""
        Aggregated customer counts by city do not match expectations.
        Expected:
        {expected}

        Actual:
        {rows}
        """
    )