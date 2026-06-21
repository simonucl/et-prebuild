# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student executes any migration commands.
#
# It checks that the pre-existing on-prem SQLite dump is present and correct
# and that **no** artefacts from the required end-state have been created yet.
#
# Only stdlib + pytest are used as mandated.

import os
import sqlite3
import pytest

HOME = "/home/user"
MIGRATION_DIR = os.path.join(HOME, "migration")
SOURCE_DB = os.path.join(MIGRATION_DIR, "source_app.db")
BACKUP_DIR = os.path.join(MIGRATION_DIR, "backup")
BACKUP_DB = os.path.join(BACKUP_DIR, "source_app_backup.db")
DEST_DB = os.path.join(MIGRATION_DIR, "dest_app.db")
CSV_EXPORT = os.path.join(MIGRATION_DIR, "customer_export.csv")
MIGRATION_LOG = os.path.join(MIGRATION_DIR, "migration.log")

EXPECTED_ROWS = [
    (1, "Alice Chen", "alice.chen@example.com"),
    (2, "Bob Gupta", "bob.gupta@example.com"),
    (3, "Carla Diaz", "carla.diaz@example.com"),
]


def test_migration_directory_exists_and_writable():
    assert os.path.isdir(
        MIGRATION_DIR
    ), f"Required directory {MIGRATION_DIR!r} does not exist."
    assert os.access(
        MIGRATION_DIR, os.W_OK
    ), f"Directory {MIGRATION_DIR!r} is not writable by the current user."


def test_source_db_exists_and_non_empty():
    assert os.path.isfile(
        SOURCE_DB
    ), f"Source database {SOURCE_DB!r} does not exist."
    assert os.path.getsize(
        SOURCE_DB
    ) > 0, f"Source database {SOURCE_DB!r} is empty (size == 0 bytes)."


@pytest.fixture(scope="module")
def source_conn():
    """SQLite connection to the source database, closed after the module."""
    conn = sqlite3.connect(f"file:{SOURCE_DB}?mode=ro", uri=True)
    try:
        yield conn
    finally:
        conn.close()


def test_source_db_integrity(source_conn):
    cursor = source_conn.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    assert (
        result == "ok"
    ), f"PRAGMA integrity_check on {SOURCE_DB!r} returned {result!r}, expected 'ok'."


def test_source_db_schema(source_conn):
    # Verify that exactly one table named 'customers' exists
    tables = [
        row[0]
        for row in source_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
    ]
    assert tables == ["customers"], (
        f"Expected a single table ['customers'] in {SOURCE_DB!r}, "
        f"found {tables}."
    )

    # Verify column definitions (name and order)
    expected_columns = [("id",), ("name",), ("email",)]
    actual_columns = [
        (row[1],) for row in source_conn.execute("PRAGMA table_info(customers);")
    ]
    assert actual_columns == expected_columns, (
        f"customers table columns are {actual_columns}, "
        f"expected {expected_columns}."
    )


def test_source_db_row_contents(source_conn):
    rows = list(
        source_conn.execute(
            "SELECT id, name, email FROM customers ORDER BY id ASC;"
        )
    )
    assert rows == EXPECTED_ROWS, (
        f"Row contents in {SOURCE_DB!r} are {rows}, expected {EXPECTED_ROWS}."
    )


def _assert_absent(path: str):
    assert not os.path.exists(
        path
    ), f"Artefact {path!r} already exists before migration begins."


def test_no_destination_artefacts_exist():
    """
    Ensure that none of the artefacts the student is expected to create
    during the migration are present yet.
    """
    for artefact in (BACKUP_DIR, BACKUP_DB, DEST_DB, CSV_EXPORT, MIGRATION_LOG):
        _assert_absent(artefact)