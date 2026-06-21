# test_initial_state.py
#
# Pytest suite that validates the _initial_ operating-system / filesystem
# state before the student performs any action.

import os
import stat
import sqlite3
import pytest

# --------------------------------------------------------------------------- #
# Paths that must already exist                                               #
# --------------------------------------------------------------------------- #
DB_DIR = "/home/user/projects/loc/db"
REPORT_DIR = "/home/user/projects/loc/report"
DB_PATH = os.path.join(DB_DIR, "translations.db")


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _mode(path):
    """Return the permission bits (e.g. 0o700)."""
    return stat.S_IMODE(os.stat(path).st_mode)


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_required_directories_exist_with_correct_permissions():
    # Directory: /home/user/projects/loc/db
    assert os.path.isdir(DB_DIR), (
        f"Required directory {DB_DIR} is missing."
    )
    assert _mode(DB_DIR) == 0o700, (
        f"Directory {DB_DIR} must have permissions 0700; "
        f"found {_mode(DB_DIR):04o}."
    )

    # Directory: /home/user/projects/loc/report
    assert os.path.isdir(REPORT_DIR), (
        f"Required directory {REPORT_DIR} is missing."
    )
    assert _mode(REPORT_DIR) == 0o700, (
        f"Directory {REPORT_DIR} must have permissions 0700; "
        f"found {_mode(REPORT_DIR):04o}."
    )


def test_database_file_exists_and_is_accessible():
    assert os.path.isfile(DB_PATH), (
        f"SQLite database not found at {DB_PATH}."
    )

    # Try to connect & perform a trivial query; this will raise on corruption.
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as exc:
        pytest.fail(f"Unable to open SQLite database: {exc}")

    with conn:
        cur = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='strings';"
        )
        row = cur.fetchone()
        assert row is not None, (
            "Table 'strings' is missing from the database."
        )


def test_strings_table_initial_contents_are_correct():
    """Validate that the table holds exactly the two expected rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = list(
        conn.execute(
            "SELECT id, key, en, es FROM strings ORDER BY id;"
        )
    )

    # Exactly two rows must be present.
    assert len(rows) == 2, (
        "Table 'strings' should contain exactly 2 rows in the initial state."
    )

    # Row 1 assertions
    r1 = rows[0]
    assert (r1["id"], r1["key"], r1["en"]) == (
        1,
        "hello_msg",
        "Hello!",
    ), (
        "First row (id=1) does not match expected values "
        "(id=1, key='hello_msg', en='Hello!')."
    )
    assert r1["es"] == "¡Hola!", (
        "Spanish text for key 'hello_msg' should be '¡Hola!' in the initial state."
    )

    # Row 2 assertions
    r2 = rows[1]
    assert (r2["id"], r2["key"], r2["en"]) == (
        2,
        "goodbye_msg",
        "Goodbye!",
    ), (
        "Second row (id=2) does not match expected values "
        "(id=2, key='goodbye_msg', en='Goodbye!')."
    )
    assert r2["es"] is None, (
        "Spanish text for key 'goodbye_msg' is expected to be NULL in the initial state."
    )

    # There must *not* yet be any row for the key 'reset_password'.
    cur = conn.execute(
        "SELECT 1 FROM strings WHERE key = 'reset_password';"
    )
    assert cur.fetchone() is None, (
        "Key 'reset_password' must NOT exist in the initial database state."
    )