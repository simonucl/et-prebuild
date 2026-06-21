# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating
# system / file-system before the student performs any action.
#
# It verifies that:
#   • /home/user/ml_data/            exists and has 0o755 permissions
#   • /home/user/ml_data/training.db exists and has 0o644 permissions
#   • The SQLite database contains a table `training_samples`
#       with the expected schema and rows.
#
# No checks are made for the /export/ directory or for the CSV file
# that the student will create later.

import os
import stat
import sqlite3
import pytest

ML_DATA_DIR = "/home/user/ml_data"
TRAINING_DB  = "/home/user/ml_data/training.db"

EXPECTED_DIR_MODE = 0o755
EXPECTED_FILE_MODE = 0o644

EXPECTED_SCHEMA = [
    # cid, name, type, notnull, dflt_value, pk
    (0, "id",    "INTEGER", 0, None, 1),
    (1, "text",  "TEXT",    0, None, 0),
    (2, "label", "INTEGER", 0, None, 0),
]

EXPECTED_ROWS = [
    (1, "hello world",   0),
    (2, "goodbye world", 1),
    (3, "test sample",   0),
]

# ---------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------
def _mode(path: str) -> int:
    """Return the permission bits of *path* (e.g. 0o755)."""
    return stat.S_IMODE(os.stat(path).st_mode)

# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------
def test_ml_data_directory_exists_and_permissions():
    assert os.path.isdir(ML_DATA_DIR), (
        f"Required directory {ML_DATA_DIR} is missing."
    )
    mode = _mode(ML_DATA_DIR)
    assert mode == EXPECTED_DIR_MODE, (
        f"Directory {ML_DATA_DIR} should have permissions "
        f"{oct(EXPECTED_DIR_MODE)} but has {oct(mode)}."
    )

def test_training_db_exists_and_permissions():
    assert os.path.isfile(TRAINING_DB), (
        f"Required SQLite database file {TRAINING_DB} is missing."
    )
    mode = _mode(TRAINING_DB)
    assert mode == EXPECTED_FILE_MODE, (
        f"Database file {TRAINING_DB} should have permissions "
        f"{oct(EXPECTED_FILE_MODE)} but has {oct(mode)}."
    )

def test_training_db_schema_and_rows():
    # Connect in read-only mode when possible
    uri = f"file:{TRAINING_DB}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError:
        # Fallback for older SQLite versions without URI support
        conn = sqlite3.connect(TRAINING_DB)

    with conn:
        cur = conn.cursor()

        # -----------------------------------------------------------------
        # Verify the table exists
        # -----------------------------------------------------------------
        cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='training_samples';"
        )
        tab = cur.fetchone()
        assert tab is not None, (
            "The SQLite database does not contain a table named "
            "'training_samples'."
        )

        # -----------------------------------------------------------------
        # Verify schema via PRAGMA table_info
        # -----------------------------------------------------------------
        cur.execute("PRAGMA table_info(training_samples);")
        schema = cur.fetchall()
        # For a clearer diff on failure convert to str
        assert schema == EXPECTED_SCHEMA, (
            "Schema mismatch for table 'training_samples'.\n"
            f"Expected: {EXPECTED_SCHEMA}\n"
            f"Found:    {schema}"
        )

        # -----------------------------------------------------------------
        # Verify data
        # -----------------------------------------------------------------
        cur.execute("SELECT id, text, label FROM training_samples ORDER BY id;")
        rows = cur.fetchall()
        assert rows == EXPECTED_ROWS, (
            "Data mismatch in table 'training_samples'.\n"
            f"Expected rows (in id order): {EXPECTED_ROWS}\n"
            f"Found:                        {rows}"
        )