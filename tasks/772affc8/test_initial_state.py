# test_initial_state.py
#
# This pytest suite validates that the filesystem and the SQLite database
# are in the expected **initial** state *before* the student performs any
# modifications.  If any one of these tests fails, the starting point is
# wrong and the assignment cannot be graded reliably.

import os
import sqlite3
from pathlib import Path

import pytest

DB_PATH = Path("/home/user/project/i18n/strings.db")
LOG_PATH = Path("/home/user/project/update_log.txt")
I18N_DIR = Path("/home/user/project/i18n")


def test_i18n_directory_exists():
    """The /home/user/project/i18n directory must already exist."""
    assert I18N_DIR.exists(), f"Expected directory {I18N_DIR} is missing."
    assert I18N_DIR.is_dir(), f"{I18N_DIR} exists but is not a directory."


def test_strings_db_exists():
    """The strings.db file must exist before any changes are made."""
    assert DB_PATH.exists(), f"Expected SQLite database {DB_PATH} is missing."
    assert DB_PATH.is_file(), f"{DB_PATH} exists but is not a regular file."


def _connect_db():
    """Helper that opens the SQLite database in read-only mode."""
    # Using URI mode with immutable option ensures we will not mutate the DB.
    uri = f"file:{DB_PATH}?mode=ro&immutable=1"
    try:
        return sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Could not open the database at {DB_PATH}: {exc}")


def test_database_schema_and_initial_rows():
    """Verify the schema and the initial English rows in the translations table."""
    with _connect_db() as conn:
        cur = conn.cursor()

        # The table 'translations' must exist
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='translations';"
        )
        table = cur.fetchone()
        assert table, "Table 'translations' is missing from the database."

        # Verify the column definitions
        cur.execute("PRAGMA table_info(translations);")
        columns = cur.fetchall()
        expected_columns = [
            ("id", "INTEGER"),
            ("lang", "TEXT"),
            ("key", "TEXT"),
            ("value", "TEXT"),
        ]
        got_columns = [(col[1], col[2]) for col in columns]  # (name, declared_type)
        assert (
            got_columns == expected_columns
        ), f"Schema mismatch in 'translations' table.\nExpected: {expected_columns}\nFound:    {got_columns}"

        # Verify that only the two expected rows are present
        cur.execute("SELECT * FROM translations ORDER BY id;")
        rows = cur.fetchall()
        expected_rows = [
            (1, "en", "greeting", "Hello"),
            (2, "en", "farewell", "Bye"),
        ]
        assert (
            rows == expected_rows
        ), f"Initial rows in 'translations' table are incorrect.\nExpected: {expected_rows}\nFound:    {rows}"

        # Extra sanity checks
        cur.execute("SELECT COUNT(*) FROM translations WHERE lang='es';")
        es_count = cur.fetchone()[0]
        assert (
            es_count == 0
        ), f"Spanish translations already exist (found {es_count} rows); they should be added by the student."


def test_update_log_does_not_exist_yet():
    """The update_log.txt file must not exist before the student's script runs."""
    assert not LOG_PATH.exists(), (
        f"{LOG_PATH} already exists, but it should be created "
        "only after the database update is performed."
    )