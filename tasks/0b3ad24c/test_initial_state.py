# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem and database
# state before the student starts solving the exercise.  These tests
# purposefully assert ONLY the pre-conditions that the assignment
# describes.  If any of them fail, the environment is not in the
# expected clean starting point.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

MONITORING_DIR = Path("/home/user/monitoring")
DB_PATH = MONITORING_DIR / "uptime.db"
REPORT_PATH = MONITORING_DIR / "uptime_report_20230515.log"


@pytest.fixture(scope="module")
def db_conn():
    """
    Open the SQLite database in read-only mode so we never mutate it.
    """
    # The URI with mode=ro forces an error rather than silently creating
    # a brand-new empty database if the file is missing.
    uri = f"file:{DB_PATH.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    yield conn
    conn.close()


def test_monitoring_directory_exists_and_permissions():
    assert MONITORING_DIR.exists(), (
        f"Required directory {MONITORING_DIR} is missing. "
        "The assignment expects it to be present."
    )
    assert MONITORING_DIR.is_dir(), (
        f"{MONITORING_DIR} exists but is not a directory."
    )

    # Directory should have at most 0755 permissions (world-readable).
    mode = MONITORING_DIR.stat().st_mode
    perms = stat.S_IMODE(mode)
    assert perms & 0o777 == 0o755, (
        f"{MONITORING_DIR} permissions are {oct(perms)}, expected 0o755."
    )


def test_database_file_exists_and_is_regular_file():
    assert DB_PATH.exists(), (
        f"SQLite database {DB_PATH} is missing. "
        "It must exist before any further work begins."
    )
    assert DB_PATH.is_file(), (
        f"{DB_PATH} exists but is not a regular file."
    )


def test_services_table_initial_contents(db_conn):
    cur = db_conn.cursor()
    # Verify that the table itself exists and has the expected columns.
    cur.execute("PRAGMA table_info(services);")
    cols = [row[1] for row in cur.fetchall()]
    expected_cols = {"service_id", "service_name"}
    assert expected_cols.issubset(set(cols)), (
        "Table 'services' is missing required columns "
        f"{expected_cols}. Present columns: {cols}"
    )

    # Verify exactly two starting rows with the correct names.
    cur.execute("SELECT service_name FROM services;")
    rows = {r[0] for r in cur.fetchall()}
    expected = {"frontend", "backend"}
    assert rows == expected, (
        "The initial 'services' table must contain exactly the two rows "
        f"{sorted(expected)}, but it currently contains {sorted(rows)}."
    )


def test_service_checks_table_initial_contents(db_conn):
    cur = db_conn.cursor()
    # Ensure the table and columns exist.
    cur.execute("PRAGMA table_info(service_checks);")
    cols = [row[1] for row in cur.fetchall()]
    expected_cols = {"id", "service_name", "status", "timestamp"}
    assert expected_cols.issubset(set(cols)), (
        "Table 'service_checks' is missing required columns "
        f"{expected_cols}. Present columns: {cols}"
    )

    # Expected six historic rows.
    expected_rows = {
        ("frontend", "up",   "2023-05-15T09:30:00Z"),
        ("backend",  "up",   "2023-05-15T09:30:00Z"),
        ("frontend", "up",   "2023-05-15T09:45:00Z"),
        ("backend",  "up",   "2023-05-15T09:45:00Z"),
        ("frontend", "down", "2023-05-15T09:55:00Z"),
        ("backend",  "up",   "2023-05-15T09:55:00Z"),
    }

    cur.execute(
        "SELECT service_name, status, timestamp FROM service_checks;"
    )
    actual_rows = set(cur.fetchall())

    assert actual_rows == expected_rows, (
        "The initial 'service_checks' table must contain exactly the six "
        "historical rows defined in the task statement.  Differences:\n"
        f"  Missing rows: {sorted(expected_rows - actual_rows)}\n"
        f"  Extra rows  : {sorted(actual_rows - expected_rows)}"
    )


def test_report_file_does_not_exist_yet():
    assert not REPORT_PATH.exists(), (
        f"The report file {REPORT_PATH} should NOT exist in the initial "
        "state; it must be created by the student solution."
    )