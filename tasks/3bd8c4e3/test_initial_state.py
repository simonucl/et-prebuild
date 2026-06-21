# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem / OS state
# before the student performs any deployment steps for the v1.4.0
# release.  Only the pre-existing resources are tested—nothing that
# the student is expected to create later is inspected here.

import os
import sqlite3
import stat
import textwrap
import pytest
from pathlib import Path

# -----------------------------------------------------------------------------
# Helper utilities
# -----------------------------------------------------------------------------


def assert_is_regular_file(path: Path):
    """Assert that *path* exists and is a regular file."""
    if not path.exists():
        pytest.fail(f"Required file not found: {path}")
    if not path.is_file():
        pytest.fail(f"Path exists but is not a regular file: {path}")


def assert_is_directory(path: Path):
    """Assert that *path* exists and is a directory."""
    if not path.exists():
        pytest.fail(f"Required directory not found: {path}")
    if not path.is_dir():
        pytest.fail(f"Path exists but is not a directory: {path}")


# -----------------------------------------------------------------------------
# Paths used throughout the tests
# -----------------------------------------------------------------------------
HOME = Path("/home/user")
DB_PATH = HOME / "app" / "data" / "app.db"
MIGRATION_SQL_PATH = HOME / "update_scripts" / "02_create_release_info.sql"
LOGS_DIR = HOME / "app" / "logs"


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_app_data_directory_exists():
    """`/home/user/app/data` must exist and be a directory."""
    data_dir = HOME / "app" / "data"
    assert_is_directory(data_dir)


def test_database_exists_and_schema():
    """
    The SQLite3 database must exist, have only the `users` table,
    contain one row (1, 'Alice'), and *not* contain the `release_info` table.
    """
    assert_is_regular_file(DB_PATH)

    # Connect read-only where possible (URI mode prevents accidental changes).
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' ORDER BY name"
        )
        tables = {row[0] for row in cur.fetchall()}
        expected_tables = {"users"}
        unexpected_tables = {"release_info"}

        missing = expected_tables - tables
        extras = tables & unexpected_tables

        if missing:
            pytest.fail(
                f"Database is missing expected table(s): {', '.join(sorted(missing))}"
            )
        if extras:
            pytest.fail(
                f"Database already contains table(s) that should not exist yet: "
                f"{', '.join(sorted(extras))}"
            )

        # Verify content of `users` table.
        cur = conn.execute("SELECT id, name FROM users")
        rows = cur.fetchall()
        assert rows == [(1, "Alice")], (
            "Table `users` should contain exactly one row: (1, 'Alice'), "
            f"but found: {rows}"
        )
    finally:
        conn.close()


def test_migration_sql_script_exact_content():
    """
    The migration SQL script must exist at the exact path and its
    content must match the 4-line block specified in the task description.
    """
    assert_is_regular_file(MIGRATION_SQL_PATH)

    expected_sql = textwrap.dedent(
        """\
        CREATE TABLE release_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            deployed_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    with MIGRATION_SQL_PATH.open("r", encoding="utf-8") as fh:
        actual_sql = fh.read()

    assert (
        actual_sql == expected_sql
    ), "SQL migration script content does not match the expected 4-line block."


def test_logs_directory_and_files():
    """
    The logs directory must exist and contain at least 'access.log' and 'error.log'.
    All entries in this directory must be regular files (not subdirectories).
    """
    assert_is_directory(LOGS_DIR)

    required_logs = {"access.log", "error.log"}
    existing_entries = {p.name for p in LOGS_DIR.iterdir()}
    missing = required_logs - existing_entries
    if missing:
        pytest.fail(
            "Missing expected log file(s) in "
            f"{LOGS_DIR}: {', '.join(sorted(missing))}"
        )

    # Ensure every entry is a regular file
    for p in LOGS_DIR.iterdir():
        if not p.is_file():
            pytest.fail(
                f"Unexpected non-file entry inside logs directory: {p.name}"
            )