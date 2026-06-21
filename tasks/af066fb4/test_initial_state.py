# test_initial_state.py
#
# Pytest suite that validates the *starting* filesystem state for the
# “FinOps archive” exercise.  These checks run **before** the student
# performs any work, so they purposely do NOT look for the deliverables
# that the student will create later on.  Instead, they verify that the
# required source CSVs are present and correct, and that none of the
# output artefacts already exist.

import os
import pytest

HOME = "/home/user"
BILLING_DIR = os.path.join(HOME, "billing_data")
BACKUPS_DIR = os.path.join(HOME, "backups")

CSV_FILES = [
    "monthly_2023-07.csv",
    "monthly_2023-08.csv",
    "monthly_2023-09.csv",
]

HEADER_LINE = "CostCenter,Service,UsageHours,CostUSD"


@pytest.mark.parametrize("csv_name", CSV_FILES)
def test_csv_exists_is_file_and_size_is_102(csv_name):
    """
    Each CSV must exist as a regular file and be exactly 102 bytes long.
    """
    path = os.path.join(BILLING_DIR, csv_name)
    assert os.path.isfile(path), f"Expected file {path!r} to exist."
    size = os.path.getsize(path)
    assert size == 102, (
        f"File {path!r} should be 102 bytes, but is {size} bytes."
    )


@pytest.mark.parametrize("csv_name", CSV_FILES)
def test_csv_first_line_is_expected_header(csv_name):
    """
    Sanity-check that the first line of each CSV is the expected header.
    (Stripped so we don’t depend on newline style.)
    """
    path = os.path.join(BILLING_DIR, csv_name)
    with open(path, "r", encoding="utf-8") as fh:
        first_line = fh.readline().rstrip("\r\n")
    assert first_line == HEADER_LINE, (
        f"The header of {path!r} is wrong or the file is corrupted."
    )


@pytest.mark.parametrize("csv_name", CSV_FILES)
def test_csv_is_world_readable(csv_name):
    """
    The source data should be readable by any non-root user (mode 0644 or
    looser).  This is important so that the student job can read them.
    """
    path = os.path.join(BILLING_DIR, csv_name)
    mode = os.stat(path).st_mode & 0o777
    assert mode & 0o004, (
        f"File {path!r} must be world-readable (mode 0644 or similar). "
        f"Current mode: {oct(mode)}"
    )


def test_no_deliverables_exist_yet():
    """
    None of the files the student is supposed to create should already be
    present.  If they exist, the starting environment is dirty.
    """
    targets = [
        os.path.join(BACKUPS_DIR, "billing_backup_2023Q3.tar.gz"),
        os.path.join(BACKUPS_DIR, "billing_backup_2023Q3.sha256"),
        os.path.join(BACKUPS_DIR, "backup_report.log"),
    ]
    for path in targets:
        assert not os.path.exists(
            path
        ), f"Deliverable {path!r} already exists; starting state should be clean."


def test_backups_directory_absent_or_empty():
    """
    The /home/user/backups directory should not exist yet.  If it does
    (e.g., from a previous failed run), it must be completely empty so
    that the student starts from a clean slate.
    """
    if not os.path.exists(BACKUPS_DIR):
        pytest.skip(f"{BACKUPS_DIR!r} does not exist yet — this is fine.")
    assert os.path.isdir(
        BACKUPS_DIR
    ), f"{BACKUPS_DIR!r} exists but is not a directory."

    leftover = os.listdir(BACKUPS_DIR)
    assert (
        len(leftover) == 0
    ), f"{BACKUPS_DIR!r} is supposed to be empty at start, but contains: {leftover}"