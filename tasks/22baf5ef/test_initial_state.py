# test_initial_state.py
#
# Pytest suite that validates the starting state of the operating system /
# filesystem prior to the student running their solution script.
#
# It checks:
#   • /home/user/release_info.db exists, is a file, and is writable.
#   • The database contains exactly one table called `deployments`
#     whose schema matches the specification.
#   • The table contains exactly eight specific rows.
#   • /home/user/today_pending.csv does NOT yet exist.
#
# Only stdlib + pytest are used.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

HOME = Path("/home/user")
DB_PATH = HOME / "release_info.db"
CSV_PATH = HOME / "today_pending.csv"

# --------------------------------------------------------------------------- #
# Helper data used by several tests                                           #
# --------------------------------------------------------------------------- #

EXPECTED_SCHEMA = [
    ("id", "INTEGER", 1),            # (name, declared type, pk)
    ("project", "TEXT", 0),
    ("environment", "TEXT", 0),
    ("scheduled_date", "TEXT", 0),
    ("status", "TEXT", 0),
]

EXPECTED_ROWS = [
    (1, "core-api",          "production", "2024-01-10", "completed"),
    (2, "core-api",          "staging",    "2024-01-10", "completed"),
    (3, "analytics-service", "production", "2024-01-15", "pending"),
    (4, "internal-tool",     "dev",        "2024-01-12", "in_progress"),
    (5, "logging-service",   "production", "2024-01-18", "scheduled"),
    (6, "search",            "staging",    "2024-01-11", "completed"),
    (7, "web-frontend",      "staging",    "2024-01-15", "pending"),
    (8, "billing",           "production", "2024-01-15", "canceled"),
]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_database_file_exists_and_is_writable():
    assert DB_PATH.exists(), f"Expected database file at {DB_PATH} but it does not exist."
    assert DB_PATH.is_file(), f"Expected {DB_PATH} to be a regular file."
    # Check write permission for the current user
    assert os.access(DB_PATH, os.W_OK), f"Database file {DB_PATH} is not writable by current user."


def test_no_report_file_yet():
    assert not CSV_PATH.exists(), (
        f"The report file {CSV_PATH} already exists, but the task has not been run yet. "
        "Please ensure the environment starts without this file."
    )


def test_database_contains_single_deployments_table():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        tables = [row[0] for row in cur.fetchall()]

    assert tables == ["deployments"], (
        f"Expected exactly one table named 'deployments', found: {tables}"
    )


def test_deployments_schema_matches_specification():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("PRAGMA table_info('deployments');")
        pragma_info = cur.fetchall()

    # Transform pragma rows into (name, type, pk) tuples for easier comparison
    simplified = [(name, col_type.upper(), pk) for _, name, col_type, _, _, pk in pragma_info]

    # Direct comparison preserves both order and content
    assert simplified == EXPECTED_SCHEMA, (
        "Schema mismatch for table 'deployments'.\n"
        f"Expected (name, type, pk): {EXPECTED_SCHEMA}\n"
        f"Found   (name, type, pk): {simplified}"
    )


def test_deployments_table_contains_expected_rows():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT id, project, environment, scheduled_date, status "
            "FROM deployments ORDER BY id;"
        )
        rows = cur.fetchall()

    assert rows == EXPECTED_ROWS, (
        "Table 'deployments' does not contain the expected initial data.\n"
        f"Expected rows ({len(EXPECTED_ROWS)}):\n{EXPECTED_ROWS}\n"
        f"Found rows ({len(rows)}):\n{rows}"
    )