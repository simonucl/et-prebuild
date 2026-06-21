# test_initial_state.py
#
# This pytest suite validates that the machine starts in the correct
# initial state *before* the student runs any commands.
#
# Specifically, it checks that:
#   • The SQLite database file exists at /home/user/data/warehouse.db
#   • The database contains a table named `inventory`
#   • The `inventory` table has the exact expected schema
#   • The table holds exactly the five expected rows
#   • The grand total of the `qty` column is 42
#
# No checks are performed on any output paths because those are part of
# the student’s deliverables and must not be asserted here.

import os
import sqlite3
import pytest

DB_PATH = "/home/user/data/warehouse.db"

EXPECTED_SCHEMA = [
    # (name, type, notnull, pk)
    ("id", "INTEGER", 0, 1),
    ("item", "TEXT", 1, 0),
    ("qty", "INTEGER", 1, 0),
]

EXPECTED_ROWS = [
    (1, "bolts",   10),
    (2, "nuts",    12),
    (3, "washers",  8),
    (4, "screws",   7),
    (5, "spacers",  5),
]

EXPECTED_QTY_TOTAL = 42


def open_connection():
    """Helper that opens a read-only SQLite connection."""
    # Using URI mode with immutable=1 guarantees we never modify the DB.
    uri = f"file:{DB_PATH}?mode=ro&immutable=1"
    return sqlite3.connect(uri, uri=True)


def test_database_file_exists():
    """The SQLite database file must be present before the exercise begins."""
    assert os.path.isfile(DB_PATH), (
        f"Expected database file not found: {DB_PATH}"
    )


def test_inventory_table_schema():
    """Verify that the `inventory` table exists with the exact schema."""
    with open_connection() as conn:
        cur = conn.cursor()

        # Confirm table exists
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='inventory';"
        )
        assert cur.fetchone(), (
            "Table `inventory` is missing in the SQLite database."
        )

        # Inspect schema
        cur.execute("PRAGMA table_info(inventory);")
        cols = cur.fetchall()  # cid, name, type, notnull, dflt_value, pk
        simplified = [(c[1], c[2].upper(), c[3], c[5]) for c in cols]

        assert simplified == EXPECTED_SCHEMA, (
            "Schema mismatch for table `inventory`.\n"
            f"Expected: {EXPECTED_SCHEMA}\n"
            f"Found:    {simplified}"
        )


def test_inventory_table_contents():
    """Ensure the table contains exactly the five expected rows and totals 42."""
    with open_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, item, qty FROM inventory ORDER BY id;")
        rows = cur.fetchall()

        assert rows == EXPECTED_ROWS, (
            "Contents of `inventory` table are not as expected.\n"
            f"Expected rows:\n{EXPECTED_ROWS}\n"
            f"Found rows:\n{rows}"
        )

        total_qty = sum(r[2] for r in rows)
        assert total_qty == EXPECTED_QTY_TOTAL, (
            f"Expected total qty to be {EXPECTED_QTY_TOTAL}, "
            f"but found {total_qty}."
        )