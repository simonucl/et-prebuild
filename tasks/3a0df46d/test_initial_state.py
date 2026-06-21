# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / filesystem
# state before the student carries out any work for the “authentication-log
# breach” incident–response task.
#
# The tests intentionally:
#   • confirm that the ir_breach directory and breach.db are present and sane;
#   • ensure that *output* artefacts (findings.log, incident_report.txt) do
#     NOT yet exist;
#   • validate the exact shape and content of the SQLite database so later
#     tests can rely on a known ground-truth.
#
# Only the Python standard library and pytest are used.
#
# Author: CI-grader bot
# ---------------------------------------------------------------------------

import os
import stat
import sqlite3
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/ir_breach")
DB_PATH = BASE_DIR / "breach.db"
FINDINGS_PATH = BASE_DIR / "findings.log"
REPORT_PATH = BASE_DIR / "incident_report.txt"

# Ground-truth expectations taken from the task description
EXPECTED_FAIL_ROWS = [
    ("2023-08-10 05:05:43", "root",   "203.0.113.45", "FAIL"),
    ("2023-08-10 05:05:55", "root",   "203.0.113.45", "FAIL"),
    ("2023-08-10 05:06:12", "root",   "203.0.113.45", "FAIL"),
    ("2023-08-10 05:07:01", "bob",    "198.51.100.23", "FAIL"),
    ("2023-08-10 05:10:42", "bob",    "198.51.100.23", "FAIL"),
    ("2023-08-10 05:11:33", "david",  "203.0.113.78", "FAIL"),
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _octal_mode(path: Path) -> int:
    """Return a path's permission bits as an octal integer (e.g., 0o755)."""
    return stat.S_IMODE(path.stat().st_mode)


def _sqlite_tables(conn: sqlite3.Connection):
    """Return a {table_name: [list_of_column_names]} mapping for a connection."""
    tables = {}
    cur = conn.cursor()
    for (tbl_name,) in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall():
        cols = [
            row[1]  # second field returned by PRAGMA table_info: column name
            for row in cur.execute(f"PRAGMA table_info({tbl_name});")
        ]
        tables[tbl_name] = cols
    return tables


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_ir_breach_directory_exists_and_is_755():
    assert BASE_DIR.exists(), f"Required directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(),  f"{BASE_DIR} exists but is not a directory."
    mode = _octal_mode(BASE_DIR)
    assert mode == 0o755, (
        f"{BASE_DIR} permissions expected 755 but found {oct(mode)}."
    )


def test_breach_db_file_exists_and_looks_like_sqlite():
    assert DB_PATH.exists(), f"Database file {DB_PATH} is missing."
    assert DB_PATH.is_file(), f"{DB_PATH} exists but is not a regular file."
    # A SQLite-3 file must start with the magic header "SQLite format 3\0"
    with DB_PATH.open("rb") as fh:
        header = fh.read(16)
    assert header.startswith(b"SQLite format 3"), (
        f"{DB_PATH} does not appear to be a valid SQLite 3 database."
    )


def test_breach_db_schema_is_correct():
    with sqlite3.connect(DB_PATH) as conn:
        tables = _sqlite_tables(conn)

        # Exactly one table named 'auth_log'
        assert list(tables.keys()) == ["auth_log"], (
            "Database must contain exactly one table named 'auth_log'. "
            f"Found: {list(tables.keys())}"
        )

        expected_columns = ["id", "timestamp", "username", "src_ip", "action"]
        assert tables["auth_log"] == expected_columns, (
            "Table 'auth_log' must have the columns "
            f"{expected_columns} (in this order). Found: {tables['auth_log']}"
        )


def test_breach_db_contains_expected_rows():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # Total rows
        cur.execute("SELECT COUNT(*) FROM auth_log;")
        (row_count,) = cur.fetchone()
        assert row_count == 10, (
            f"Expected 10 total rows in auth_log but found {row_count}."
        )

        # FAIL rows
        cur.execute(
            """
            SELECT timestamp, username, src_ip, action
            FROM auth_log
            WHERE action='FAIL'
            ORDER BY timestamp ASC;
            """
        )
        fail_rows = cur.fetchall()

        # There must be exactly six FAIL rows in chronological order
        assert len(fail_rows) == 6, (
            f"Expected 6 rows where action='FAIL' but found {len(fail_rows)}."
        )
        assert fail_rows == EXPECTED_FAIL_ROWS, (
            "FAIL rows do not match the expected ground-truth.\n"
            f"Expected:\n{EXPECTED_FAIL_ROWS}\nFound:\n{fail_rows}"
        )


def test_no_output_files_exist_yet():
    for p in (FINDINGS_PATH, REPORT_PATH):
        assert not p.exists(), (
            f"Output artefact {p} should NOT exist before the student starts."
        )


def test_directory_contains_only_breach_db():
    allowed = {"breach.db"}
    contents = {p.name for p in BASE_DIR.iterdir() if not p.name.startswith(".")}
    extras = contents - allowed
    assert not extras, (
        f"Unexpected extra files/directories in {BASE_DIR}: {sorted(extras)}\n"
        "The initial state should only contain breach.db (plus hidden files if "
        "the environment adds any)."
    )