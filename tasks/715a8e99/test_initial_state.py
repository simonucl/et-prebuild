# test_initial_state.py
#
# This pytest suite verifies the **initial** operating-system / filesystem state
# before the student begins working on the migration task.  It intentionally
# checks only the *pre-existing* items (the source database) and stays away from
# any files or directories that the student is expected to create later.
#
# IMPORTANT: Do **not** modify these tests.  If they fail, it means the starting
# environment is not correctly provisioned.

import os
import sqlite3
import pytest

SOURCE_DB = "/home/user/source_data.db"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _open_db(path):
    """Open an SQLite database in read-only mode."""
    if not os.path.isfile(path):
        pytest.fail(f"Expected database file not found at '{path}'.")
    # The URI format with mode=ro prevents accidental modification.
    uri = f"file:{path}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Unable to open SQLite database '{path}' in read-only mode: {exc}")
    return conn


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_source_db_exists():
    """The source SQLite database file must exist at the exact expected path."""
    assert os.path.isfile(
        SOURCE_DB
    ), f"Source database file was expected at '{SOURCE_DB}' but was not found."


def test_source_db_has_single_table_named_dataset():
    """
    The database should have exactly one table and it must be named 'dataset'.
    """
    conn = _open_db(SOURCE_DB)
    try:
        cursor = conn.execute(
            """
            SELECT name
              FROM sqlite_master
             WHERE type='table'
            """
        )
        tables = [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()

    assert tables, "The source database contains no tables."
    assert tables == [
        "dataset"
    ], (
        "The source database must contain exactly one table named 'dataset'. "
        f"Found tables: {tables}"
    )


def test_dataset_table_schema_is_correct():
    """
    The 'dataset' table must have the exact schema:
        id    INTEGER PRIMARY KEY
        value TEXT
    """
    conn = _open_db(SOURCE_DB)
    try:
        pragma_rows = conn.execute("PRAGMA table_info('dataset')").fetchall()
    finally:
        conn.close()

    # PRAGMA table_info columns: cid, name, type, notnull, dflt_value, pk
    expected = [
        ("id", "INTEGER", 1),   # pk == 1 for primary key
        ("value", "TEXT", 0),   # pk == 0 for non-primary key column
    ]
    actual = [(row[1], row[2].upper(), row[5]) for row in pragma_rows]

    assert actual == expected, (
        "Schema mismatch in 'dataset' table.\n"
        f"Expected columns (name, type, pk flag): {expected}\n"
        f"Actual columns: {actual}"
    )


def test_dataset_table_contains_expected_rows():
    """
    The 'dataset' table must contain exactly three rows with the expected values:
        1 | alpha
        2 | beta
        3 | gamma
    """
    conn = _open_db(SOURCE_DB)
    try:
        rows = conn.execute("SELECT id, value FROM dataset ORDER BY id").fetchall()
    finally:
        conn.close()

    expected_rows = [(1, "alpha"), (2, "beta"), (3, "gamma")]

    assert rows == expected_rows, (
        "Row contents of 'dataset' table do not match expectations.\n"
        f"Expected: {expected_rows}\n"
        f"Found   : {rows}"
    )