# test_initial_state.py
#
# Pytest suite that validates the expected **initial** filesystem state
# before the student executes the required compound command.

import os
from pathlib import Path

HOME = Path("/home/user")

DB_SCRIPTS_DIR = HOME / "db_scripts"
BACKUPS_DIR = HOME / "backups"
LOGS_DIR = HOME / "backup_logs"

ARCHIVE_PATH = BACKUPS_DIR / "db_scripts_backup_20231015.tar.gz"
LOG_FILE_PATH = LOGS_DIR / "backup_status.log"

SCHEMA_SQL = DB_SCRIPTS_DIR / "schema.sql"
OPTIMIZE_SQL = DB_SCRIPTS_DIR / "optimize_queries.sql"

EXPECTED_DB_SCRIPTS_FILES = {
    SCHEMA_SQL.name: "-- Schema definition placeholder\n",
    OPTIMIZE_SQL.name: "-- Query optimization placeholder\n",
}


def _read_text(path):
    """
    Utility: read file contents as text with universal newlines.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def test_db_scripts_directory_exists_and_has_only_expected_files():
    assert DB_SCRIPTS_DIR.exists(), f"Missing directory: {DB_SCRIPTS_DIR}"
    assert DB_SCRIPTS_DIR.is_dir(), f"{DB_SCRIPTS_DIR} exists but is not a directory"

    actual_files = sorted(p.name for p in DB_SCRIPTS_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_DB_SCRIPTS_FILES.keys())
    assert (
        actual_files == expected_files
    ), f"{DB_SCRIPTS_DIR} must contain exactly {expected_files}, found {actual_files}"

    # Ensure no sub-directories are present
    subdirs = [p.name for p in DB_SCRIPTS_DIR.iterdir() if p.is_dir()]
    assert (
        not subdirs
    ), f"{DB_SCRIPTS_DIR} must not contain sub-directories; found {subdirs}"


def test_db_scripts_file_contents_are_placeholders():
    for filename, expected_content in EXPECTED_DB_SCRIPTS_FILES.items():
        path = DB_SCRIPTS_DIR / filename
        assert path.exists(), f"Expected file missing: {path}"
        actual_content = _read_text(path)
        assert (
            actual_content == expected_content
        ), f"File {path} has unexpected content.\nExpected: {repr(expected_content)}\nFound:    {repr(actual_content)}"


def test_backups_directory_exists_and_is_empty():
    assert BACKUPS_DIR.exists(), f"Missing directory: {BACKUPS_DIR}"
    assert BACKUPS_DIR.is_dir(), f"{BACKUPS_DIR} exists but is not a directory"

    entries = [p.name for p in BACKUPS_DIR.iterdir()]
    assert (
        not entries
    ), f"{BACKUPS_DIR} must be empty before the backup is created; found: {entries}"


def test_backup_logs_directory_exists_and_is_empty():
    assert LOGS_DIR.exists(), f"Missing directory: {LOGS_DIR}"
    assert LOGS_DIR.is_dir(), f"{LOGS_DIR} exists but is not a directory"

    entries = [p.name for p in LOGS_DIR.iterdir()]
    assert (
        not entries
    ), f"{LOGS_DIR} must be empty before the backup is created; found: {entries}"


def test_no_archive_or_log_file_yet():
    assert (
        not ARCHIVE_PATH.exists()
    ), f"Backup archive {ARCHIVE_PATH} should NOT exist before the command is run"
    assert (
        not LOG_FILE_PATH.exists()
    ), f"Log file {LOG_FILE_PATH} should NOT exist before the command is run"