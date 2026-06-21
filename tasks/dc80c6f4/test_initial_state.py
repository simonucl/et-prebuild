# test_initial_state.py
#
# Pytest suite that verifies the filesystem *before* the student runs
# their “backup-isolation” script.  All assertions reflect the truth
# described in the task statement and must pass **prior** to any
# student action.

from pathlib import Path
import os
import subprocess
import pytest

HOME                = Path("/home/user")
DATASETS            = HOME / "datasets"
RAW                 = DATASETS / "raw"
OLD                 = RAW / "old"
ARCHIVE             = RAW / "archive"
BACKUP_DIR          = DATASETS / "backup"
CLEANUP_LOGS_DIR    = DATASETS / "cleanup_logs"

# ---------- Paths that MUST exist ----------

EXPECTED_BACKUP_FILES = {
    RAW / "sales_backup.csv",
    OLD / "sales_jan_backup.csv",
    OLD / "customers_backup.csv",
    ARCHIVE / "2021_sales_backup.csv",
}

EXPECTED_NON_BACKUP_FILES = {
    RAW / "sales_jan.csv",
    RAW / "sales_feb.csv",
    RAW / "customers.csv",
    RAW / "readme.txt",
}

# ---------- Helpers ----------

def find_paths(base: Path, pattern: str):
    """Return a set of absolute Paths matching the glob *pattern* under *base*."""
    return {p.resolve() for p in base.rglob(pattern) if p.is_file()}


# ---------- Tests ----------

def test_required_directories_exist():
    for path in (DATASETS, RAW, OLD, ARCHIVE):
        assert path.is_dir(), f"Missing required directory: {path}"


def test_unexpected_directories_absent():
    assert not BACKUP_DIR.exists(), (
        f"Directory {BACKUP_DIR} should NOT exist before the student runs their script"
    )
    assert not CLEANUP_LOGS_DIR.exists(), (
        f"Directory {CLEANUP_LOGS_DIR} should NOT exist before the student runs their script"
    )


def test_expected_backup_files_exist():
    for path in EXPECTED_BACKUP_FILES:
        assert path.is_file(), f"Expected backup file is missing: {path}"


def test_expected_non_backup_files_exist():
    for path in EXPECTED_NON_BACKUP_FILES:
        assert path.is_file(), f"Expected non-backup file is missing: {path}"


def test_no_extra_backup_csv_files_exist():
    """Exactly the four declared *_backup.csv files must exist under the raw tree."""
    found = find_paths(RAW, "*_backup.csv")
    assert found == EXPECTED_BACKUP_FILES, (
        "Unexpected set of *_backup.csv files found under /home/user/datasets/raw.\n"
        f"Found: {sorted(map(str, found))}\n"
        f"Expected: {sorted(map(str, EXPECTED_BACKUP_FILES))}"
    )


def test_no_gzipped_backups_exist_yet():
    gz_files = find_paths(DATASETS, "*.csv.gz")
    assert not gz_files, (
        "No .csv.gz files should exist before the student processes the data.\n"
        f"Found: {sorted(map(str, gz_files))}"
    )


def test_non_backup_files_untouched():
    """
    Ensure there are no accidental duplicate compressed or backup versions
    of the non-backup CSVs.
    """
    forbidden_patterns = ["sales_jan.csv.gz", "sales_feb.csv.gz", "customers.csv.gz"]
    for pattern in forbidden_patterns:
        matches = find_paths(DATASETS, pattern)
        assert not matches, (
            f"Did not expect to find any pre-existing '{pattern}' files, "
            f"but found: {sorted(map(str, matches))}"
        )


def test_no_cleanup_log_exists_yet():
    log_path = CLEANUP_LOGS_DIR / "backup_move.log"
    assert not log_path.exists(), (
        f"Log file {log_path} should NOT exist before the student starts the task"
    )


def test_find_command_output_matches_expectation():
    """
    Validate the shell `find` view of *_backup.csv files to ensure the
    teaching instructions that require a find/xargs pipeline are feasible.
    """
    result = subprocess.run(
        ["find", str(RAW), "-type", "f", "-name", "*_backup.csv", "-print0"],
        check=True,
        stdout=subprocess.PIPE,
        text=False,
    )
    # Split the NUL-delimited list into Path objects (strip trailing empty)
    found = {
        Path(p.decode()).resolve()
        for p in result.stdout.split(b"\0") if p
    }
    assert found == EXPECTED_BACKUP_FILES, (
        "Shell find detected an unexpected set of *_backup.csv files.\n"
        f"Found: {sorted(map(str, found))}\n"
        f"Expected: {sorted(map(str, EXPECTED_BACKUP_FILES))}"
    )