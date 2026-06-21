# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student performs any action for the “Alice open tickets” task.
#
# What we verify:
#   1.   The help-desk directory exists at /home/user/helpdesk.
#   2.   The SQLite database /home/user/helpdesk/tickets.db exists and is a file.
#   3.   The CSV file that the student is supposed to create
#        (/home/user/helpdesk/alice_open_tickets.csv) must NOT exist yet.
#   4.   The database contains a table `tickets` whose schema includes the
#        required columns: id, title, assignee, status, priority.
#   5.   The table currently holds exactly the expected five rows
#        (see EXPECTED_ROWS below).  This ensures the subsequent query
#        yields deterministic results.

import os
import sqlite3
import stat
import pytest

HELPDESK_DIR = "/home/user/helpdesk"
DB_PATH       = os.path.join(HELPDESK_DIR, "tickets.db")
CSV_PATH      = os.path.join(HELPDESK_DIR, "alice_open_tickets.csv")

EXPECTED_ROWS = [
    (1, "Email not working", "Alice",   "open",   "High"),
    (2, "VPN issue",         "Bob",     "closed", "Medium"),
    (3, "Computer hangs",    "Alice",   "open",   "Low"),
    (4, "Printer offline",   "Charlie", "open",   "Medium"),
    (5, "Password reset",    "Alice",   "closed", "Low"),
]


def test_helpdesk_directory_exists():
    assert os.path.isdir(HELPDESK_DIR), (
        f"Expected directory {HELPDESK_DIR!r} does not exist."
    )


def test_database_file_exists_and_is_regular_file():
    assert os.path.exists(DB_PATH), (
        f"Expected SQLite database file {DB_PATH!r} is missing."
    )
    mode = os.stat(DB_PATH).st_mode
    assert stat.S_ISREG(mode), (
        f"{DB_PATH!r} exists but is not a regular file."
    )


def test_csv_file_does_not_exist_yet():
    assert not os.path.exists(CSV_PATH), (
        f"The CSV file {CSV_PATH!r} should NOT exist before the task is done."
    )


@pytest.fixture(scope="module")
def db_conn():
    """Return a SQLite3 connection to the help-desk database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def test_tickets_table_schema(db_conn):
    """Ensure the `tickets` table exists and has the required columns."""
    cursor = db_conn.execute("PRAGMA table_info(tickets);")
    columns = {row["name"] for row in cursor.fetchall()}
    required = {"id", "title", "assignee", "status", "priority"}
    missing = required - columns
    assert not missing, (
        f"The `tickets` table is missing required columns: {', '.join(sorted(missing))}"
    )


def test_tickets_table_contents(db_conn):
    """Verify that the tickets table holds exactly the expected five rows."""
    cursor = db_conn.execute(
        "SELECT id, title, assignee, status, priority FROM tickets ORDER BY id;"
    )
    rows = cursor.fetchall()
    # Convert sqlite3.Row objects to plain tuples for comparison.
    rows_tuples = [tuple(row) for row in rows]

    # Helpful failure message when things do not match.
    assert rows_tuples == EXPECTED_ROWS, (
        "The contents of the `tickets` table are not as expected.\n"
        f"Expected rows:\n{EXPECTED_ROWS}\n"
        f"Actual rows:\n{rows_tuples}"
    )