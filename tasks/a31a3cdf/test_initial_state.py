# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating-system before
# the student runs any commands.  It checks only for the prerequisites and
# explicitly avoids testing for any files that the student is expected to
# create later.

import os
from pathlib import Path

HOME = Path("/home/user")
BACKUPS_DIR = HOME / "backups"
CSV_FILE = BACKUPS_DIR / "backup_report.csv"

# --------------------------------------------------------------------------- #
# Helper: The exact content that must already be present inside               #
#         /home/user/backups/backup_report.csv (including the final newline). #
# --------------------------------------------------------------------------- #
EXPECTED_CSV_CONTENT = (
    "BackupID,Date,Status,SizeMB\n"
    "BKP001,2023-07-01,OK,512\n"
    "BKP002,2023-07-02,OK,514\n"
    "BKP003,2023-07-03,FAILED,0\n"
    "BKP004,2023-07-04,OK,518\n"
    "BKP005,2023-07-05,OK,520\n"
)


def test_backups_directory_exists_and_is_directory():
    """
    /home/user/backups must exist and be a directory before the student starts.
    """
    assert BACKUPS_DIR.exists(), (
        f"Required directory {BACKUPS_DIR} does not exist. "
        "Create it before proceeding."
    )
    assert BACKUPS_DIR.is_dir(), (
        f"{BACKUPS_DIR} exists but is not a directory. "
        "It must be a directory."
    )


def test_backup_report_csv_exists():
    """
    backup_report.csv must already be present inside /home/user/backups/.
    """
    assert CSV_FILE.exists(), (
        f"Expected file {CSV_FILE} is missing. "
        "The initial backup report CSV must be provided."
    )
    assert CSV_FILE.is_file(), (
        f"{CSV_FILE} exists but is not a regular file. "
        "It must be a regular text file."
    )


def test_backup_report_csv_content_is_exact():
    """
    The content of backup_report.csv must match the exact specification,
    including the trailing newline on the last line.
    """
    actual = CSV_FILE.read_text(encoding="utf-8")
    assert actual == EXPECTED_CSV_CONTENT, (
        "The content of backup_report.csv does not match the expected initial "
        "state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{actual!r}\n"
        "Ensure the file is created exactly as specified, including the final "
        "newline character."
    )