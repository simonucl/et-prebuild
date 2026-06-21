# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student performs any action.  It intentionally does NOT check for
# the presence (or absence) of the artefacts that the student will be
# asked to create later (e.g., the backup tarball or its log file).
#
# What we *do* verify:
#   • /home/user/credentials/ directory exists.
#   • /home/user/credentials/db_creds.txt exists and contains the expected
#     “username=” and “password=” lines.
#   • /home/user/credentials/api_key.txt exists and contains an “API_KEY=”.
#   • /home/user/backup/ directory exists.
#
# Only stdlib + pytest are used, as required.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
CREDENTIALS_DIR = HOME / "credentials"
BACKUP_DIR = HOME / "backup"

DB_CREDS_FILE = CREDENTIALS_DIR / "db_creds.txt"
API_KEY_FILE = CREDENTIALS_DIR / "api_key.txt"


def _read_text(path: Path) -> str:
    """Helper that returns the full text content of *path*."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


@pytest.mark.describe("Initial directory structure is present")
def test_credentials_directory_exists():
    assert CREDENTIALS_DIR.is_dir(), (
        f"Expected directory {CREDENTIALS_DIR} does not exist. "
        "The credentials directory must be in place before starting the task."
    )


@pytest.mark.describe("Backup directory is present")
def test_backup_directory_exists():
    assert BACKUP_DIR.is_dir(), (
        f"Expected directory {BACKUP_DIR} does not exist. "
        "Create it (mkdir -p /home/user/backup) before attempting the task."
    )


@pytest.mark.describe("Credential files exist with plausible content")
def test_db_creds_file_exists_and_contains_expected_markers():
    assert DB_CREDS_FILE.is_file(), (
        f"Expected credential file {DB_CREDS_FILE} is missing."
    )

    text = _read_text(DB_CREDS_FILE)
    missing_markers = [marker for marker in ("username=", "password=") if marker not in text]
    assert not missing_markers, (
        f"{DB_CREDS_FILE} is missing the following expected marker(s): "
        + ", ".join(missing_markers)
    )


def test_api_key_file_exists_and_contains_marker():
    assert API_KEY_FILE.is_file(), (
        f"Expected credential file {API_KEY_FILE} is missing."
    )

    text = _read_text(API_KEY_FILE)
    assert "API_KEY=" in text, (
        f"{API_KEY_FILE} does not contain the expected 'API_KEY=' line."
    )