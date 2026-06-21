# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem
# BEFORE the student performs any action.  It checks that the
# SQLite database and its contents are exactly in the expected
# initial state.
#
# IMPORTANT:  These tests purposely do NOT look for any output
# artefacts that the student is supposed to create (e.g.
# ticket_summary.log).  They assert only the pre-existing state.

import os
import stat
import sqlite3
import pytest

HOME = "/home/user"
HELPDESK_DIR = os.path.join(HOME, "helpdesk")
DB_PATH = os.path.join(HELPDESK_DIR, "helpdesk.db")

EXPECTED_ROWS = [
    (1, "Cannot connect to VPN", "open"),
    (2, "Email not syncing",     "open"),
    (3, "Forgot password",       "resolved"),
    (4, "Printer jam",           "in_progress"),
]

@pytest.fixture(scope="module")
def db_connection():
    """Provide a module-scoped connection to the SQLite database."""
    if not os.path.isfile(DB_PATH):
        pytest.fail(
            f"Expected database file '{DB_PATH}' to exist, "
            "but it is missing."
        )
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as exc:
        pytest.fail(f"Failed to open SQLite database '{DB_PATH}': {exc}")
    yield conn
    conn.close()


def test_helpdesk_directory_exists_and_permissions():
    """Verify that /home/user/helpdesk exists with 755 permissions."""
    assert os.path.isdir(HELPDESK_DIR), (
        f"Directory '{HELPDESK_DIR}' is missing — "
        "it must exist before the task starts."
    )

    mode = os.stat(HELPDESK_DIR).st_mode & 0o777
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory '{HELPDESK_DIR}' should have permissions "
        f"{oct(expected_mode)}, but found {oct(mode)}."
    )


def test_helpdesk_db_exists_and_is_file():
    """Check that the SQLite database file exists and is a regular file."""
    assert os.path.exists(DB_PATH), (
        f"SQLite database '{DB_PATH}' is missing."
    )
    assert os.path.isfile(DB_PATH), (
        f"Path '{DB_PATH}' exists but is not a regular file."
    )


def test_helpdesk_db_integrity(db_connection):
    """Run PRAGMA integrity_check to confirm the DB is not corrupt."""
    cursor = db_connection.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()
    assert result == ("ok",), (
        f"Database integrity check failed for '{DB_PATH}': {result}"
    )


def test_tickets_table_schema(db_connection):
    """Ensure the 'tickets' table exists with the correct columns."""
    cursor = db_connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='tickets';"
    )
    table = cursor.fetchone()
    assert table is not None, (
        "Table 'tickets' is missing from the helpdesk database."
    )

    cursor = db_connection.execute("PRAGMA table_info('tickets');")
    columns = [(row[1], row[2].upper()) for row in cursor.fetchall()]
    expected_columns = [
        ("id", "INTEGER"),
        ("title", "TEXT"),
        ("status", "TEXT"),
    ]
    assert columns == expected_columns, (
        "Schema mismatch for table 'tickets'.\n"
        f"Expected columns: {expected_columns}\n"
        f"Found columns   : {columns}"
    )

    # Verify that 'id' is the PRIMARY KEY
    cursor = db_connection.execute("PRAGMA table_info('tickets');")
    primary_key_cols = [row[1] for row in cursor.fetchall() if row[5] == 1]
    assert primary_key_cols == ["id"], (
        "Column 'id' should be the PRIMARY KEY of table 'tickets'.\n"
        f"Primary key columns reported by SQLite: {primary_key_cols}"
    )


def test_initial_ticket_rows(db_connection):
    """Check that the tickets table contains the expected 4 rows."""
    cursor = db_connection.execute(
        "SELECT id, title, status FROM tickets ORDER BY id;"
    )
    rows = cursor.fetchall()
    assert rows == EXPECTED_ROWS, (
        "Initial rows in the 'tickets' table do not match the expected "
        "dataset.\n"
        f"Expected: {EXPECTED_ROWS}\n"
        f"Found   : {rows}"
    )