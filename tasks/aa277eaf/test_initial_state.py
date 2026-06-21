# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the migration task is performed.

import os
import sqlite3
import stat
import pytest

HOME = "/home/user"
LEGACY_DIR = os.path.join(HOME, "legacy")
NEW_DIR = os.path.join(HOME, "new")
LEGACY_DB = os.path.join(LEGACY_DIR, "legacy.db")
NEW_DB = os.path.join(NEW_DIR, "new.db")
REPORT_FILE = os.path.join(HOME, "migration_report.txt")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_sqlite_file(path):
    """
    Quick sanity‐check that the file at *path* is a valid SQLite database.
    """
    assert os.path.isfile(path), f"Expected a file at {path}, but it does not exist."
    # The first 16 bytes of a SQLite DB file are: b'SQLite format 3\0'
    with open(path, "rb") as fh:
        header = fh.read(16)
    assert header.startswith(b"SQLite format 3"), (
        f"{path} exists but does not appear to be a valid SQLite database."
    )

def _get_tables(cursor):
    """
    Returns the list of non‐sqlite_internal tables for the connected DB.
    """
    cursor.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name"
    )
    return [row[0] for row in cursor.fetchall()]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_exist_and_permissions():
    """Both legacy and new directories must exist and be accessible."""
    for directory in (LEGACY_DIR, NEW_DIR):
        assert os.path.isdir(directory), f"Directory {directory} should exist."
        mode = os.stat(directory).st_mode
        assert mode & stat.S_IRUSR, f"Directory {directory} must be readable."
        assert mode & stat.S_IWUSR, f"Directory {directory} must be writable."

def test_new_directory_is_empty():
    """
    /home/user/new should be empty before migration (no pre‐existing DB,
    temp files, hidden files, etc.).
    """
    contents = os.listdir(NEW_DIR)
    assert contents == [] , (
        f"{NEW_DIR} is expected to be empty, but contains: {', '.join(contents)}"
    )

def test_legacy_database_file_exists_and_is_valid_sqlite():
    _assert_sqlite_file(LEGACY_DB)

def test_legacy_database_has_expected_table_only():
    with sqlite3.connect(LEGACY_DB) as conn:
        cur = conn.cursor()
        tables = _get_tables(cur)
        assert tables == ["customers_old"], (
            f"Expected exactly one table named 'customers_old' in {LEGACY_DB}, "
            f"found: {tables or 'none'}"
        )

def test_customers_old_schema_is_correct():
    expected_schema = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "name", "TEXT", 0, None, 0),
        (2, "email", "TEXT", 0, None, 0),
    ]
    with sqlite3.connect(LEGACY_DB) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(customers_old);")
        schema = cur.fetchall()
        assert schema == expected_schema, (
            "Schema mismatch for 'customers_old'.\n"
            f"Expected: {expected_schema}\nActual:   {schema}"
        )

def test_customers_old_contains_expected_rows():
    expected_rows = [
        (1, "Alice Smith", "alice@example.com"),
        (2, "Bob Jones", "bob@example.com"),
        (3, "Charlie Brown", "charlie@example.com"),
    ]
    with sqlite3.connect(LEGACY_DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers_old ORDER BY id;")
        rows = cur.fetchall()
        assert rows == expected_rows, (
            "Data mismatch in 'customers_old'.\n"
            f"Expected rows:\n{expected_rows}\nActual rows:\n{rows}"
        )

def test_output_artifacts_do_not_exist_yet():
    """
    The destination database and migration report must *not* exist before
    the migration command is executed.
    """
    assert not os.path.exists(NEW_DB), (
        f"{NEW_DB} should not exist before migration starts."
    )
    assert not os.path.exists(REPORT_FILE), (
        f"{REPORT_FILE} should not exist before migration starts."
    )