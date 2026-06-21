# test_initial_state.py
#
# This test-suite validates the **initial** filesystem / database state
# before the student executes any command.  Nothing related to the
# requested *output* path is checked, in accordance with the grading
# rules.
#
# What is verified:
#   1. /home/user/microservices/ exists and is a directory.
#   2. /home/user/microservices/logs.db exists and is a regular file.
#   3. The SQLite DB contains a table named `services` whose schema
#      matches the specification.
#   4. The table is pre-populated with the exact five rows described in
#      the task (three of which have status='running').
#
# Only stdlib and pytest are used.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

MICROSERVICES_DIR = Path("/home/user/microservices")
DB_PATH            = MICROSERVICES_DIR / "logs.db"

EXPECTED_ROWS = [
    (1, "auth-api",     "running"),
    (2, "payments-api", "stopped"),
    (3, "user-api",     "running"),
    (4, "metrics",      "running"),
    (5, "gateway",      "stopped"),
]

@pytest.fixture(scope="session")
def db_conn():
    """Return a read-only SQLite connection to logs.db."""
    uri = f"file:{DB_PATH.as_posix()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Unable to open the database in read-only mode: {exc}")
    yield conn
    conn.close()

def test_microservices_directory_exists():
    assert MICROSERVICES_DIR.exists(), (
        f"Required directory {MICROSERVICES_DIR} is missing."
    )
    assert MICROSERVICES_DIR.is_dir(), (
        f"{MICROSERVICES_DIR} exists but is not a directory."
    )

def test_logs_db_file_exists():
    assert DB_PATH.exists(), (
        f"SQLite database expected at {DB_PATH} is missing."
    )
    assert DB_PATH.is_file(), (
        f"{DB_PATH} exists but is not a regular file."
    )
    st = DB_PATH.stat()
    assert stat.S_ISREG(st.st_mode), (
        f"{DB_PATH} exists but is not a regular file (mode: {oct(st.st_mode)})"
    )

def test_services_table_schema(db_conn):
    cur = db_conn.execute("PRAGMA table_info(services);")
    rows = cur.fetchall()
    assert rows, (
        "Table 'services' is missing from the database."
    )

    # Extract column names and types in the order returned by PRAGMA.
    col_info = [(r[1], r[2].upper()) for r in rows]  # (name, declared_type)
    expected_schema = [
        ("id",     "INTEGER"),
        ("name",   "TEXT"),
        ("status", "TEXT"),
    ]
    # We care only about the first three columns matching the spec.
    assert col_info[:3] == expected_schema, (
        "Schema of table 'services' does not match the expected definition.\n"
        f"Expected first three columns: {expected_schema}\n"
        f"Found: {col_info}"
    )

def test_preloaded_services_rows(db_conn):
    cur = db_conn.execute(
        "SELECT id, name, status FROM services ORDER BY id;"
    )
    data = cur.fetchall()
    assert data, "Table 'services' is empty; expected pre-populated rows."
    assert data == EXPECTED_ROWS, (
        "Rows in 'services' table do not match the expected initial dataset.\n"
        f"Expected:\n  {EXPECTED_ROWS}\n"
        f"Found:\n  {data}"
    )

def test_running_services_count(db_conn):
    cur = db_conn.execute(
        "SELECT COUNT(*) FROM services WHERE status='running';"
    )
    (count,) = cur.fetchone()
    expected_count = 3
    assert count == expected_count, (
        f"Expected {expected_count} rows with status='running', "
        f"but found {count}."
    )