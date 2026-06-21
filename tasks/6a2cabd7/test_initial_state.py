# test_initial_state.py
#
# This test-suite validates the *starting* filesystem state that must be
# present **before** the student performs any actions for the SQL-backup
# clean-up task.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constant paths                                                              #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
ROOT = HOME / "db_migrations"
BACKUP_LARGE = ROOT / "backup_large"

# Mapping of absolute paths → expected byte sizes
EXPECTED_FILES = {
    ROOT / "2021" / "01_schema_update.sql.bak": 1500,
    ROOT / "2021" / "02_index_update.sql.bak": 900,
    ROOT / "2022" / "03_add_columns.sql.bak": 3000,
    ROOT / "2022" / "temp" / "04_cleanup.sql.bak": 5000,
    ROOT / "2023" / "05_remove_obsolete.sql.bak": 800,
    ROOT / "legacy" / "06_legacy_patch.sql.bak": 2048,
}

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #


def bytes_size(path: Path) -> int:
    """Return the size (in bytes) of *path* as an int."""
    return path.stat().st_size


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #


def test_root_directory_exists():
    assert ROOT.is_dir(), f"Expected directory {ROOT} to exist."


@pytest.mark.parametrize("file_path", list(EXPECTED_FILES.keys()))
def test_expected_file_exists(file_path: Path):
    assert file_path.is_file(), f"Expected file {file_path} to exist."


@pytest.mark.parametrize(
    ("file_path", "expected_size"), list(EXPECTED_FILES.items())
)
def test_expected_file_size_is_correct(file_path: Path, expected_size: int):
    actual_size = bytes_size(file_path)
    msg = (
        f"File {file_path} should be {expected_size} bytes "
        f"but is {actual_size} bytes."
    )
    assert actual_size == expected_size, msg


def test_backup_large_directory_absent():
    """
    The target directory must *not* exist before the student runs the
    clean-up script.  Its presence would indicate a prior run or an
    improperly prepared image.
    """
    assert not BACKUP_LARGE.exists(), (
        f"Directory {BACKUP_LARGE} should NOT exist before the task is run. "
        "Remove it so the student starts from a clean slate."
    )


def test_no_gz_files_present_yet():
    """
    No gzip files should be lurking anywhere under the root tree at start.
    The clean-up job will create them later.
    """
    gz_files = list(ROOT.rglob("*.gz"))
    assert not gz_files, (
        "Found unexpected '.gz' files before the task is executed:\n"
        + "\n".join(str(p) for p in gz_files)
    )


def test_initial_sql_bak_files_intact():
    """
    Ensure every '*.sql.bak' file that is expected to be processed later is
    still in its original location.  None of them should have been moved or
    deleted prior to the student's work.
    """
    for path in EXPECTED_FILES:
        assert path.exists(), f"File {path} is missing; starting state corrupt."


def test_unqualified_files_in_place():
    """
    Confirm that the non-qualifying small files are present so that the
    downstream tests can later verify they were left untouched.
    """
    small_files = {
        ROOT / "2021" / "02_index_update.sql.bak",
        ROOT / "2023" / "05_remove_obsolete.sql.bak",
    }
    for p in small_files:
        assert p.is_file(), f"Small non-qualifying file {p} is missing."