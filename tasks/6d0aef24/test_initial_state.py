# test_initial_state.py
#
# Pytest test-suite that validates the **initial** state of the operating
# system / filesystem before the student performs any action.

import os
import sqlite3
import stat
import pytest

HELPDESK_DB = "/home/user/helpdesk.db"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _connect_db(db_path):
    """Return a sqlite3.Connection object to the given database path."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as exc:
        pytest.fail(f"Unable to connect to SQLite database at {db_path!r}: {exc}")

def _fetch_all_tickets(conn):
    """Return all rows from the tickets table, ordered by id."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, status, assigned_to FROM tickets ORDER BY id;")
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as exc:
        pytest.fail(f"Failed to query 'tickets' table: {exc}")

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_helpdesk_db_exists_and_is_regular_file():
    """Validate that /home/user/helpdesk.db exists and is a regular file."""
    assert os.path.exists(HELPDESK_DB), (
        f"Expected database file {HELPDESK_DB} does not exist."
    )

    mode = os.stat(HELPDESK_DB).st_mode
    assert stat.S_ISREG(mode), (
        f"Path {HELPDESK_DB} exists but is not a regular file."
    )

def test_tickets_table_contents():
    """
    Verify that the 'tickets' table exists and contains exactly the expected
    six rows before the student begins work.
    """
    expected_rows = [
        (1, "open",   "unassigned"),
        (2, "closed", "alice"),
        (3, "open",   "unassigned"),
        (4, "open",   "bob"),
        (5, "closed", "unassigned"),
        (6, "open",   "charlie"),
    ]

    conn = _connect_db(HELPDESK_DB)
    try:
        actual_rows = _fetch_all_tickets(conn)
    finally:
        conn.close()

    assert actual_rows == expected_rows, (
        "The 'tickets' table contents do not match the expected initial state.\n"
        f"Expected rows:\n{expected_rows}\n\nActual rows:\n{actual_rows}"
    )

def test_open_unassigned_count_is_two():
    """
    Confirm that the count of tickets where status='open' AND
    assigned_to='unassigned' is exactly 2 in the initial state.
    """
    conn = _connect_db(HELPDESK_DB)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*) FROM tickets
            WHERE status = 'open' AND assigned_to = 'unassigned';
            """
        )
        (count,) = cur.fetchone()
    finally:
        conn.close()

    assert count == 2, (
        f"Expected exactly 2 open & unassigned tickets, found {count}."
    )