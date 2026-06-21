# test_initial_state.py
#
# Pytest suite that validates the operating-system state **before** the
# student performs any actions.  It intentionally checks *only* the
# pre-populated artefacts and **never** looks for the files/directories
# that the student is supposed to create later.

import os
import sqlite3
import pytest

DB_PATH = "/home/user/data/sales.db"


@pytest.fixture(scope="module")
def connection():
    """
    Provide a read-only SQLite connection to the pre-existing database.
    The connection is closed automatically when the module’s tests end.
    """
    if not os.path.isfile(DB_PATH):
        pytest.fail(f"Required database file not found at {DB_PATH!r}")
    try:
        # Opening URI with mode=ro guarantees we never modify the DB.
        con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    except sqlite3.Error as e:
        pytest.fail(f"Cannot open SQLite database at {DB_PATH!r}: {e}")
    yield con
    con.close()


def test_sales_db_file_exists_and_is_readable():
    """
    The database file must exist and be a regular, readable file.
    """
    assert os.path.exists(DB_PATH), (
        f"Expected database file at {DB_PATH}, but it does not exist."
    )
    assert os.path.isfile(DB_PATH), (
        f"Expected {DB_PATH} to be a file, but it is not."
    )
    assert os.access(DB_PATH, os.R_OK), (
        f"Database file {DB_PATH} is not readable."
    )


def test_required_tables_present(connection):
    """
    The database must contain at least the tables `customers` and `orders`.
    """
    cur = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    tables = {row[0] for row in cur.fetchall()}
    missing = {"customers", "orders"} - tables
    assert not missing, (
        "Database is missing required tables: "
        + ", ".join(sorted(missing))
    )


def test_required_tables_have_rows(connection):
    """
    Both `customers` and `orders` tables must contain at least one row each.
    """
    for table in ("customers", "orders"):
        cur = connection.execute(f"SELECT COUNT(*) FROM {table};")
        count = cur.fetchone()[0]
        assert count > 0, (
            f"Table '{table}' is expected to have at least one row, "
            f"but it contains {count} rows."
        )