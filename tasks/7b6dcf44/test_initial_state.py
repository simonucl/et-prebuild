# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem state
# that must be present **before** the student carries out the task.
#
# It intentionally does NOT look for any output artefacts that the student is
# supposed to create later (e.g. /home/user/incident_report.txt).

import os
import stat
import sqlite3
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #
HOME_DIR = Path("/home/user")
DATA_DIR = HOME_DIR / "data"
DB_FILE = DATA_DIR / "infra.db"

EXPECTED_DIR_MODE = 0o700
EXPECTED_FILE_MODE = 0o644

EXPECTED_ALERT_ROWS = [
    (1, "Sev1", "Open"),
    (2, "Sev1", "Acknowledged"),
    (3, "Sev1", "Resolved"),
    (4, "Sev2", "Open"),
    (5, "Sev1", "Open"),
    (6, "Sev3", "Closed"),
]
EXPECTED_UNRESOLVED_SEV1_COUNT = 3


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _octal_permission_bits(st_mode: int) -> int:
    """
    Return the permission bits (e.g. 0o755) from st_mode.
    """
    return stat.S_IMODE(st_mode)


def _connect_db(path: Path):
    """
    Connect to a SQLite database in read-only mode to prevent any accidental
    modification of the initial state.
    """
    uri = f"file:{path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_data_directory_exists_with_correct_permissions():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."

    mode = _octal_permission_bits(DATA_DIR.stat().st_mode)
    assert (
        mode == EXPECTED_DIR_MODE
    ), f"{DATA_DIR} permissions are {oct(mode)}, expected {oct(EXPECTED_DIR_MODE)}."


def test_db_file_exists_with_correct_permissions():
    assert DB_FILE.exists(), f"SQLite file {DB_FILE} is missing."
    assert DB_FILE.is_file(), f"{DB_FILE} exists but is not a regular file."

    mode = _octal_permission_bits(DB_FILE.stat().st_mode)
    assert (
        mode == EXPECTED_FILE_MODE
    ), f"{DB_FILE} permissions are {oct(mode)}, expected {oct(EXPECTED_FILE_MODE)}."


def test_alerts_table_and_contents_are_correct():
    # Connect read-only.
    try:
        conn = _connect_db(DB_FILE)
    except sqlite3.OperationalError as exc:
        pytest.fail(f"Could not open SQLite DB {DB_FILE}: {exc}")

    with conn:
        cur = conn.cursor()

        # Verify the alerts table exists.
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='alerts';"
        )
        row = cur.fetchone()
        assert row is not None, "Table 'alerts' is missing from the database."

        # Fetch entire table ordered by id for deterministic comparison.
        cur.execute("SELECT id, severity, status FROM alerts ORDER BY id;")
        rows = cur.fetchall()
        assert (
            rows == EXPECTED_ALERT_ROWS
        ), f"'alerts' table rows do not match expectation.\nExpected: {EXPECTED_ALERT_ROWS}\nFound   : {rows}"

        # Verify unresolved Sev1 count.
        cur.execute(
            "SELECT COUNT(*) FROM alerts WHERE severity='Sev1' AND status!='Resolved';"
        )
        (count,) = cur.fetchone()
        assert (
            count == EXPECTED_UNRESOLVED_SEV1_COUNT
        ), f"Expected {EXPECTED_UNRESOLVED_SEV1_COUNT} unresolved Sev1 alerts, found {count}."