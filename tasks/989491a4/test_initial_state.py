# test_initial_state.py
#
# This test-suite validates that the operating-system / file-system is in the
# correct **initial** state *before* the student performs the migration task.
#
# • The legacy database (/home/user/data/legacy.db) **must** exist and contain
#   exactly the expected table definition and rows.
# • Neither the new database (/home/user/data/hr.db) nor the migration log
#   (/home/user/migration/migration.log) should exist yet.
#
# If any of the following tests fail, the initial set-up is incorrect and the
# student cannot reasonably be expected to succeed.

import os
import sqlite3
import stat
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
MIGRATION_DIR = os.path.join(HOME, "migration")

LEGACY_DB = os.path.join(DATA_DIR, "legacy.db")
NEW_DB = os.path.join(DATA_DIR, "hr.db")
MIGRATION_LOG = os.path.join(MIGRATION_DIR, "migration.log")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def connect_readonly(path):
    """
    Open a SQLite database in read-only mode.  This prevents the test-suite
    from creating a file if the path is wrong and makes accidental writes
    impossible.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Expected database file not found at: {path}")
    uri = f"file:{path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_legacy_db_file_exists_and_is_regular():
    assert os.path.isfile(LEGACY_DB), (
        f"Legacy database not found at expected location: {LEGACY_DB}"
    )
    st_mode = os.stat(LEGACY_DB).st_mode
    assert stat.S_ISREG(st_mode), (
        f"The legacy database exists but is not a regular file: {LEGACY_DB}"
    )


def test_legacy_db_schema_and_rows():
    """
    Validate that the legacy database contains exactly one table named
    'employees' with the expected schema and rows.
    """
    expected_columns = [
        # (cid, name, type, notnull, dflt_value, pk)
        (0, "id", "INTEGER", 0, None, 1),
        (1, "name", "TEXT", 0, None, 0),
        (2, "salary", "INTEGER", 0, None, 0),
    ]
    expected_rows = [
        (1, "Alice", 72000),
        (2, "Bob", 68000),
        (3, "Charlie", 65000),
    ]

    with connect_readonly(LEGACY_DB) as conn:
        cur = conn.cursor()

        # ------------------------------------------------------------------ #
        # 1. Exactly one user table named 'employees'.
        # ------------------------------------------------------------------ #
        cur.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%';
            """
        )
        tables = [row[0] for row in cur.fetchall()]
        assert tables == ["employees"], (
            "Legacy database must contain exactly one user table named "
            f"'employees', but found: {tables}"
        )

        # ------------------------------------------------------------------ #
        # 2. Validate table schema column-by-column.
        # ------------------------------------------------------------------ #
        cur.execute("PRAGMA table_info(employees);")
        columns = cur.fetchall()
        assert columns == expected_columns, (
            "The 'employees' table schema does not match expectation.\n"
            f"Expected: {expected_columns}\n"
            f"Found   : {columns}"
        )

        # ------------------------------------------------------------------ #
        # 3. Validate row data.
        # ------------------------------------------------------------------ #
        cur.execute("SELECT id, name, salary FROM employees ORDER BY id;")
        rows = cur.fetchall()
        assert rows == expected_rows, (
            "The 'employees' table does not contain the expected rows.\n"
            f"Expected: {expected_rows}\n"
            f"Found   : {rows}"
        )


def test_new_db_does_not_yet_exist():
    assert not os.path.exists(NEW_DB), (
        f"The new database {NEW_DB} should NOT exist before migration begins."
    )


def test_migration_log_does_not_yet_exist():
    assert not os.path.exists(MIGRATION_LOG), (
        f"The migration log {MIGRATION_LOG} should NOT exist before migration."
    )