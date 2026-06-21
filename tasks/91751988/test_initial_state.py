# test_initial_state.py
#
# Pytest suite that validates the *pre-existing* operating-system / filesystem
# state expected **before** the student carries out any action.
#
# It asserts that:
#   • The /home/user/doc_management directory already exists.
#   • The SQLite database /home/user/doc_management/doc_index.db exists.
#   • The database contains exactly one table named `documents` whose schema is
#       (doc_id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL).
#   • The table currently holds exactly the three required rows.
#
# No checks are made for any output artefacts that the student is supposed to
# create later (e.g. documents_export.csv).

import os
import stat
import sqlite3
import pytest


DOC_DIR = "/home/user/doc_management"
DB_PATH = os.path.join(DOC_DIR, "doc_index.db")

EXPECTED_SCHEMA = [
    ("doc_id", "INTEGER", 1),     # (column_name, declared_type, pk_flag)
    ("title", "TEXT", 0),
    ("category", "TEXT", 0),
]

EXPECTED_ROWS = [
    (1, "Getting_Started", "Guide"),
    (2, "API_Reference",   "Reference"),
    (3, "Release_Notes",   "Changelog"),
]


def test_directory_exists_and_permissions():
    """
    The working directory must already exist and be accessible.
    """
    assert os.path.isdir(DOC_DIR), (
        f"Required directory {DOC_DIR} is missing. "
        "Create it before attempting the task."
    )

    dir_mode = stat.S_IMODE(os.stat(DOC_DIR).st_mode)
    # Expect at least 0o755 (rwxr-xr-x); looser perms are acceptable
    assert dir_mode & 0o700 == 0o700, (
        f"Directory {DOC_DIR} exists but lacks owner rwx permissions "
        f"(mode is {oct(dir_mode)})."
    )


def test_database_file_exists():
    """
    The SQLite database file must be present.
    """
    assert os.path.isfile(DB_PATH), (
        f"SQLite database {DB_PATH} is missing. "
        "It must be provided before running the export command."
    )


@pytest.fixture(scope="module")
def db_connection():
    """
    Provide a read-only connection to the existing SQLite database.
    """
    # SQLite URI with mode=ro prevents accidental modifications.
    uri = f"file:{DB_PATH}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    yield conn
    conn.close()


def test_single_documents_table_present(db_connection):
    """
    Verify that exactly one table named `documents` exists.
    """
    cur = db_connection.cursor()
    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """)
    tables = [row[0] for row in cur.fetchall()]

    assert tables == ["documents"], (
        "Database should contain exactly one table named 'documents'. "
        f"Found: {tables or 'none'}."
    )


def test_documents_table_schema(db_connection):
    """
    Confirm the `documents` table schema matches the specification.
    """
    cur = db_connection.cursor()
    cur.execute("PRAGMA table_info(documents);")
    pragma_info = cur.fetchall()  # (cid, name, type, notnull, dflt_value, pk)

    # Build simplified representation: (name, type, pk_flag)
    observed_schema = [(row[1], row[2].upper(), row[5]) for row in pragma_info]

    assert observed_schema == EXPECTED_SCHEMA, (
        "Schema of 'documents' table does not match the required layout.\n"
        f"Expected: {EXPECTED_SCHEMA}\n"
        f"Found   : {observed_schema}"
    )


def test_documents_table_rows(db_connection):
    """
    The table must already contain exactly the three prescribed rows.
    """
    cur = db_connection.cursor()
    cur.execute("SELECT doc_id, title, category FROM documents ORDER BY doc_id;")
    rows = cur.fetchall()

    assert rows == EXPECTED_ROWS, (
        "Content of 'documents' table is incorrect.\n"
        f"Expected rows:\n{EXPECTED_ROWS}\n"
        f"Found rows   :\n{rows}"
    )