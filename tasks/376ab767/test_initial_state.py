# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem and database state
before the student performs any migration work.

This file must remain unchanged by the student; it is executed first to
assert that the starting conditions match the specification.
"""

from pathlib import Path
import sqlite3
import pytest

# ---------------------------------------------------------------------------
# Constant paths used throughout the tests
# ---------------------------------------------------------------------------
LEGACY_DIR = Path("/home/user/legacy_app")
DATA_DIR = LEGACY_DIR / "data"
OLD_DB_PATH = DATA_DIR / "old_users.db"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _open_sqlite_readonly(db_path: Path):
    """
    Opens an SQLite database in read-only mode to prevent accidental mutation.
    """
    if not db_path.exists():
        pytest.fail(f"Expected database file {db_path} is missing.")
    # Use URI mode=ro to avoid write access.
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_legacy_directory_structure_exists():
    """
    Verify the legacy directory tree and database file exist with correct types.
    """
    assert LEGACY_DIR.is_dir(), f"Directory {LEGACY_DIR} is missing."
    assert DATA_DIR.is_dir(), f"Directory {DATA_DIR} is missing."
    assert OLD_DB_PATH.is_file(), f"Database file {OLD_DB_PATH} is missing."


def test_legacy_database_schema_and_contents():
    """
    Ensure the old_users.db database has the expected schema and data
    *before* any migration is attempted.
    """
    expected_columns = [
        ("id", "INTEGER"),
        ("username", "TEXT"),
        ("email", "TEXT"),
    ]

    expected_rows = [
        (1, "alice", "alice@example.com"),
        (2, "bob", "bob@example.com"),
        (3, "carol", "carol@example.com"),
        (4, "dave", "dave@example.com"),
        (5, "eve", "eve@example.com"),
    ]

    with _open_sqlite_readonly(OLD_DB_PATH) as conn:
        cur = conn.cursor()

        # ------------------------------------------------------------------
        # Validate table existence and column definitions
        # ------------------------------------------------------------------
        cur.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='users';
            """
        )
        table_exists = cur.fetchone()
        assert table_exists, "Table 'users' is missing from old_users.db."

        # Fetch column info: cid | name | type | notnull | dflt | pk
        cur.execute("PRAGMA table_info(users);")
        columns = cur.fetchall()

        # Compare column names and types only.
        obtained_columns = [(col[1], col[2]) for col in columns]
        assert (
            obtained_columns == expected_columns
        ), (
            "Schema mismatch in 'users' table.\n"
            f"Expected columns: {expected_columns}\n"
            f"Found columns:    {obtained_columns}"
        )

        # Confirm that the schema has NOT yet been hardened
        # (i.e., no 'last_login' column and no 'idx_users_email' index).
        assert all(
            name != "last_login" for name, _ in obtained_columns
        ), "Column 'last_login' should NOT exist in the initial state."

        cur.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='index' AND name='idx_users_email';
            """
        )
        idx_present = cur.fetchone()
        assert idx_present is None, (
            "Index 'idx_users_email' should NOT exist in the initial state."
        )

        # ------------------------------------------------------------------
        # Validate row count and contents
        # ------------------------------------------------------------------
        cur.execute("SELECT * FROM users ORDER BY id;")
        rows = cur.fetchall()

        assert (
            len(rows) == 5
        ), f"Expected 5 rows in 'users'; found {len(rows)}."

        assert (
            rows == expected_rows
        ), (
            "Row contents in 'users' do not match the expected initial data.\n"
            f"Expected rows:\n{expected_rows}\nFound rows:\n{rows}"
        )