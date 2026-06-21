# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem / database
# state before the student runs any migration commands.
#
# It checks ONLY the legacy artefacts that must already be present:
#   • /home/user/security_scans                (directory)
#   • /home/user/security_scans/scan_results_v1.db
#       – contains table "vulnerabilities"
#       – columns: id INTEGER PRIMARY KEY, host TEXT, port INTEGER, vuln TEXT
#       – exactly the three expected rows
#
# It deliberately does NOT look for the yet-to-be-created v2 database or
# the migration log, adhering strictly to the task instructions.
#
# The tests rely solely on Python’s standard library and pytest.

import os
import sqlite3
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# Constants describing the expected initial state
# ----------------------------------------------------------------------

BASE_DIR = Path("/home/user/security_scans")
V1_DB = BASE_DIR / "scan_results_v1.db"

EXPECTED_COLUMNS = [
    ("id", "INTEGER", 1),      # name, type, pk flag (1 means part of PK)
    ("host", "TEXT", 0),
    ("port", "INTEGER", 0),
    ("vuln", "TEXT", 0),
]

EXPECTED_ROWS = [
    (1, "192.168.0.5", 22,  "OpenSSH 7.2p2 outdated"),
    (2, "192.168.0.18", 445, "SMB v1 enabled"),
    (3, "10.0.0.7",     80,  "Apache 2.2 directory listing"),
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def get_table_info(cursor, table_name):
    """
    Return a list of tuples (name, type, pk) for each column in the given table,
    in the order SQLite reports them.
    """
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [(row[1], row[2].upper(), row[5]) for row in cursor.fetchall()]


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_security_scans_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Required directory '{BASE_DIR}' is missing. The initial filesystem "
        f"should contain this directory with the legacy database."
    )


def test_v1_database_file_exists():
    assert V1_DB.is_file(), (
        f"Legacy database file '{V1_DB}' is missing. Ensure the initial "
        f"state includes this SQLite database."
    )


def test_v1_database_schema_and_rows():
    # Connect read-only if possible; fallback to normal connect.
    # Using URI with mode=ro prevents accidental modifications.
    uri = f"file:{V1_DB}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError:
        conn = sqlite3.connect(V1_DB)

    with conn:
        cur = conn.cursor()

        # --- Verify table existence ---
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='vulnerabilities';"
        )
        result = cur.fetchone()
        assert result is not None, (
            "Table 'vulnerabilities' not found in the legacy database. "
            "The initial DB must contain exactly one table named 'vulnerabilities'."
        )

        # --- Verify column definitions ---
        actual_columns = get_table_info(cur, "vulnerabilities")
        expected_columns_simplified = [(n, t, pk) for n, t, pk in EXPECTED_COLUMNS]
        assert actual_columns == expected_columns_simplified, (
            "Schema mismatch in table 'vulnerabilities'.\n"
            f"Expected columns (name, type, pk): {expected_columns_simplified}\n"
            f"Found columns: {actual_columns}"
        )

        # Ensure no extra columns (e.g., 'severity') exist
        extra_columns = [col[0] for col in actual_columns if col[0] not in {c[0] for c in EXPECTED_COLUMNS}]
        assert not extra_columns, (
            f"Unexpected extra columns found in 'vulnerabilities' table: {extra_columns}. "
            "The legacy table should only have columns id, host, port, vuln."
        )

        # --- Verify row contents ---
        cur.execute("SELECT id, host, port, vuln FROM vulnerabilities ORDER BY id;")
        rows = cur.fetchall()
        assert rows == EXPECTED_ROWS, (
            "Row data in the legacy 'vulnerabilities' table does not match the "
            "expected initial contents.\n"
            f"Expected rows:\n{EXPECTED_ROWS}\n"
            f"Found rows:\n{rows}"
        )

        # --- Extra assurance: no additional rows ---
        assert len(rows) == len(EXPECTED_ROWS), (
            "The legacy 'vulnerabilities' table contains an unexpected number of rows. "
            f"Expected {len(EXPECTED_ROWS)}, found {len(rows)}."
        )