# test_initial_state.py
#
# This pytest file validates that the *initial* filesystem state required
# for the “backup overview” task is present **before** the student begins
# working.  It deliberately avoids looking for any result/output files
# the student is supposed to create later.

from pathlib import Path
import pytest

# Constants -------------------------------------------------------------------

BACKUPS_DIR = Path("/home/user/backups")
CSV_PATH = BACKUPS_DIR / "all_backups.csv"

EXPECTED_CSV_LINES = [
    "backup_id,db_name,timestamp,size_mb,compressed_size_mb,checksum",
    "bkp-20240101-pg,customerdb,2024-01-01T02:05:00Z,10240,2048,a1b2c3d4",
    "bkp-20240102-mysql,ordersdb,2024-01-02T03:10:00Z,5120,1024,b2c3d4e5",
    "bkp-20240103-pg,inventorydb,2024-01-03T01:55:00Z,20480,4096,c3d4e5f6",
    "bkp-20240104-mysql,analyticsdb,2024-01-04T04:20:00Z,102400,20480,d4e5f6g7",
]

# Tests -----------------------------------------------------------------------


def test_backups_directory_exists_and_is_directory():
    assert BACKUPS_DIR.exists(), (
        f"Required directory {BACKUPS_DIR} is missing. "
        "Create it or adjust the path."
    )
    assert BACKUPS_DIR.is_dir(), (
        f"{BACKUPS_DIR} exists but is not a directory."
    )


def test_csv_file_exists_and_is_regular_file():
    assert CSV_PATH.exists(), (
        f"Required CSV file {CSV_PATH} is missing."
    )
    assert CSV_PATH.is_file(), (
        f"{CSV_PATH} exists but is not a regular file."
    )


def test_csv_file_contents_are_exact():
    """
    Verify that /home/user/backups/all_backups.csv contains exactly the six
    expected lines (header + 4 data rows) with LF line endings and no extra
    blank lines.
    """
    raw = CSV_PATH.read_text(encoding="utf-8")
    assert raw.endswith("\n"), (
        f"{CSV_PATH} must end with a single LF newline."
    )

    lines = raw.splitlines()
    assert lines == EXPECTED_CSV_LINES, (
        "The contents of all_backups.csv do not match the expected seed data.\n"
        "Differences:\n"
        f"Expected:\n{EXPECTED_CSV_LINES!r}\n\nActual:\n{lines!r}"
    )