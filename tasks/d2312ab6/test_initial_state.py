# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student performs any actions for the “release-manager”
# exercise.
#
# Checks performed:
#   1. /home/user/app_release.db
#        • File exists and is a valid SQLite database.
#        • Contains a table called “releases” with the correct schema.
#        • Table currently holds exactly the two expected rows and NO row
#          whose version is 'v1.2.3'.
#   2. /home/user/release_log.csv
#        • File must NOT exist at the outset.
#
# No third-party libraries are used—only the Python stdlib and pytest.

import os
import sqlite3
from pathlib import Path

import pytest

HOME = Path("/home/user")
DB_PATH = HOME / "app_release.db"
LOG_PATH = HOME / "release_log.csv"


def _fetchall(conn, query, params=()):
    """Utility helper to run a query and fetch all rows."""
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def test_database_file_exists_and_is_sqlite():
    assert DB_PATH.is_file(), (
        f"Expected SQLite database at {DB_PATH}, but the file does not exist."
    )

    # Attempt to open the database; sqlite3.DatabaseError will be raised
    # if the file is not a valid SQLite database.
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA schema_version;")
    except sqlite3.DatabaseError as exc:
        pytest.fail(
            f"File {DB_PATH} exists but is not a valid SQLite database: {exc}"
        )


def test_releases_table_schema():
    expected_schema = [
        ("id", "INTEGER"),
        ("version", "TEXT"),
        ("status", "TEXT"),
    ]

    with sqlite3.connect(DB_PATH) as conn:
        rows = _fetchall(conn, "PRAGMA table_info(releases);")

    assert rows, (
        "Table 'releases' does not exist in the database "
        f"{DB_PATH} or pragma returned no columns."
    )

    # Reduce to (name, type)
    actual_schema = [(row[1], row[2].upper()) for row in rows]

    assert actual_schema == expected_schema, (
        "Schema mismatch for 'releases' table.\n"
        f"Expected columns: {expected_schema}\n"
        f"Found columns:    {actual_schema}"
    )


def test_releases_table_initial_rows():
    expected_rows = [
        ("v1.0.0", "deployed"),
        ("v1.1.0", "deployed"),
    ]
    with sqlite3.connect(DB_PATH) as conn:
        rows = _fetchall(
            conn, "SELECT version, status FROM releases ORDER BY id;"
        )

    assert rows == expected_rows, (
        "Unexpected initial data in 'releases' table.\n"
        f"Expected rows (ordered by id): {expected_rows}\n"
        f"Found rows:                    {rows}"
    )

    # Ensure target version is not already present
    disallowed_version = "v1.2.3"
    assert all(v != disallowed_version for v, _ in rows), (
        f"Version '{disallowed_version}' is already present in the "
        "'releases' table. The student should insert it during the task; "
        "it must NOT exist beforehand."
    )


def test_release_log_does_not_exist():
    assert not LOG_PATH.exists(), (
        f"File {LOG_PATH} should NOT exist before the student "
        "runs the task, but it is present."
    )