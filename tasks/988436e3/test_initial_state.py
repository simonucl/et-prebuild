# test_initial_state.py
#
# This pytest suite verifies that the workspace is in a **clean initial state**
# before the student carries out any of the requested actions.
#
# Nothing related to the assignment should exist yet.  If any of the checked
# paths or database artefacts are already present, the test will fail with a
# clear, actionable message so the student knows the environment needs to be
# reset.

import os
import sqlite3
import stat
import pytest

HOME = "/home/user"
REPORTS_DIR = os.path.join(HOME, "storage_reports")
DB_FILE = os.path.join(REPORTS_DIR, "disk_space.db")
LOG_FILE = os.path.join(REPORTS_DIR, "critical_space.log")


def _pretty_mode(path):
    """Return a human-readable file-mode string (e.g. '0o755') for error msgs."""
    try:
        return oct(os.stat(path, follow_symlinks=False).st_mode & 0o777)
    except FileNotFoundError:
        return "<not found>"


@pytest.mark.order(1)
def test_reports_directory_absent():
    """
    The directory /home/user/storage_reports must NOT exist yet.
    """
    assert not os.path.exists(REPORTS_DIR), (
        f"Precondition failed: {REPORTS_DIR!r} already exists "
        f"(mode={_pretty_mode(REPORTS_DIR)}). "
        "Start with a clean workspace before running your solution."
    )


@pytest.mark.order(2)
def test_database_file_absent():
    """
    The SQLite database file must NOT exist before the student creates it.
    """
    assert not os.path.exists(DB_FILE), (
        f"Precondition failed: Database file {DB_FILE!r} already exists "
        f"(mode={_pretty_mode(DB_FILE)}). "
        "Remove it before proceeding so tests can confirm creation logic."
    )


@pytest.mark.order(3)
def test_log_file_absent():
    """
    The critical_space.log report must NOT exist yet.
    """
    assert not os.path.exists(LOG_FILE), (
        f"Precondition failed: Report file {LOG_FILE!r} already exists "
        f"(mode={_pretty_mode(LOG_FILE)}). "
        "The report should be generated only after the database is ready."
    )


@pytest.mark.order(4)
def test_no_leftover_volumes_table():
    """
    Even if a dangling database file was left behind, ensure it does NOT
    already contain the required 'volumes' table with populated rows.
    This guards against situations where only the directory was cleaned.
    """
    if not os.path.exists(DB_FILE):
        pytest.skip("Database file does not exist yet ― good.")
    # A stale database file exists; inspect its contents.
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT count(*) FROM sqlite_master "
            "WHERE type='table' AND name='volumes';"
        )
        table_count = cur.fetchone()[0]

    assert table_count == 0, (
        f"Precondition failed: {DB_FILE!r} already contains a 'volumes' table. "
        "Start from a clean slate so your script creates the table itself."
    )