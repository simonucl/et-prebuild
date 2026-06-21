# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system
# before the learner performs any migration work.
#
# What we check
# -------------
# 1. /home/user/legacy/old_db.sqlite exists and is a regular file.
# 2. The database contains a table called `employees` whose schema matches the
#    specification.
# 3. The table `employees` contains exactly the expected five rows.
#
# We intentionally do *not* look for any artefacts that the learner is
# expected to create (e.g. /home/user/migration, new_db.sqlite, log files).
#
# Only stdlib modules are used, in accordance with the rules.

import os
import sqlite3
import pytest
from pathlib import Path

SOURCE_DB = Path("/home/user/legacy/old_db.sqlite")

# Expected rows, sorted by the primary key `id`
EXPECTED_ROWS = [
    (1, "Ava",  "Moore",   "Engineering"),
    (2, "Liam", "Johnson", "Finance"),
    (3, "Emma", "Davis",   "Marketing"),
    (4, "Noah", "Wilson",  "HR"),
    (5, "Mia",  "Brown",   "Sales"),
]

# Expected schema information as returned by PRAGMA table_info(employees);
# Each entry is: (cid, name, type, notnull, dflt_value, pk)
EXPECTED_SCHEMA = [
    (0, "id",         "INTEGER", 0, None, 1),
    (1, "first_name", "TEXT",    0, None, 0),
    (2, "last_name",  "TEXT",    0, None, 0),
    (3, "department", "TEXT",    0, None, 0),
]


@pytest.fixture(scope="module")
def connection():
    """Yield a read-only sqlite3 connection to the legacy database."""
    if not SOURCE_DB.exists():
        pytest.skip(f"Source database {SOURCE_DB} does not exist; "
                    "skipping DB-level tests.")
    # Open the database in read-only mode to guarantee we never modify it.
    conn = sqlite3.connect(f"file:{SOURCE_DB}?mode=ro", uri=True)
    try:
        yield conn
    finally:
        conn.close()


def test_source_db_file_exists_and_is_regular():
    assert SOURCE_DB.exists(), (
        f"Expected source database at {SOURCE_DB}, but it does not exist."
    )
    assert SOURCE_DB.is_file(), (
        f"Expected {SOURCE_DB} to be a regular file."
    )


def test_employees_table_schema(connection):
    cursor = connection.execute("PRAGMA table_info(employees);")
    schema = cursor.fetchall()

    # We only compare the *expected* number of columns and their key details.
    # sqlite3 may return rows in the order they were defined, which we expect.
    assert schema == EXPECTED_SCHEMA, (
        "Schema of table 'employees' is incorrect.\n"
        f"Expected:\n{EXPECTED_SCHEMA}\n"
        f"Found:\n{schema}"
    )


def test_employees_table_contents(connection):
    cursor = connection.execute(
        "SELECT id, first_name, last_name, department "
        "FROM employees ORDER BY id;"
    )
    rows = cursor.fetchall()

    assert len(rows) == 5, (
        "Table 'employees' should contain exactly 5 rows, "
        f"but {len(rows)} row(s) were found."
    )
    assert rows == EXPECTED_ROWS, (
        "Data mismatch in table 'employees'.\n"
        f"Expected rows:\n{EXPECTED_ROWS}\n"
        f"Found rows:\n{rows}"
    )