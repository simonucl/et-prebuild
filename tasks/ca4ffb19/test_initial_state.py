# test_initial_state.py
#
# Pytest suite that verifies the required initial state of the
# localisation project **before** the student performs any actions.
#
# NOTE: These tests purposefully avoid checking for any artefacts that
# will be produced by the student (back-up, CSV export, logs, …).
# They only assert that the pre-existing data and directory structure
# are in place.

import os
import sqlite3
import pytest

PROJECT_ROOT = "/home/user/projects/loc"
DB_DIR = os.path.join(PROJECT_ROOT, "db")
DB_PATH = os.path.join(DB_DIR, "translations.db")


@pytest.fixture(scope="session")
def db_connection():
    """Yield a read-only connection to the SQLite database."""
    if not os.path.isfile(DB_PATH):
        pytest.skip(f"Database file {DB_PATH!r} not found; cannot run DB tests.")
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        yield con
    finally:
        con.close()


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_ROOT), (
        f"Expected project directory {PROJECT_ROOT!r} to exist."
    )
    assert os.path.isdir(DB_DIR), (
        f"Expected database directory {DB_DIR!r} to exist inside project directory."
    )


def test_database_file_exists_and_is_file():
    assert os.path.isfile(DB_PATH), (
        f"Expected database file {DB_PATH!r} to exist."
    )
    assert os.access(DB_PATH, os.R_OK), (
        f"Database file {DB_PATH!r} is not readable."
    )


def test_translations_table_initial_contents(db_connection):
    """
    Verify the `translations` table starts with exactly the four rows
    described in the task (English and Spanish only, no French yet).
    """
    cur = db_connection.cursor()

    # Ensure the table itself exists with the expected columns.
    cur.execute(
        """
        PRAGMA table_info(translations);
        """
    )
    columns = [row[1] for row in cur.fetchall()]
    expected_columns = ["id", "locale", "key", "value", "updated_at"]
    assert columns == expected_columns, (
        "Schema mismatch for 'translations' table. "
        f"Expected columns {expected_columns}, found {columns}."
    )

    # Fetch all rows ordered by id for deterministic comparison.
    cur.execute(
        """
        SELECT id, locale, key, value, updated_at
        FROM translations
        ORDER BY id;
        """
    )
    rows = cur.fetchall()

    expected_rows = [
        (1, "en", "welcome", "Welcome", "2023-01-01"),
        (2, "en", "logout", "Logout", "2023-01-01"),
        (3, "es", "welcome", "Bienvenido", "2023-01-01"),
        (4, "es", "logout", "Cerrar sesión", "2023-01-01"),
    ]

    assert rows == expected_rows, (
        "Initial contents of 'translations' table do not match the specification.\n"
        f"Expected rows:\n{expected_rows}\nFound rows:\n{rows}"
    )

    # Additional guard: there must be no French rows yet.
    french_rows = [r for r in rows if r[1] == "fr"]
    assert not french_rows, (
        "Detected unexpected French ('fr') rows in the initial database state."
    )