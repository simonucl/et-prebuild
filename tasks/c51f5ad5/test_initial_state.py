# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state is
# exactly as described in the exercise BEFORE the student performs any
# cleaning.  If any of the assertions fail the environment is not in
# the expected “messy” condition and the subsequent grading of the
# student’s work would be unreliable.

from pathlib import Path
import pytest

HOME = Path("/home/user")
RAW_ROOT = HOME / "workspace" / "raw_data"
REPORT_FILE = HOME / "workspace" / "cleaning_report.txt"


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _full_paths(root: Path, relative_paths):
    """Return a list of Path objects given a root and iterable of str."""
    return [root / rel for rel in relative_paths]


# ----------------------------------------------------------------------
# Expected artefacts in the *initial* tree
# ----------------------------------------------------------------------
BACKUP_FILES_REL = [
    "customer_data_2020.csv.bak",
    "old_notes.txt~",
    "logs/error.log~",
    "logs/debug.log~",
    "archive/old/legacy_data.csv.bak",
    "archive/old/placeholder.txt~",
]

CSV_FILES_REL = [
    "customer_data_2020.csv",
    "product_data_2021.csv",
    "sales_Q4_2021.csv",
]

EMPTY_DIRS_REL = [
    "archive/old/empty_dir",
    "archive/zip",
]

NON_EMPTY_DIRS_REL = [
    "logs",
    "archive",
    "archive/old",
    "duplicates",
]

OTHER_FILES_REL = [
    "README.md",
    "logs/usage.log",
    "duplicates/duplicates_readme.txt",
]


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_root_directory_exists():
    assert RAW_ROOT.is_dir(), (
        f"Expected directory {RAW_ROOT} does not exist. "
        "The entire test suite relies on this path."
    )


def test_expected_backup_files_present_and_count():
    expected_paths = _full_paths(RAW_ROOT, BACKUP_FILES_REL)

    # 1. Every listed file must exist.
    for p in expected_paths:
        assert p.is_file(), f"Required backup file missing: {p}"

    # 2. No extra *.bak or *~ files should be present.
    found_backup_files = [
        p for p in RAW_ROOT.rglob("*")
        if p.is_file() and (p.name.endswith(".bak") or p.name.endswith("~"))
    ]
    assert len(found_backup_files) == len(BACKUP_FILES_REL), (
        "The number of '.bak' and '~' files in the initial tree is incorrect.\n"
        f"Expected {len(BACKUP_FILES_REL)}, found {len(found_backup_files)}.\n"
        "List of found files:\n" + "\n".join(str(p) for p in found_backup_files)
    )


def test_expected_csv_files_present_and_uncompressed():
    expected_paths = _full_paths(RAW_ROOT, CSV_FILES_REL)

    for p in expected_paths:
        assert p.is_file(), f"Required CSV file missing: {p}"

    # Verify NO *.csv.gz files yet.
    gz_files = list(RAW_ROOT.rglob("*.csv.gz"))
    assert not gz_files, (
        "Compressed CSV files (*.csv.gz) already exist in the initial state, "
        "but they should only appear after the student performs the cleanup.\n"
        "Found:\n" + "\n".join(str(p) for p in gz_files)
    )

    # Verify the count of uncompressed CSVs is exactly 3.
    found_csv_files = [
        p for p in RAW_ROOT.rglob("*.csv")
        if not p.name.endswith(".bak")  # exclude backup CSVs
    ]
    assert len(found_csv_files) == len(CSV_FILES_REL), (
        "Unexpected number of '*.csv' (non-back-up) files in initial state.\n"
        f"Expected {len(CSV_FILES_REL)}, found {len(found_csv_files)}.\n"
        "List of found files:\n" + "\n".join(str(p) for p in found_csv_files)
    )


def test_empty_directories_exist_and_are_empty():
    for rel in EMPTY_DIRS_REL:
        dir_path = RAW_ROOT / rel
        assert dir_path.is_dir(), f"Expected empty dir missing: {dir_path}"
        # directory is considered empty if it contains no entries at all
        contents = list(dir_path.iterdir())
        assert not contents, (
            f"Directory {dir_path} was expected to be empty but contains:\n"
            + "\n".join(str(p) for p in contents)
        )


def test_non_empty_directories_exist():
    for rel in NON_EMPTY_DIRS_REL:
        dir_path = RAW_ROOT / rel
        assert dir_path.is_dir(), f"Required directory missing: {dir_path}"
        contents = list(dir_path.iterdir())
        assert contents, f"Directory {dir_path} was expected to be non-empty."


def test_other_important_files_present():
    for rel in OTHER_FILES_REL:
        p = RAW_ROOT / rel
        assert p.is_file(), f"Required file missing: {p}"


def test_no_cleaning_report_yet():
    assert not REPORT_FILE.exists(), (
        f"The cleaning report {REPORT_FILE} already exists, but it should "
        "only be created by the student’s solution."
    )