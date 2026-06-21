# test_initial_state.py
#
# This pytest suite verifies the **initial** environment state _before_ the
# student runs any solution commands.  It ensures that all prerequisites are in
# place (database, schema, test-data) and that no artefact of the final result
# (api_status_summary.txt) is present yet.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

HOME = Path("/home/user")
DB_PATH = HOME / "dev_data" / "api_responses.db"
OUTPUT_PATH = HOME / "api_status_summary.txt"


@pytest.fixture(scope="session")
def db_conn():
    """Return a read-only sqlite3 connection to the prepared database."""
    if not DB_PATH.exists():
        pytest.skip(f"Database file {DB_PATH} is missing; can’t run DB tests.")
    # Open read-only: prepend URI header and use mode=ro to avoid accidental writes
    uri = f"file:{DB_PATH}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def test_database_file_exists():
    assert DB_PATH.exists(), (
        f"The expected SQLite database file {DB_PATH} is missing. "
        "It must be pre-populated by the test harness."
    )
    assert DB_PATH.is_file(), f"{DB_PATH} exists but is not a regular file."


def test_database_schema(db_conn):
    """Validate that the 'responses' table exists with the correct schema."""
    cur = db_conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='responses';
    """)
    row = cur.fetchone()
    assert row is not None, "Table 'responses' is missing from the database."

    # Check column definitions
    cur.execute("PRAGMA table_info('responses');")
    cols = [(c[1], c[2].upper()) for c in cur.fetchall()]  # (name, declared_type)
    expected = [
        ("id", "INTEGER"),
        ("endpoint", "TEXT"),
        ("status_code", "INTEGER"),
        ("ts", "TEXT"),
    ]
    assert cols == expected, (
        "Table 'responses' schema mismatch.\n"
        f"Expected columns: {expected}\n"
        f"Found columns   : {cols}"
    )


def test_database_seed_data(db_conn):
    """Verify that the seed rows are present exactly as described."""
    cur = db_conn.cursor()
    cur.execute("SELECT * FROM responses ORDER BY id;")
    rows = cur.fetchall()

    expected_rows = [
        (1, "/v1/accounts", 200, "2023-10-01T10:00:00Z"),
        (2, "/v1/accounts", 500, "2023-10-01T10:01:00Z"),
        (3, "/v1/accounts", 200, "2023-10-01T10:02:00Z"),
        (4, "/v1/payments", 200, "2023-10-01T10:03:00Z"),
    ]

    assert rows == expected_rows, (
        "Seed data in 'responses' does not match expectations.\n"
        f"Expected rows:\n{expected_rows}\n"
        f"Found rows   :\n{rows}"
    )


def test_output_file_absent_initially():
    """The summary file must NOT exist before the student's command runs."""
    assert not OUTPUT_PATH.exists(), (
        f"Output file {OUTPUT_PATH} already exists. "
        "It should only be created by the student's solution command."
    )