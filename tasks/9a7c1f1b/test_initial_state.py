# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating
# system / filesystem before the student performs any migration work.
#
# It ensures that only the legacy SQLite database is present and that
# the project is otherwise untouched.  If any of these tests fail, the
# exercise runner itself has been provisioned incorrectly.

import os
import sqlite3
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
OLD_DB_PATH = PROJECT_DIR / "old_app.db"
DATA_DIR_PATH = PROJECT_DIR / "data"
TARGET_DB_PATH = DATA_DIR_PATH / "app_v2.db"
MIGRATION_LOG_PATH = PROJECT_DIR / "migration.log"


def test_project_directory_exists():
    """The /home/user/project directory must exist."""
    assert PROJECT_DIR.is_dir(), (
        f"Expected project directory {PROJECT_DIR} to exist, "
        "but it is missing."
    )


def test_old_database_exists_and_is_sqlite():
    """The legacy SQLite database must exist and be openable."""
    assert OLD_DB_PATH.is_file(), (
        f"Expected legacy database file {OLD_DB_PATH} to exist, "
        "but it is missing."
    )

    # Attempt to connect to ensure it is a valid SQLite database.
    try:
        conn = sqlite3.connect(str(OLD_DB_PATH))
        conn.execute("PRAGMA schema_version;")
    except sqlite3.DatabaseError as exc:
        pytest.fail(f"{OLD_DB_PATH} exists but is not a valid SQLite DB: {exc}")
    finally:
        conn.close()


def test_users_table_has_three_rows():
    """Table `users` must exist and contain exactly three rows."""
    conn = sqlite3.connect(str(OLD_DB_PATH))
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users';"
        )
        table_exists = cursor.fetchone() is not None
        assert table_exists, (
            f"Expected table 'users' to exist in {OLD_DB_PATH}, "
            "but it was not found."
        )

        cursor = conn.execute("SELECT COUNT(*) FROM users;")
        row_count = cursor.fetchone()[0]
        assert row_count == 3, (
            f"Table 'users' in {OLD_DB_PATH} should contain 3 rows, "
            f"but found {row_count} rows."
        )
    finally:
        conn.close()


def test_data_directory_does_not_yet_exist():
    """The /home/user/project/data directory must NOT yet exist."""
    assert not DATA_DIR_PATH.exists(), (
        f"Directory {DATA_DIR_PATH} should not exist before migration."
    )


def test_target_database_does_not_yet_exist():
    """The renamed/moved database must not yet exist."""
    assert not TARGET_DB_PATH.exists(), (
        f"Database {TARGET_DB_PATH} should not exist before migration."
    )


def test_migration_log_not_present():
    """No migration log should be present before the task is executed."""
    assert not MIGRATION_LOG_PATH.exists(), (
        f"Migration log {MIGRATION_LOG_PATH} should not exist before migration."
    )