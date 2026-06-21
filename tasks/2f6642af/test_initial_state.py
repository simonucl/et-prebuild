# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# *before* the learner performs any backup action.
#
# What we assert:
#   1. /home/user/production_data exists and is a directory.
#   2. Exactly three files are present inside that directory.
#   3. Each required file exists and contains the expected,
#      byte-for-byte content (including the trailing newline).
#   4. The directory /home/user/backups must *not* exist yet.
#
# If any assertion fails the error message explains what is missing
# or differs from the expected truth.

import os
from pathlib import Path

import pytest

# --- Constants --------------------------------------------------------------

PRODUCTION_DIR = Path("/home/user/production_data")
BACKUPS_DIR = Path("/home/user/backups")

EXPECTED_FILES = {
    PRODUCTION_DIR / "customers.csv": (
        "id,name,email\n"
        "1,Alice,alice@example.com\n"
        "2,Bob,bob@example.com\n"
        "3,Charlie,charlie@example.com\n"
    ),
    PRODUCTION_DIR / "orders.csv": (
        "order_id,customer_id,product,quantity\n"
        "1001,1,Keyboard,2\n"
        "1002,2,Mouse,1\n"
        "1003,3,Monitor,1\n"
    ),
    PRODUCTION_DIR / "README.md": (
        "# Production Data\n"
        "This directory contains the CSV exports used by the sales team.\n"
    ),
}


# --- Helper -----------------------------------------------------------------


def _read_text(path: Path) -> str:
    """Read a UTF-8 file and return its content as str."""
    return path.read_text(encoding="utf-8")


# --- Tests ------------------------------------------------------------------


def test_production_data_directory_exists_and_is_dir():
    assert PRODUCTION_DIR.exists(), (
        f"Required directory {PRODUCTION_DIR} is missing."
    )
    assert PRODUCTION_DIR.is_dir(), (
        f"{PRODUCTION_DIR} exists but is not a directory."
    )


def test_expected_files_present_and_no_extras():
    # Collect actual files (non-directories, non-symlinks) in the directory.
    actual_files = {p for p in PRODUCTION_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_FILES.keys())

    missing = expected_files - actual_files
    extras = actual_files - expected_files

    assert not missing, (
        f"The following required file(s) are missing from {PRODUCTION_DIR}: "
        f"{', '.join(str(p) for p in missing)}"
    )
    assert not extras, (
        f"Unexpected extra file(s) found in {PRODUCTION_DIR}: "
        f"{', '.join(str(p) for p in extras)}"
    )


@pytest.mark.parametrize("file_path, expected_content", EXPECTED_FILES.items())
def test_file_contents_exact_match(file_path: Path, expected_content: str):
    assert file_path.exists(), f"Expected file {file_path} is missing."

    actual_content = _read_text(file_path)
    assert actual_content == expected_content, (
        f"Contents of {file_path} do not match the expected reference text."
    )


def test_backups_directory_absent():
    assert not BACKUPS_DIR.exists(), (
        f"Directory {BACKUPS_DIR} should NOT exist before the backup task runs."
    )