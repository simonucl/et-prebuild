# test_initial_state.py
#
# This pytest suite validates the *initial* operating–system / filesystem
# conditions expected **before** the student runs any migration command.
#
# Truth assumptions (must already hold when these tests run):
#   • /home/user/source_sales.db          : must exist & be a valid SQLite-3 DB
#   • /home/user/target_sales.db          : must NOT exist
#   • /home/user/migration_validation.log : must NOT exist
#
# The existing database must contain exactly one table named `sales`
# and that table must have exactly 5 rows.

import os
import sqlite3
import stat
import pytest

SRC_DB = "/home/user/source_sales.db"
TGT_DB = "/home/user/target_sales.db"
LOG_FILE = "/home/user/migration_validation.log"


def _db_connect(path):
    """
    Helper: connect to an SQLite DB in read-only mode to avoid mutations.
    """
    # The URI mode flags ensure read-only. Works on modern SQLite (3.7+).
    uri = f"file:{path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def test_source_db_file_exists_and_is_regular():
    """Verify that the source DB file exists and is a regular file."""
    assert os.path.exists(SRC_DB), (
        f"Expected source DB at {SRC_DB!r} but it is missing."
    )
    st = os.stat(SRC_DB)
    assert stat.S_ISREG(st.st_mode), (
        f"Expected {SRC_DB!r} to be a regular file, but it is not."
    )


def test_source_db_has_sales_table_with_five_rows():
    """
    Validate that `source_sales.db` is a readable SQLite DB
    containing table `sales` with exactly 5 rows.
    """
    try:
        with _db_connect(SRC_DB) as conn:
            cur = conn.cursor()

            # Check that the table `sales` exists.
            cur.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='sales';"
            )
            row = cur.fetchone()
            assert row is not None, (
                "Table 'sales' is missing from source DB."
            )

            # Count the rows.
            cur.execute("SELECT COUNT(*) FROM sales;")
            (count,) = cur.fetchone()
            assert count == 5, (
                f"Table 'sales' is expected to have 5 rows, found {count}."
            )
    except sqlite3.Error as exc:
        pytest.fail(f"Failed to open or query {SRC_DB!r}: {exc}")


def test_target_db_does_not_exist_initially():
    """
    The target DB must **not** exist before the migration command is run.
    """
    assert not os.path.exists(TGT_DB), (
        f"Target DB {TGT_DB!r} already exists; it should be created "
        "by the student's command."
    )


def test_log_file_does_not_exist_initially():
    """
    The migration validation log must **not** exist before the command.
    """
    assert not os.path.exists(LOG_FILE), (
        f"Log file {LOG_FILE!r} already exists; it should be generated "
        "by the student's command."
    )