# test_initial_state.py
#
# Pytest suite that validates the original operating-system / filesystem
# state *before* the student carries out the “failed-login report” task.
#
# It intentionally checks only the pre-existing artefacts and *absence* of
# the files the student is expected to create, so that any deviation from
# the prescribed starting point is reported early and clearly.
#
# The tests rely exclusively on the Python standard library and pytest.

import os
import sqlite3
import stat
import pytest

HOME = "/home/user"
AUDIT_DIR = os.path.join(HOME, "audit")
REPORTS_DIR = os.path.join(AUDIT_DIR, "reports")
LOGS_DIR = os.path.join(AUDIT_DIR, "logs")
DB_PATH = os.path.join(AUDIT_DIR, "auth.db")
CSV_PATH = os.path.join(REPORTS_DIR, "failed_login_report_20230501.csv")
LOG_PATH = os.path.join(LOGS_DIR, "audit_task.log")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _is_regular_file(path: str) -> bool:
    """Return True if 'path' exists and is a regular file (not dir, symlink, etc.)."""
    try:
        return stat.S_ISREG(os.lstat(path).st_mode)
    except FileNotFoundError:
        return False


def _is_directory(path: str) -> bool:
    """Return True if 'path' exists and is a directory (not symlink, etc.)."""
    try:
        return stat.S_ISDIR(os.lstat(path).st_mode)
    except FileNotFoundError:
        return False


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """
    Ensure the audit base directory and its two sub-directories exist.
    """
    for path in (AUDIT_DIR, REPORTS_DIR, LOGS_DIR):
        assert _is_directory(path), f"Required directory missing: {path}"


def test_database_file_exists_and_is_regular():
    """
    The SQLite database file must already be present and be a regular file.
    """
    assert _is_regular_file(DB_PATH), f"SQLite database not found at expected location: {DB_PATH}"


@pytest.fixture(scope="module")
def conn():
    """
    Yields a read-only SQLite connection to the auth.db database.
    """
    if not _is_regular_file(DB_PATH):
        pytest.skip("Database file is missing; skipping DB-related tests.")
    # Open the DB in read-only mode to guarantee we do not mutate it.
    uri = f"file:{DB_PATH}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    try:
        yield connection
    finally:
        connection.close()


def test_logins_table_schema(conn):
    """
    Validate that the 'logins' table exists with the expected four columns
    (id, username, success, ts) and data types.
    """
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(logins);")
    rows = cur.fetchall()

    # Expected schema mapping: {name: type}
    expected_schema = {
        "id": "INTEGER",
        "username": "TEXT",
        "success": "INTEGER",
        "ts": "TEXT",
    }

    # Convert PRAGMA results into {name: type} dict
    pragma_schema = {row[1]: row[2].upper() for row in rows}

    missing_cols = expected_schema.keys() - pragma_schema.keys()
    extra_cols = pragma_schema.keys() - expected_schema.keys()

    assert not missing_cols, (
        "The 'logins' table is missing expected columns: "
        + ", ".join(sorted(missing_cols))
    )
    assert not extra_cols, (
        "The 'logins' table has unexpected extra columns: "
        + ", ".join(sorted(extra_cols))
    )

    # Check data types match (case-insensitive)
    mismatched_types = [
        f"{col} (expected {expected_schema[col]}, found {pragma_schema[col]})"
        for col in expected_schema
        if pragma_schema.get(col) != expected_schema[col]
    ]
    assert not mismatched_types, (
        "Column type mismatches detected in 'logins' table: "
        + "; ".join(mismatched_types)
    )


def test_prepopulated_rows(conn):
    """
    Confirm that the pre-populated rows match the specification exactly.
    The database should contain eight rows with the precise (id, username,
    success, ts) tuples described in the task.
    """
    cur = conn.cursor()
    cur.execute("SELECT id, username, success, ts FROM logins ORDER BY id;")
    rows = cur.fetchall()

    expected_rows = [
        (1, "alice", 1, "2023-05-01 10:00"),
        (2, "bob",   0, "2023-05-01 10:05"),
        (3, "alice", 0, "2023-05-01 10:06"),
        (4, "carol", 0, "2023-05-01 10:07"),
        (5, "bob",   0, "2023-05-01 10:08"),
        (6, "alice", 0, "2023-05-01 10:09"),
        (7, "dave",  1, "2023-05-01 10:10"),
        (8, "carol", 1, "2023-05-01 10:11"),
    ]

    assert rows == expected_rows, (
        "Contents of 'logins' table do not match the expected pre-populated "
        "rows.\n\nExpected:\n"
        + "\n".join(map(str, expected_rows))
        + "\n\nFound:\n"
        + "\n".join(map(str, rows))
    )


def test_failed_login_counts(conn):
    """
    Sanity-check that the failed-login numbers (success = 0) match the
    values that downstream tasks rely on.
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT username, COUNT(*) AS failed_count
        FROM logins
        WHERE success = 0
        GROUP BY username
        ORDER BY username;
    """)
    results = cur.fetchall()
    expected = [
        ("alice", 2),
        ("bob",   2),
        ("carol", 1),
    ]
    assert results == expected, (
        "Failed-login summary differs from expected.\n\nExpected:\n"
        + "\n".join(map(str, expected))
        + "\n\nFound:\n"
        + "\n".join(map(str, results))
    )


def test_report_and_log_files_absent_initially():
    """
    Before the task is run, the CSV report file must *not* yet exist.
    The log file may or may not exist (it can be pre-existing from earlier
    runs), so we do *not* enforce its absence/presence—only that the report
    itself is absent to avoid clobbering.
    """
    assert not os.path.exists(CSV_PATH), (
        f"Report file already exists at {CSV_PATH}. The student task should "
        f"create it, so the start state must *not* have this file."
    )