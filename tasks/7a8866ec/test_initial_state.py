# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# BEFORE the student performs any action.
# The checks focus exclusively on the pre-existing SQLite database.
#
# • Only the standard library and pytest are used.
# • We purposefully do NOT test for the presence of the output file
#   `/home/user/profile_report/avg_cpu_usage.txt`, because it should
#   be created by the student as part of the task.

import os
import sqlite3
import pytest
from pathlib import Path

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

DB_PATH = Path("/home/user/projects/profile/data.db").resolve()

EXPECTED_ROWS = [
    (1, "auth", 55.2),
    (2, "api",  70.8),
    (3, "db",   65.0),
    (4, "ui",   40.0),
]

EXPECTED_AVG = 57.75  # Provided by the exercise statement.

EXPECTED_SCHEMA = [
    # (cid, name, type, notnull, dflt_value, pk)
    (0, "id",        "INTEGER", 0, None, 1),  # Primary key
    (1, "component", "TEXT",    0, None, 0),
    (2, "cpu_usage", "REAL",    0, None, 0),
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def _open_connection(db_path: Path):
    """Return a sqlite3 connection to the given database path."""
    return sqlite3.connect(str(db_path))

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_db_file_exists_and_is_readable():
    """
    The SQLite database must already exist at the exact absolute path and
    be readable by the current user.
    """
    assert DB_PATH.is_file(), (
        f"Expected database file not found: {DB_PATH}\n"
        f"Make sure the file exists at this precise location."
    )
    # Basic readability check
    try:
        with DB_PATH.open("rb"):
            pass
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Database file exists but cannot be opened for reading: {exc}")

def test_table_schema_is_correct():
    """
    The `metrics` table must exist with the exact column order, names,
    SQLite types, and primary-key definition described in the spec.
    """
    with _open_connection(DB_PATH) as conn:
        cur = conn.cursor()

        # Verify that the table exists
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'metrics';"
        )
        table = cur.fetchone()
        assert table is not None, (
            "Table `metrics` not found in the database. "
            "Expected schema is missing."
        )

        # Inspect table schema
        cur.execute("PRAGMA table_info(metrics);")
        schema_rows = cur.fetchall()

        # Normalize the schema for comparison: keep only the first 6 fields
        normalized_schema = [
            (cid, name, type_, notnull, dflt_value, pk)
            for cid, name, type_, notnull, dflt_value, pk in schema_rows
        ]
        assert normalized_schema == EXPECTED_SCHEMA, (
            "Schema mismatch detected for table `metrics`.\n"
            f"Expected (cid, name, type, notnull, dflt_value, pk):\n  {EXPECTED_SCHEMA}\n"
            f"Actual:\n  {normalized_schema}"
        )

def test_initial_rows_are_present_and_correct():
    """
    The `metrics` table must contain exactly four rows with the precise
    (id, component, cpu_usage) values defined in the task description.
    """
    with _open_connection(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, component, cpu_usage FROM metrics ORDER BY id;")
        rows = cur.fetchall()

    assert rows == EXPECTED_ROWS, (
        "Row contents of `metrics` table do not match the expected initial state.\n"
        f"Expected (ordered by id):\n  {EXPECTED_ROWS}\n"
        f"Actual:\n  {rows}"
    )

def test_average_cpu_usage_is_accurate():
    """
    The arithmetic mean of the `cpu_usage` column should equal 57.75.
    This value is used later to grade the student's generated report.
    """
    with _open_connection(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT ROUND(AVG(cpu_usage), 2) FROM metrics;")
        (avg_value,) = cur.fetchone()

    assert abs(avg_value - EXPECTED_AVG) < 1e-9, (
        "Computed average CPU usage from the database does not equal the "
        f"expected value of {EXPECTED_AVG:.2f}.\n"
        f"Actual average: {avg_value:.2f}"
    )