# test_initial_state.py
#
# Pytest suite that verifies the pre-task operating-system / filesystem
# state for the “enabled services CSV” exercise.
#
# It confirms:
#   1. Presence of the /home/user/configs directory.
#   2. Presence of the SQLite database file
#        /home/user/configs/security_audit.db .
#   3. Correct schema and contents of the `services` table in that DB.
#   4. Absence of the /home/user/output directory (and therefore the
#        expected CSV artefact) prior to the student’s actions.
#
# Only the Python stdlib and pytest are used.

import os
import sqlite3
import pytest
from pathlib import Path

CONFIGS_DIR = Path("/home/user/configs")
DB_PATH      = CONFIGS_DIR / "security_audit.db"
OUTPUT_DIR   = Path("/home/user/output")
CSV_PATH     = OUTPUT_DIR / "enabled_services.csv"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _connect_to_db(db_path: Path):
    """Return a sqlite3.Connection to the given database path.

    An explicit timeout of 1 second is used to fail fast if the file is
    somehow locked or inaccessible.
    """
    return sqlite3.connect(db_path.as_posix(), timeout=1.0)


# ---------------------------------------------------------------------------
# Tests validating the initial environment
# ---------------------------------------------------------------------------

def test_configs_directory_exists():
    assert CONFIGS_DIR.is_dir(), (
        f"Required directory {CONFIGS_DIR} is missing. "
        "The exercise expects the SQLite database to live inside this "
        "directory. Please ensure the directory exists before students "
        "begin the task."
    )


def test_database_file_exists():
    assert DB_PATH.is_file(), (
        f"SQLite database file {DB_PATH} is missing. "
        "Without this file students cannot query the services table."
    )


def test_services_table_schema_and_contents():
    """
    Validate that the `services` table exists, has the expected columns,
    and contains exactly the four predefined rows (ids 1-4 with expected
    names / status values).
    """
    expected_schema = [
        (0, "id",     "INTEGER", 0, None, 1),
        (1, "name",   "TEXT",    1, None, 0),
        (2, "status", "TEXT",    1, None, 0),
    ]
    expected_rows = [
        (1, "sshd", "enabled"),
        (2, "cron", "enabled"),
        (3, "cups", "disabled"),
        (4, "ufw",  "enabled"),
    ]

    with _connect_to_db(DB_PATH) as conn:
        cur = conn.cursor()

        # ------------------------------------------------------------------
        # Validate schema using PRAGMA table_info
        # ------------------------------------------------------------------
        cur.execute("PRAGMA table_info(services);")
        schema = cur.fetchall()

        # Compare only the columns we care about, ignore everything else
        assert schema == expected_schema, (
            "Schema mismatch for table `services` in "
            f"{DB_PATH}.\nExpected columns:\n{expected_schema}\n"
            f"Found:\n{schema}"
        )

        # ------------------------------------------------------------------
        # Validate rows
        # ------------------------------------------------------------------
        cur.execute(
            "SELECT id, name, status FROM services ORDER BY id ASC;"
        )
        rows = cur.fetchall()

        assert rows == expected_rows, (
            "Row data in `services` table does not match the expected "
            "initial dataset.\nExpected rows (ordered by id):\n"
            f"{expected_rows}\nFound:\n{rows}"
        )


def test_output_directory_absent():
    """
    Prior to the student's task execution, the output directory must not
    exist.  Its presence could indicate leftover files from a prior run
    and would invalidate the initial state assumptions.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} should *not* exist before the task is "
        "performed. If it is present, please remove it to restore the "
        "clean initial environment."
    )

    # If (unexpectedly) the directory exists, also check that the CSV file
    # is absent, to provide a clearer failure reason.
    if OUTPUT_DIR.exists():
        assert not CSV_PATH.exists(), (
            f"Found unexpected file {CSV_PATH}. The CSV report must not "
            "exist before the student has run their solution."
        )