# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “stalled Android build 42” scenario.
#
# These tests must all pass *before* the student performs any action.
# They guarantee that the CI/CD environment starts from the known good state
# described in the assignment.
#
# IMPORTANT:
# • We do *not* check for the existence (or absence) of any output artefacts
#   the student is expected to create (e.g. the log file
#   /home/user/pipelines/logs/build_42_update.log).
# • Only the Python stdlib and pytest are used.

import os
import stat
import sqlite3
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PIPELINES_DIR = Path("/home/user/pipelines")
LOGS_DIR = PIPELINES_DIR / "logs"
DB_PATH = PIPELINES_DIR / "app_builds.db"

# Expected UNIX modes (permissions bits).  We compare against the lowest
# nine permission bits, i.e. st_mode & 0o777.
DIR_MODE = 0o770
DB_MODE  = 0o660

# Database expectations
EXPECTED_SCHEMA = [
    ("id",        "INTEGER", 1),
    ("platform",  "TEXT",    0),
    ("status",    "TEXT",    0),
    ("timestamp", "TEXT",    0),
]
EXPECTED_BUILD_42 = {
    "id":       42,
    "platform": "android",
    "status":   "queued",
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o770) of a file or directory."""
    return stat.S_IMODE(path.stat().st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_exist_and_permissions():
    """Check that the required directories exist with the correct modes."""
    for directory, expected_mode in [
        (PIPELINES_DIR, DIR_MODE),
        (LOGS_DIR,      DIR_MODE),
    ]:
        assert directory.exists(), f"Directory {directory} is missing."
        assert directory.is_dir(), f"{directory} exists but is not a directory."
        actual_mode = _mode(directory)
        assert actual_mode == expected_mode, (
            f"Directory {directory} has mode {oct(actual_mode)}, "
            f"expected {oct(expected_mode)}."
        )


def test_database_file_and_permissions():
    """Ensure the SQLite database file exists with correct permissions."""
    assert DB_PATH.exists(), f"Database file {DB_PATH} is missing."
    assert DB_PATH.is_file(), f"{DB_PATH} exists but is not a regular file."
    actual_mode = _mode(DB_PATH)
    assert actual_mode == DB_MODE, (
        f"Database file {DB_PATH} has mode {oct(actual_mode)}, "
        f"expected {oct(DB_MODE)}."
    )


def test_database_schema_and_contents():
    """Validate the `builds` table schema and the queued row for build 42."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # ------------------------------------------------------------------
        # Validate schema
        # ------------------------------------------------------------------
        cur.execute("PRAGMA table_info(builds);")
        # Each row of PRAGMA table_info has fields:
        # cid, name, type, notnull, dflt_value, pk
        raw_schema = cur.fetchall()
        extracted = [(row["name"], row["type"], row["pk"]) for row in raw_schema]

        assert extracted == EXPECTED_SCHEMA, (
            "Unexpected schema for 'builds' table.\n"
            f"Found:      {extracted}\n"
            f"Expected:   {EXPECTED_SCHEMA}"
        )

        # ------------------------------------------------------------------
        # Validate build 42 is queued for Android
        # ------------------------------------------------------------------
        cur.execute("SELECT * FROM builds WHERE id = 42;")
        row = cur.fetchone()
        assert row is not None, "Row with id=42 is missing in the builds table."

        # Convert to a simpler dict for comparison
        row_dict = {k: row[k] for k in ["id", "platform", "status"]}
        assert row_dict == EXPECTED_BUILD_42, (
            f"Row 42 has unexpected values.\n"
            f"Found:    {row_dict}\n"
            f"Expected: {EXPECTED_BUILD_42}"
        )


@pytest.mark.skip(reason="The output log file must not exist before student actions.")
def test_output_log_file_should_not_exist():
    """
    This test is intentionally skipped.

    We explicitly *do not* test for the presence or absence of the expected
    output file (/home/user/pipelines/logs/build_42_update.log) because it is
    the artefact the student is tasked to create.  Including such a test could
    interfere with automatic grading behaviour.
    """
    pass