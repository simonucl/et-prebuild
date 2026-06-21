# test_initial_state.py
#
# This pytest suite validates the *initial* state of the workstation
# before the student performs any action.  It checks that
#   • the expected SQLite database is present and unmodified,
#   • required directories exist and are writable,
#   • no backup / report files have been created yet,
#   • the database schema and seed data match the specification.
#
# Only the Python stdlib and pytest are used.

import os
import stat
import sqlite3
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "projects", "i18n")
DB_PATH = os.path.join(PROJECT_DIR, "app_translations.db")
BACKUP_DIR = os.path.join(PROJECT_DIR, "backups")
BACKUP_PATH = os.path.join(BACKUP_DIR, "app_translations_20230401.db")
SUMMARY_PATH = os.path.join(PROJECT_DIR, "translation_summary.log")


@pytest.fixture(scope="module")
def db_connection():
    """Yield a read-only connection to the translations database."""
    if not os.path.isfile(DB_PATH):
        pytest.fail(
            f"Expected SQLite file not found at {DB_PATH!r}. "
            "The starting database must be in place."
        )
    # Open in read-only mode to ensure the test does not mutate anything
    uri = f"file:{DB_PATH}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        yield conn
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Filesystem / directory prerequisites
# ---------------------------------------------------------------------------

def test_project_structure():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR!r} is missing. "
        "It should already exist before the task begins."
    )
    assert os.path.isdir(BACKUP_DIR), (
        f"Backup directory {BACKUP_DIR!r} is missing. "
        "Create the directory hierarchy ahead of time."
    )

    # The backup directory must be writable
    mode = os.stat(BACKUP_DIR).st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, (
        f"Backup directory {BACKUP_DIR!r} is not writable by the current user."
    )


def test_no_backup_or_report_files_yet():
    assert not os.path.exists(
        BACKUP_PATH
    ), f"Backup file {BACKUP_PATH!r} already exists — it should be created by the student."
    assert not os.path.exists(
        SUMMARY_PATH
    ), f"Report file {SUMMARY_PATH!r} already exists — it should be generated after the database edits."


# ---------------------------------------------------------------------------
# Database schema and seed data
# ---------------------------------------------------------------------------

def test_translations_table_schema(db_connection):
    cur = db_connection.cursor()
    cur.execute('PRAGMA table_info(translations);')
    cols = {row[1] for row in cur.fetchall()}  # row[1] == column name
    expected = {"id", "language", "key", "value", "updated_at"}
    assert cols == expected, (
        "The translations table must contain exactly the columns:\n"
        f"  {sorted(expected)}\n"
        f"Found instead:\n  {sorted(cols)}"
    )


def test_seed_rows_present(db_connection):
    cur = db_connection.cursor()
    cur.execute('SELECT id, language, "key", value, updated_at '
                'FROM translations ORDER BY id;')
    rows = cur.fetchall()
    expected_rows = [
        (1, "en", "welcome_message",  "Welcome",   "2023-01-10 12:00:00"),
        (2, "fr", "welcome_message",  "Bienvenue", "2023-01-10 12:00:00"),
        (3, "de", "welcome_message",  "Willkommen","2023-01-10 12:00:00"),
        (4, "fr", "help_link",        "Aide",      "2023-01-15 09:00:00"),
        (5, "de", "deprecated_notice","Veraltet",  "2023-01-20 15:00:00"),
    ]

    assert rows == expected_rows, (
        "The seed data inside translations is not as expected.\n"
        f"Expected rows (in order):\n  {expected_rows}\n"
        f"Actual rows:\n  {rows}"
    )