# test_initial_state.py
"""
Pytest test-suite that validates the machine’s initial state *before*
the student performs any actions for the “SQLite audit” task.

The checks assert:
1. The audit database file exists at the expected absolute path.
2. Exactly one table named `system_access` is present.
3. The table schema matches the specification.
4. The pre-loaded dataset is exactly as described and yields three
   failed log-in attempts for June 2024.
5. The result file that the student must create **does not yet exist**.

Failures give clear, actionable messages.
"""

import os
import sqlite3
import stat
import pytest
from pathlib import Path

# ----------  CONSTANTS  ------------------------------------------------------

DB_PATH = Path("/home/user/audit_data/compliance.db")
OUTPUT_DIR = Path("/home/user/audit_logs")
OUTPUT_FILE = OUTPUT_DIR / "june_fail_count.log"

# Expected schema: list of (cid, name, type, notnull, dflt_value, pk)
EXPECTED_SCHEMA = [
    (0, "id", "INTEGER", 0, None, 1),          # PRIMARY KEY
    (1, "username", "TEXT", 1, None, 0),
    (2, "access_time", "TEXT", 1, None, 0),
    (3, "result", "TEXT", 1, None, 0),
]

# Expected rows in the table
EXPECTED_ROWS = [
    (1, "alice",   "2024-05-20 09:10:00", "SUCCESS"),
    (2, "bob",     "2024-06-02 14:55:00", "FAIL"),
    (3, "charlie", "2024-06-10 07:32:12", "FAIL"),
    (4, "dan",     "2024-06-15 15:45:30", "FAIL"),
    (5, "erin",    "2024-05-18 22:11:09", "FAIL"),
]

# ----------  HELPERS  --------------------------------------------------------


def open_db(path: Path):
    """Open SQLite DB in read-only mode and return the connection."""
    uri = f"file:{path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


# ----------  TESTS  ----------------------------------------------------------


def test_database_file_exists_and_is_readable():
    assert DB_PATH.exists(), (
        f"Expected database file {DB_PATH} to exist, but it is missing."
    )
    assert DB_PATH.is_file(), f"{DB_PATH} exists but is not a regular file."
    st = DB_PATH.stat()
    assert bool(st.st_mode & stat.S_IRUSR), (
        f"Database file {DB_PATH} is not readable by the current user."
    )


def test_exactly_one_system_access_table_present():
    with open_db(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        tables = [row[0] for row in cur.fetchall()]

    assert tables == ["system_access"], (
        "The database must contain exactly one table named 'system_access'. "
        f"Found tables: {tables}"
    )


def test_system_access_schema_matches_spec():
    with open_db(DB_PATH) as conn:
        cur = conn.execute("PRAGMA table_info(system_access);")
        schema = cur.fetchall()

    assert schema == EXPECTED_SCHEMA, (
        "Schema mismatch for table 'system_access'.\n"
        f"Expected:\n{EXPECTED_SCHEMA}\nFound:\n{schema}"
    )


def test_preloaded_rows_and_june_fail_count():
    with open_db(DB_PATH) as conn:
        cur = conn.execute("SELECT * FROM system_access ORDER BY id;")
        rows = cur.fetchall()

        assert rows == EXPECTED_ROWS, (
            "Pre-loaded rows in 'system_access' do not match the specification.\n"
            f"Expected:\n{EXPECTED_ROWS}\nFound:\n{rows}"
        )

        cur = conn.execute(
            """
            SELECT COUNT(*)
            FROM system_access
            WHERE result = 'FAIL' AND access_time LIKE '2024-06%';
            """
        )
        (count,) = cur.fetchone()

    assert count == 3, (
        "The June 2024 FAIL count should be 3 according to the ground truth, "
        f"but the query returned {count}."
    )


def test_output_file_absent_before_student_action():
    if OUTPUT_FILE.exists():
        pytest.fail(
            f"The result file {OUTPUT_FILE} should NOT exist before "
            "the student runs their command, but it is already present."
        )