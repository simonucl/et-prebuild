# test_initial_state.py
#
# Pytest suite verifying the filesystem and database **before** the student
# runs the required shell command.  All checks must pass on the pristine
# machine state that the exercise describes.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

# ---------- Constants -------------------------------------------------------

HOME               = Path("/home/user")
SCAN_DIR           = HOME / "vuln_scans"
DB_FILE            = SCAN_DIR / "scan_results.db"
CSV_OUTPUT_FILE    = SCAN_DIR / "high_vulns.csv"

EXPECTED_TABLE     = "vulnerabilities"
EXPECTED_COLUMNS   = [
    ("id",       "INTEGER"),
    ("host",     "TEXT"),
    ("port",     "INTEGER"),
    ("service",  "TEXT"),
    ("severity", "TEXT"),
    ("cvss",     "REAL"),
]

EXPECTED_ROWS = [
    (1, "192.168.1.10", 22,  "ssh", "HIGH",   9.0),
    (2, "192.168.1.10", 80,  "http", "MEDIUM", 6.5),
    (3, "192.168.1.11", 445, "smb", "HIGH",   8.6),
    (4, "192.168.1.12", 21,  "ftp", "LOW",    3.7),
]

# ---------- Helper functions -------------------------------------------------

def _open_db():
    """Open the SQLite database in read-only mode to avoid accidental writes."""
    uri = f"file:{DB_FILE}?mode=ro"
    try:
        return sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Could not open SQLite database at '{DB_FILE}': {exc}")

# ---------- Tests -----------------------------------------------------------

def test_vuln_scans_directory_exists_and_is_accessible():
    assert SCAN_DIR.exists(), f"Required directory '{SCAN_DIR}' is missing."
    assert SCAN_DIR.is_dir(), f"'{SCAN_DIR}' exists but is not a directory."
    mode = SCAN_DIR.stat().st_mode
    # Directory should be at least readable/executable by owner.
    assert mode & stat.S_IRUSR, f"Directory '{SCAN_DIR}' is not readable by the user."
    assert mode & stat.S_IXUSR, f"Directory '{SCAN_DIR}' is not accessible (no execute bit for user)."

def test_scan_results_db_file_exists():
    assert DB_FILE.exists(), f"Database file '{DB_FILE}' is missing."
    assert DB_FILE.is_file(), f"Path '{DB_FILE}' exists but is not a regular file."
    size = DB_FILE.stat().st_size
    assert size > 0, f"Database file '{DB_FILE}' is empty (size 0 bytes)."

def test_database_has_expected_single_table_and_schema():
    with _open_db() as conn:
        cur = conn.cursor()

        # Ensure exactly one user table exists and it is the expected one.
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cur.fetchall()]
        assert tables == [EXPECTED_TABLE], (
            f"Database should contain exactly one table named "
            f"'{EXPECTED_TABLE}', but found: {tables}"
        )

        # Verify column order, names, and (case-insensitive) types.
        cur.execute(f"PRAGMA table_info({EXPECTED_TABLE});")
        pragma_rows = cur.fetchall()
        seen_cols = [(row[1], row[2].upper()) for row in pragma_rows]

        expected_names  = [name for name, _ in EXPECTED_COLUMNS]
        found_names     = [name for name, _ in seen_cols]
        assert found_names == expected_names, (
            f"Column names/order mismatch.\n"
            f"Expected: {expected_names}\nFound:    {found_names}"
        )

        expected_types = [ctype.upper() for _, ctype in EXPECTED_COLUMNS]
        found_types    = [ctype.upper() for _, ctype in seen_cols]
        assert found_types == expected_types, (
            f"Column type mismatch.\n"
            f"Expected: {expected_types}\nFound:    {found_types}"
        )

def test_vulnerabilities_table_contains_exact_expected_rows():
    with _open_db() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {EXPECTED_TABLE} ORDER BY id ASC;")
        rows = cur.fetchall()

    assert rows == EXPECTED_ROWS, (
        "Data in table 'vulnerabilities' does not match the expected fixture.\n"
        f"Expected rows ({len(EXPECTED_ROWS)}):\n{EXPECTED_ROWS}\n"
        f"Found rows ({len(rows)}):\n{rows}"
    )

def test_output_csv_does_not_preexist():
    assert not CSV_OUTPUT_FILE.exists(), (
        f"Output CSV '{CSV_OUTPUT_FILE}' already exists before the task is run; "
        "it should be created by the student's command."
    )