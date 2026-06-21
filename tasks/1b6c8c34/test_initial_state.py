# test_initial_state.py
#
# This pytest suite validates that the environment is in the correct
# “pre-task” state _before_ the student performs any action.
# The checks ensure:
#   1. The SQLite database /home/user/security_settings.db exists and has the
#      expected table & contents.
#   2. The log file /home/user/operation_done.log is **absent**.
#
# Only stdlib and pytest are used.

import os
import sqlite3
import stat
import pytest

DB_PATH = "/home/user/security_settings.db"
LOG_PATH = "/home/user/operation_done.log"


@pytest.fixture(scope="module")
def db_conn():
    """
    Yields a read-write connection to the SQLite database.

    The connection is closed automatically after the module’s tests run.
    """
    if not os.path.exists(DB_PATH):
        pytest.skip(f"Database file {DB_PATH!r} is missing; remaining DB tests "
                    f"cannot run.")
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def test_db_file_exists_and_is_regular():
    assert os.path.exists(DB_PATH), (
        f"Expected database file at {DB_PATH}, but it does not exist."
    )

    st = os.stat(DB_PATH)
    assert stat.S_ISREG(st.st_mode), (
        f"{DB_PATH} exists but is not a regular file."
    )


def test_system_config_table_exists(db_conn):
    cur = db_conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='system_config';"
    )
    row = cur.fetchone()
    assert row is not None, (
        "Table 'system_config' is missing from the database. "
        "The initial database should contain this table."
    )


def test_system_config_schema_minimal_check(db_conn):
    """
    Verify that the system_config table has at least the expected
    columns 'param' and 'val'. We do not insist on exact SQL types here,
    only on column presence so that the rest of the exercise makes sense.
    """
    cur = db_conn.cursor()
    cur.execute("PRAGMA table_info('system_config');")
    columns = {row[1] for row in cur.fetchall()}  # row[1] == column name
    expected_cols = {"param", "val"}
    missing = expected_cols - columns
    assert not missing, (
        "Table 'system_config' is missing expected columns: "
        f"{', '.join(sorted(missing))}"
    )


def test_initial_row_value_is_yes(db_conn):
    """
    Confirm that, before the task starts, the permit_remote_root parameter
    is set to 'yes' exactly once.
    """
    cur = db_conn.cursor()
    cur.execute(
        "SELECT val FROM system_config WHERE param='permit_remote_root';"
    )
    rows = cur.fetchall()

    assert rows, (
        "Row with param='permit_remote_root' is missing from system_config; "
        "the initial database should contain exactly one such row."
    )
    assert len(rows) == 1, (
        f"Expected exactly 1 row for param='permit_remote_root', "
        f"found {len(rows)} rows."
    )

    val = rows[0][0]
    assert val == "yes", (
        f"Initial value for permit_remote_root should be 'yes' but is {val!r}."
    )


def test_operation_done_log_absent():
    assert not os.path.exists(LOG_PATH), (
        f"Log file {LOG_PATH} should NOT exist before the student runs their "
        "solution, but it is present."
    )