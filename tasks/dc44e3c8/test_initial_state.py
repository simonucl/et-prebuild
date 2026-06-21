# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student performs the migration task.
#
# It asserts that:
# 1. The legacy database (/home/user/observability.db) exists and is valid.
# 2. The legacy database contains exactly one table named `metrics`
#    whose schema is (id INTEGER PRIMARY KEY, name TEXT, value REAL).
# 3. The `metrics` table holds exactly three rows.
# 4. Neither the destination database
#    (/home/user/observability_v2.db) nor the validation log
#    (/home/user/migration_validation.log) exist yet.
#
# If any check fails, the test output will clearly explain what is
# missing or incorrect.
#
# Only the Python standard library and pytest are used.

import os
import sqlite3
import pytest

HOME_DIR = "/home/user"
LEGACY_DB = os.path.join(HOME_DIR, "observability.db")
DEST_DB = os.path.join(HOME_DIR, "observability_v2.db")
VALIDATION_LOG = os.path.join(HOME_DIR, "migration_validation.log")


def _connect_sqlite(path):
    """Return a read-only SQLite connection to *path* or fail with a
    descriptive pytest message if that is not possible."""
    if not os.path.exists(path):
        pytest.fail(f"Expected SQLite database at {path} does NOT exist.")
    try:
        # Open the database in read-only mode to ensure the initial state
        # remains untouched.
        uri = f"file:{path}?mode=ro"
        return sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        pytest.fail(f"Could NOT open {path} as a valid SQLite database: {exc}")


def test_legacy_db_exists_and_is_sqlite():
    """The legacy DB file must exist and be a valid SQLite database."""
    conn = _connect_sqlite(LEGACY_DB)
    conn.close()


def test_destination_db_does_not_exist_yet():
    """The new DB should not exist before the migration."""
    assert not os.path.exists(
        DEST_DB
    ), f"Destination DB {DEST_DB} already exists; it should be created by the migration step, not before."


def test_validation_log_does_not_exist_yet():
    """The validation log should not exist before the migration."""
    assert not os.path.exists(
        VALIDATION_LOG
    ), f"Validation log {VALIDATION_LOG} already exists; it should be produced after the migration, not before."


def test_legacy_db_schema_and_rowcount():
    """
    The legacy DB must contain exactly one table (`metrics`) with the
    expected schema and three rows.
    """
    conn = _connect_sqlite(LEGACY_DB)
    cur = conn.cursor()

    # 1. Ensure ONLY ONE user table exists.
    cur.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """
    )
    tables = [row[0] for row in cur.fetchall()]
    assert tables == [
        "metrics"
    ], f"Legacy DB should contain exactly one table named 'metrics'; found: {tables}"

    # 2. Verify schema via PRAGMA table_info.
    cur.execute("PRAGMA table_info(metrics);")
    columns = cur.fetchall()
    # columns: (cid, name, type, notnull, dflt_value, pk)
    expected_colspec = [
        ("id", "INTEGER", 1),   # pk == 1
        ("name", "TEXT", 0),
        ("value", "REAL", 0),
    ]
    if len(columns) != 3:
        pytest.fail(f"'metrics' table should have exactly 3 columns; found {len(columns)}")
    for col, expected in zip(columns, expected_colspec):
        name_expected, type_expected, pk_expected = expected
        _, name, coltype, _, _, pk = col
        assert name == name_expected, f"Expected column '{name_expected}', found '{name}'"
        # SQLite is case-insensitive for types; compare uppercase.
        assert coltype.upper() == type_expected, (
            f"Column '{name}' should be of type {type_expected}, "
            f"found {coltype}"
        )
        assert pk == pk_expected, (
            f"Column '{name}' should have pk={pk_expected}, "
            f"found pk={pk}"
        )

    # 3. Verify row count equals 3.
    cur.execute("SELECT COUNT(*) FROM metrics;")
    count = cur.fetchone()[0]
    assert (
        count == 3
    ), f"'metrics' table should have exactly 3 rows; found {count}"

    conn.close()