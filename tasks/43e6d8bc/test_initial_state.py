# test_initial_state.py
#
# Pytest suite to validate the OS / filesystem *before* the student’s
# work begins.  It asserts the presence of the initial SQLite database
# and the absence of any backup artefacts.

import os
import stat
import datetime
import sqlite3
import pytest

HOME_DIR = "/home/user"
DATA_DIR = os.path.join(HOME_DIR, "data")
DB_PATH  = os.path.join(DATA_DIR, "company.db")
ARCHIVE_DIR = os.path.join(HOME_DIR, "archive")

# Helpers ---------------------------------------------------------------------


def utc_today_ymd() -> str:
    """Return today’s date in UTC formatted as YYYYMMDD."""
    return datetime.datetime.utcnow().strftime("%Y%m%d")


def expected_archive_paths():
    """Return paths that will eventually be created by the student."""
    ymd = utc_today_ymd()
    dump_file = os.path.join(ARCHIVE_DIR, f"company_{ymd}.sql")
    tar_file  = os.path.join(ARCHIVE_DIR, f"company_backup_{ymd}.tar.gz")
    log_file  = os.path.join(ARCHIVE_DIR, "backup.log")
    return dump_file, tar_file, log_file


# Tests -----------------------------------------------------------------------


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), (
        f"Expected {HOME_DIR} to exist and be a directory."
    )


def test_database_file_exists_and_valid():
    # --- file existence & type ------------------------------------------------
    assert os.path.isfile(DB_PATH), (
        f"Required SQLite database not found at {DB_PATH}"
    )
    st = os.stat(DB_PATH)
    assert stat.S_ISREG(st.st_mode), (
        f"{DB_PATH} exists but is not a regular file."
    )
    assert st.st_size > 0, f"{DB_PATH} is empty."

    # --- open read-only and examine contents ----------------------------------
    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        pytest.fail(f"Could not open SQLite database at {DB_PATH}: {exc}")

    with conn:
        # verify table exists
        tables = {
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            )
        }
        assert "employees" in tables, (
            "Table 'employees' not found in the initial database."
        )

        # verify schema (column names)
        cols = [
            row[1] for row in conn.execute("PRAGMA table_info(employees);")
        ]
        expected_cols = ["id", "name", "department", "salary"]
        assert cols == expected_cols, (
            f"'employees' table schema mismatch. "
            f"Expected columns {expected_cols}, got {cols}"
        )

        # verify row count == 5
        (row_count,) = conn.execute("SELECT COUNT(*) FROM employees;").fetchone()
        assert row_count == 5, (
            f"Expected 5 rows in employees table, found {row_count}."
        )


def test_archive_directory_absent_initially():
    assert not os.path.exists(ARCHIVE_DIR), (
        f"{ARCHIVE_DIR} should NOT exist before the backup task begins."
    )


def test_no_preexisting_backup_artifacts():
    dump_file, tar_file, log_file = expected_archive_paths()

    for path in (dump_file, tar_file, log_file):
        assert not os.path.exists(path), (
            f"Backup artifact {path} should not exist prior to running the task."
        )