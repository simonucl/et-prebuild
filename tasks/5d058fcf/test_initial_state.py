# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state required for the “Iris minimum-petal-width” exercise.
#
# The checks purposefully run **before** the student’s bash command is
# executed.  They assert that:
#
# 1. The SQLite database file exists at the expected absolute path.
# 2. A working sqlite3 CLI is discoverable in the current $PATH.
# 3. The database contains a single table named `iris`.
# 4. The `iris` table has the exact five-column schema specified.
# 5. The minimum value in `petal_width` is *already* the known truth
#    value `0.1`, ensuring that the grader’s reference answer is valid.
#
# All assertions include clear failure messages so that any mismatch
# between the real environment and the specification is immediately
# obvious.

import os
import shutil
import sqlite3
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DB_PATH = Path("/home/user/ml/iris.db")
EXPECTED_TABLE = "iris"
EXPECTED_SCHEMA = [
    ("sepal_length", "REAL"),
    ("sepal_width", "REAL"),
    ("petal_length", "REAL"),
    ("petal_width", "REAL"),
    ("species", "TEXT"),
]
EXPECTED_MIN_PETAL_WIDTH = 0.1


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _connect_db():
    """Return a sqlite3.Connection to the iris.db file."""
    return sqlite3.connect(str(DB_PATH))


def _table_exists(conn, table_name):
    """Return True/False depending on whether a table exists in the DB."""
    cursor = conn.execute(
        """
        SELECT 1
          FROM sqlite_master
         WHERE type = 'table'
           AND name = ?
        """,
        (table_name,),
    )
    return cursor.fetchone() is not None


def _get_table_schema(conn, table_name):
    """
    Return a list of (col_name, col_type) pairs in the order
    defined in the table schema.
    """
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    return [(row[1], row[2].upper()) for row in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_sqlite_cli_available():
    """
    The sqlite3 command-line client must be available in $PATH so that the
    learner can invoke it directly from the shell.
    """
    sqlite_cli = shutil.which("sqlite3")
    assert (
        sqlite_cli
    ), "sqlite3 executable not found in PATH; please install SQLite command-line tools."


def test_database_file_exists():
    """
    The iris.db file must be present so that students can query it.
    """
    assert DB_PATH.is_file(), f"Expected database file not found: {DB_PATH}"


@pytest.fixture(scope="module")
def db_conn():
    """
    Module-scoped fixture that opens a read-only connection to the database.
    """
    # Open in read-only mode (`mode=ro`) to avoid accidental modifications.
    uri = f"file:{DB_PATH}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    yield conn
    conn.close()


def test_iris_table_exists(db_conn):
    """
    The database must contain exactly one table named 'iris'.
    """
    assert _table_exists(
        db_conn, EXPECTED_TABLE
    ), f"Table '{EXPECTED_TABLE}' not found in {DB_PATH}."


def test_iris_table_schema(db_conn):
    """
    The 'iris' table schema must match the specification exactly, both in
    column order and data types.
    """
    actual_schema = _get_table_schema(db_conn, EXPECTED_TABLE)
    assert (
        actual_schema == EXPECTED_SCHEMA
    ), f"Schema mismatch for table '{EXPECTED_TABLE}'.\n" \
       f"Expected: {EXPECTED_SCHEMA}\n" \
       f"Actual:   {actual_schema}"


def test_min_petal_width_value(db_conn):
    """
    Confirm that the minimum value in the petal_width column is the expected
    reference value used by the autograder.
    """
    cursor = db_conn.execute(f"SELECT MIN(petal_width) FROM {EXPECTED_TABLE}")
    result = cursor.fetchone()
    assert result is not None, "'SELECT MIN(petal_width)' returned no rows."
    min_value = result[0]
    assert (
        abs(min_value - EXPECTED_MIN_PETAL_WIDTH) < 1e-6
    ), f"Minimum petal_width mismatch.\n" \
       f"Expected: {EXPECTED_MIN_PETAL_WIDTH}\n" \
       f"Actual:   {min_value}"