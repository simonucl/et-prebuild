# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# and SQLite database before the student performs any actions described in
# the assignment.  All tests must pass *before* the student starts working.

import os
import sqlite3
import stat
import pytest

CI_CD_DIR = "/home/user/ci_cd_poc"
DB_PATH = os.path.join(CI_CD_DIR, "pipelines.db")
AUDIT_DIR = os.path.join(CI_CD_DIR, "audit")
AUDIT_FILE = os.path.join(AUDIT_DIR, "deployment_audit.log")

EXPECTED_BUILD_ROWS = [
    (1, "success", "2023-01-01T10:00:00Z"),
    (2, "failed",  "2023-01-02T11:00:00Z"),
    (3, "success", "2023-01-03T12:00:00Z"),
]


@pytest.fixture(scope="module")
def db_conn():
    """
    Returns a read-only SQLite connection to the pipelines.db file.
    Raises a test failure immediately if the file is unreadable or not a
    valid SQLite database.
    """
    if not os.path.isfile(DB_PATH):
        pytest.fail(
            f"Expected SQLite database file at {DB_PATH!r}, "
            "but the file does not exist."
        )

    # Open the DB in read-only mode to ensure we don't accidentally modify it.
    uri = f"file:{DB_PATH}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        pytest.fail(f"Unable to open {DB_PATH!r} as a SQLite database: {exc}")

    # Verify the file is actually a SQLite database (PRAGMA user_version as a smoke test)
    try:
        conn.execute("PRAGMA user_version")
    except sqlite3.DatabaseError as exc:
        conn.close()
        pytest.fail(f"The file at {DB_PATH!r} is not a valid SQLite database: {exc}")

    yield conn
    conn.close()


def test_ci_cd_directory_exists():
    assert os.path.isdir(CI_CD_DIR), (
        f"Directory {CI_CD_DIR!r} is expected to exist but is missing."
    )
    # Confirm it is actually a directory and not e.g. a symlink to a file.
    mode = os.stat(CI_CD_DIR).st_mode
    assert stat.S_ISDIR(mode), (
        f"Path {CI_CD_DIR!r} exists but is not a directory."
    )


def test_database_file_exists_and_is_regular_file():
    assert os.path.exists(DB_PATH), (
        f"Database file {DB_PATH!r} is expected to exist but is missing."
    )
    assert os.path.isfile(DB_PATH), (
        f"Path {DB_PATH!r} exists but is not a regular file."
    )


def test_builds_table_exists_with_expected_schema(db_conn):
    cursor = db_conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='builds';"
    )
    table = cursor.fetchone()
    assert table is not None, (
        "Expected table 'builds' to exist in pipelines.db, but it is missing."
    )

    # Fetch column info
    cursor.execute("PRAGMA table_info(builds);")
    columns = cursor.fetchall()
    col_names_and_types = [(col[1], col[2]) for col in columns]

    expected_cols_and_types = [
        ("id", "INTEGER"),
        ("status", "TEXT"),
        ("started_at", "TEXT"),
    ]
    assert col_names_and_types == expected_cols_and_types, (
        "Table 'builds' does not have the expected schema.\n"
        f"Expected columns and types: {expected_cols_and_types}\n"
        f"Actual columns and types  : {col_names_and_types}"
    )


def test_builds_table_contains_expected_seed_rows(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT id, status, started_at FROM builds ORDER BY id ASC;")
    rows = cursor.fetchall()

    assert rows == EXPECTED_BUILD_ROWS, (
        "Seed rows in table 'builds' do not match the expected initial state.\n"
        f"Expected rows:\n{EXPECTED_BUILD_ROWS}\n"
        f"Actual rows:\n{rows}"
    )


def test_deployments_table_does_not_exist_yet(db_conn):
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='deployments';"
    )
    table = cursor.fetchone()
    assert table is None, (
        "Table 'deployments' should NOT exist in the initial state, "
        "but it is already present."
    )


def test_audit_log_does_not_exist_yet():
    assert not os.path.exists(AUDIT_FILE), (
        f"Audit file {AUDIT_FILE!r} should NOT exist in the initial state."
    )