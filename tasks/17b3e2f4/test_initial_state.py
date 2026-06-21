# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state *before* the student executes any action.  It checks that the
# required directories, SQLite database file, table schema, and seed data
# are present and exactly match the specification in the task description.
#
# NOTE:  Per the instructions, we deliberately do **not** test for the
#        existence or contents of any *output* files that the student is
#        supposed to create later (e.g. gateway_fail_2023-10-05.log).

import os
import stat
import sqlite3
from pathlib import Path

# Hard-coded absolute paths as required
NETWORK_DIR = Path("/home/user/network")
REPORTS_DIR = NETWORK_DIR / "reports"
DB_PATH = NETWORK_DIR / "conn_logs.db"

# Expected rows in ping_results (order by id)
EXPECTED_ROWS = [
    (1, "gateway", "failure", "2023-10-05 00:12:34"),
    (2, "gateway", "failure", "2023-10-05 05:45:12"),
    (3, "gateway", "success", "2023-10-05 06:00:01"),
    (4, "gateway", "failure", "2023-10-05 23:59:59"),
    (5, "router1", "failure", "2023-10-05 10:22:11"),
    (6, "gateway", "failure", "2023-10-04 20:00:00"),
    (7, "gateway", "success", "2023-10-03 08:00:00"),
]


def _assert_path_is_directory(path: Path) -> None:
    assert path.exists(), f"Required directory {path} is missing."
    assert path.is_dir(), f"{path} exists but is not a directory."
    # Optional: basic permission sanity (world-executable bit should be set for 0755)
    mode = path.stat().st_mode
    assert mode & stat.S_IXUSR, f"{path} should be accessible/executable by owner."


def _assert_path_is_file(path: Path) -> None:
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."


def test_directories_exist():
    """Verify that /home/user/network and .../reports directories exist."""
    _assert_path_is_directory(NETWORK_DIR)
    _assert_path_is_directory(REPORTS_DIR)


def test_database_file_exists():
    """Verify that the SQLite database file exists and is a regular file."""
    _assert_path_is_file(DB_PATH)


def test_database_schema_and_seed_data():
    """
    Validate that the ping_results table exists with the correct schema
    and contains exactly the seven expected rows.
    """
    # Connect read-only if the SQLite version supports it; otherwise default.
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = conn.cursor()

        # ----- Schema checks -------------------------------------------------
        cur.execute("PRAGMA table_info(ping_results);")
        cols = [(row[1], row[2]) for row in cur.fetchall()]  # (name, type)
        expected_cols = [
            ("id", "INTEGER"),
            ("host", "TEXT"),
            ("status", "TEXT"),
            ("timestamp", "TEXT"),
        ]
        assert cols == expected_cols, (
            "ping_results table schema mismatch.\n"
            f"Expected columns: {expected_cols}\n"
            f"Found columns   : {cols}"
        )

        # ----- Data checks ---------------------------------------------------
        cur.execute("SELECT * FROM ping_results ORDER BY id;")
        rows = cur.fetchall()
        assert rows == EXPECTED_ROWS, (
            "Seed data in ping_results does not match the specification.\n"
            f"Expected rows:\n{EXPECTED_ROWS}\n\nFound rows:\n{rows}"
        )

        # Extra: ensure the task's query would yield exactly 3.
        cur.execute(
            """
            SELECT COUNT(*)
            FROM ping_results
            WHERE host = 'gateway'
              AND status = 'failure'
              AND date(timestamp) = '2023-10-05'
            ;"""
        )
        (count,) = cur.fetchone()
        assert count == 3, (
            "Pre-populated database should yield 3 failed pings for "
            "host 'gateway' on 2023-10-05, but query returned "
            f"{count} instead."
        )
    finally:
        conn.close()