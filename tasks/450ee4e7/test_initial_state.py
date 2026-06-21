# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “incident-responder” exercise **before** the student has
# run any solution commands.
#
# What we assert:
#   • /home/user/ir_case exists and is a directory.
#   • /home/user/ir_case/logs.db exists, is a readable SQLite database, and
#     contains the expected `auth` table with the correct columns and rows.
#   • The DISTINCT usernames whose status == 'FAIL' are exactly the five
#     accounts defined in the truth value.
#   • The output file that the student is supposed to create later
#     (/home/user/ir_case/failed_users.csv) does *not* yet exist.
#
# No third-party packages are used; only stdlib + pytest.

import os
import sqlite3
import pytest
from pathlib import Path
from textwrap import dedent

IR_DIR = Path("/home/user/ir_case")
DB_PATH = IR_DIR / "logs.db"
OUTPUT_CSV = IR_DIR / "failed_users.csv"

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def connect_db(db_path: Path) -> sqlite3.Connection:
    """
    Return a read-only sqlite3 connection to *db_path*.

    The URI trick enforces read-only mode so accidental writes in the test
    suite are impossible.
    """
    uri = f"file:{db_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_ir_directory_exists():
    assert IR_DIR.exists(), (
        f"Required directory {IR_DIR} is missing. "
        "The exercise expects this directory to be pre-created."
    )
    assert IR_DIR.is_dir(), f"{IR_DIR} exists but is not a directory."


def test_logs_db_exists():
    assert DB_PATH.exists(), (
        f"SQLite database {DB_PATH} is missing. "
        "It must be present before the student begins."
    )
    assert DB_PATH.is_file(), f"{DB_PATH} exists but is not a regular file."

    # Try opening the database to prove it is a valid SQLite file.
    try:
        with connect_db(DB_PATH) as conn:
            conn.execute("PRAGMA schema_version;")
    except sqlite3.DatabaseError as exc:
        pytest.fail(
            f"{DB_PATH} exists, but it is not a valid SQLite database "
            f"(sqlite3 raised: {exc})."
        )


def test_auth_table_schema_and_rowcount():
    expected_columns = ["id", "ts", "user", "status"]
    expected_rowcount = 9

    with connect_db(DB_PATH) as conn:
        # Verify table presence.
        cur = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='auth';
            """
        )
        row = cur.fetchone()
        assert row is not None, (
            f"The SQLite database {DB_PATH} does not contain a table "
            "'auth', which is required by the exercise."
        )

        # Verify table schema (column names and order).
        cur = conn.execute("PRAGMA table_info(auth);")
        columns = [r[1] for r in cur.fetchall()]  # r[1] == column name
        assert columns == expected_columns, (
            "The 'auth' table has an unexpected schema.\n"
            f"Expected columns: {expected_columns}\n"
            f"Actual columns  : {columns}"
        )

        # Verify row count.
        cur = conn.execute("SELECT COUNT(*) FROM auth;")
        (rowcount,) = cur.fetchone()
        assert rowcount == expected_rowcount, (
            f"The 'auth' table should contain {expected_rowcount} rows "
            f"per the provided truth data, but it contains {rowcount}."
        )


def test_distinct_failed_users_match_truth():
    """
    Ensure the database contains exactly the DISTINCT user values with
    status == 'FAIL' that the truth data specifies.
    """
    expected_users = ["alice", "bob", "charlie", "eve", "frank"]

    with connect_db(DB_PATH) as conn:
        cur = conn.execute(
            """
            SELECT DISTINCT user
            FROM auth
            WHERE status = 'FAIL'
            ORDER BY user ASC;
            """
        )
        users = [row[0] for row in cur.fetchall()]

    assert users == expected_users, dedent(
        f"""
        The set of DISTINCT users with status='FAIL' does not match the truth
        value.

        Expected (alphabetical):
            {expected_users}
        Actual:
            {users}
        """
    ).strip()


def test_output_csv_not_present_yet():
    """
    Before the student’s solution runs, the CSV must *not* exist.  Its presence
    would indicate that the exercise has already been completed or that the
    workspace is in an unexpected state.
    """
    assert not OUTPUT_CSV.exists(), (
        f"Output file {OUTPUT_CSV} already exists, but it should only be "
        "created by the student's single sqlite3 command."
    )