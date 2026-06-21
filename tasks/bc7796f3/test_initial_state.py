# test_initial_state.py
#
# This test-suite validates the *initial* filesystem / operating-system
# state **before** the student runs any command.
#
# What must already be true:
#   • /home/user/cluster_state.db exists and is a valid SQLite 3 database.
#   • The database contains exactly one table named “manifests” with the
#     schema:
#         id      INTEGER PRIMARY KEY
#         name    TEXT    NOT NULL
#         kind    TEXT    NOT NULL
#   • The table contains exactly the four rows listed in the task
#     description (two of them with kind='Deployment').
#   • The file /home/user/report/deployment_count.log does *not* exist yet
#     (it will be created by the student command).
#
# Any deviation from the above means the environment is not in the expected
# initial state and the tests will fail with a descriptive message.

import os
import sqlite3
import stat
import pytest

DB_PATH = "/home/user/cluster_state.db"
REPORT_FILE = "/home/user/report/deployment_count.log"


@pytest.fixture(scope="session")
def connection():
    """Return a read-only SQLite connection to the expected database."""
    # The URI trick enforces read-only mode so the test suite cannot mutate
    # the database even by accident.
    uri = f"file:{DB_PATH}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Could not open SQLite database at {DB_PATH!r}: {exc}")
    yield conn
    conn.close()


def test_db_file_exists_and_is_regular():
    assert os.path.exists(DB_PATH), (
        f"Expected database file {DB_PATH!r} to exist, "
        "but it is missing."
    )
    st = os.stat(DB_PATH)
    assert stat.S_ISREG(st.st_mode), (
        f"Expected {DB_PATH!r} to be a regular file, "
        "but it is not."
    )


def test_db_has_exactly_one_table_named_manifests(connection):
    cur = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    )
    tables = [row[0] for row in cur.fetchall()]
    assert tables == ["manifests"], (
        "Database must contain exactly one table named 'manifests'. "
        f"Found tables: {tables}"
    )


def test_table_schema_matches_specification(connection):
    cur = connection.execute("PRAGMA table_info(manifests);")
    columns = [(col[1], col[2].upper(), col[5]) for col in cur.fetchall()]
    # col[1] = name, col[2] = declared type, col[5] = pk (1 if part of PK)
    expected = [
        ("id", "INTEGER", 1),
        ("name", "TEXT", 0),
        ("kind", "TEXT", 0),
    ]
    assert columns == expected, (
        "Schema mismatch for table 'manifests'.\n"
        f"Expected columns: {expected}\n"
        f"Actual columns:   {columns}"
    )


def test_table_contains_expected_rows(connection):
    cur = connection.execute("SELECT id, name, kind FROM manifests ORDER BY id;")
    rows = cur.fetchall()
    expected_rows = [
        (1, "nginx-deployment", "Deployment"),
        (2, "redis",            "StatefulSet"),
        (3, "api-config",       "ConfigMap"),
        (4, "frontend",         "Deployment"),
    ]
    assert rows == expected_rows, (
        "Content of table 'manifests' does not match expectation.\n"
        f"Expected rows (ordered by id): {expected_rows}\n"
        f"Actual rows:                   {rows}"
    )


def test_deployment_count_is_two(connection):
    cur = connection.execute(
        "SELECT COUNT(*) FROM manifests WHERE kind='Deployment';"
    )
    (count,) = cur.fetchone()
    assert count == 2, (
        f"Expected exactly 2 rows with kind='Deployment', found {count}."
    )


def test_report_file_not_yet_present():
    assert not os.path.exists(REPORT_FILE), (
        f"Report file {REPORT_FILE!r} already exists but should be created "
        "only by the student's command."
    )