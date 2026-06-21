# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state *before* the learner performs any actions.
#
# It verifies (1) the presence and basic permissions of the releases
# directory, (2) the existence of the SQLite database file, and
# (3) the schema and data that must already be present inside that
# database.  These checks guarantee that the starting point is exactly
# what the task description specifies.
#
# NOTE:  Per the grading-framework rules we intentionally DO NOT check
# for the existence (or non-existence) of any output files or
# directories such as /home/user/release_logs or
# /home/user/release_logs/pending_count.log.  Only the prerequisite
# artefacts are verified here.
#
# This file uses only the Python standard library plus pytest.

import os
import stat
import sqlite3
import pytest

HOME = "/home/user"
RELEASES_DIR = os.path.join(HOME, "releases")
DB_PATH = os.path.join(RELEASES_DIR, "app_releases.db")


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def mode_bits(path):
    """Return the permission bits (e.g. 0o755) for the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def fetchall(conn, query, params=()):
    """Run a SELECT query and return all rows."""
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_releases_directory_present_and_mode_755():
    """The /home/user/releases directory must exist with mode 755."""
    assert os.path.isdir(RELEASES_DIR), (
        f"Required directory {RELEASES_DIR} does not exist or is not a directory."
    )

    expected_mode = 0o755
    actual_mode = mode_bits(RELEASES_DIR)
    assert actual_mode == expected_mode, (
        f"{RELEASES_DIR} exists but has mode {oct(actual_mode)}; "
        f"expected {oct(expected_mode)} (rwxr-xr-x)."
    )


def test_database_file_exists():
    """The SQLite database file must already be present."""
    assert os.path.isfile(DB_PATH), (
        f"Expected SQLite database file {DB_PATH} to exist, but it does not."
    )


@pytest.fixture(scope="module")
def db_connection():
    """Open a read-only connection to the existing SQLite database."""
    # The URI format allows us to open in read-only mode; safeguards against
    # accidental writes during the test.
    uri = f"file:{DB_PATH}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Unable to open SQLite database {DB_PATH}: {exc}")
    yield conn
    conn.close()


def test_releases_table_schema(db_connection):
    """Validate that the 'releases' table exists with the correct columns."""
    rows = fetchall(
        db_connection,
        "PRAGMA table_info(releases)"
    )

    assert rows, (
        "Table 'releases' is missing from the database; expected it to exist."
    )

    # Extract column name and type.
    columns = {row[1]: row[2].upper() for row in rows}  # row[1]=name, row[2]=type
    expected_columns = {
        "version": "TEXT",
        "status": "TEXT",
    }

    missing = [col for col in expected_columns if col not in columns]
    extra = [col for col in columns if col not in expected_columns]

    assert not missing, (
        f"Table 'releases' is missing expected columns: {missing}"
    )
    assert not extra, (
        f"Table 'releases' contains unexpected extra columns: {extra}"
    )

    # Confirm the column types match.
    mismatched_types = {
        col: (expected_columns[col], columns[col])
        for col in expected_columns
        if columns[col] != expected_columns[col]
    }
    assert not mismatched_types, (
        "Column type mismatches found in 'releases' table: "
        + ", ".join(
            f"{col} expected {exp} got {got}"
            for col, (exp, got) in mismatched_types.items()
        )
    )


def test_releases_table_contents(db_connection):
    """Ensure the table has exactly the five rows described in the prompt."""
    all_rows = fetchall(db_connection, "SELECT version, status FROM releases ORDER BY version")

    expected_rows = [
        ('v1.0.0',      'released'),
        ('v1.1.0',      'released'),
        ('v2.0.0',      'released'),
        ('v2.1.0-beta', 'pending'),
        ('v2.2.0',      'pending'),
    ]

    assert len(all_rows) == len(expected_rows), (
        f"Expected exactly {len(expected_rows)} rows in 'releases' table, "
        f"found {len(all_rows)}."
    )

    # Convert to lists for order-agnostic comparison.
    assert sorted(all_rows) == sorted(expected_rows), (
        "Contents of 'releases' table do not match the expected dataset.\n"
        f"Expected rows:\n  {expected_rows}\n"
        f"Actual rows:\n  {all_rows}"
    )


def test_pending_count_is_two(db_connection):
    """There must be exactly two rows whose status == 'pending'."""
    (pending_count,) = fetchall(
        db_connection,
        "SELECT COUNT(*) FROM releases WHERE status = ?",
        ("pending",)
    )[0]

    assert pending_count == 2, (
        f"Expected 2 pending releases, but found {pending_count}."
    )