# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student
# runs any command.  It asserts that the datasets/ directory tree
# is exactly in the “Initial situation” specified in the task
# description.

from pathlib import Path
import pytest

HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"
RAW_DIR = DATASETS_DIR / "raw"
CLEAN_DIR = DATASETS_DIR / "clean"
LOG_FILE = DATASETS_DIR / "cleaning.log"

EXPECTED_CSV_FILES = {
    "customers.csv",
    "inventory.csv",
    "products.csv",
    "sales.csv",
}
EXPECTED_JSON_FILES = {
    "notes.json",
}
EXPECTED_RAW_FILES = EXPECTED_CSV_FILES | EXPECTED_JSON_FILES


def _file_set(directory: Path):
    """
    Helper that returns a set with the names of regular files
    directly contained in `directory`.
    """
    return {p.name for p in directory.iterdir() if p.is_file()}


def test_raw_directory_exists_with_correct_files():
    """`raw/` must exist and contain exactly the five expected files."""
    assert RAW_DIR.exists(), f"Missing directory: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory"

    actual_files = _file_set(RAW_DIR)
    assert actual_files == EXPECTED_RAW_FILES, (
        f"{RAW_DIR} must contain exactly {sorted(EXPECTED_RAW_FILES)}, "
        f"but currently contains {sorted(actual_files)}"
    )

    # All files should be non-empty.
    for filename in EXPECTED_RAW_FILES:
        filepath = RAW_DIR / filename
        size = filepath.stat().st_size
        assert size > 0, f"File {filepath} is empty (size 0 bytes)"


def test_clean_directory_exists_and_is_empty():
    """`clean/` must exist and be completely empty at the start."""
    assert CLEAN_DIR.exists(), f"Missing directory: {CLEAN_DIR}"
    assert CLEAN_DIR.is_dir(), f"{CLEAN_DIR} exists but is not a directory"

    contents = list(CLEAN_DIR.iterdir())
    assert contents == [], (
        f"{CLEAN_DIR} is expected to be empty at the beginning, "
        f"but currently contains: {[p.name for p in contents]}"
    )


def test_cleaning_log_does_not_yet_exist():
    """The log file must not exist before the student runs their command."""
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} already exists, but it should be created "
        "only after the CSV files are moved."
    )


def test_no_extra_subdirectories():
    """
    Ensure there are no unexpected extra subdirectories inside
    `/home/user/datasets/`.
    """
    allowed_dirs = {"raw", "clean"}
    actual_dirs = {p.name for p in DATASETS_DIR.iterdir() if p.is_dir()}
    assert actual_dirs.issuperset(allowed_dirs), (
        f"{DATASETS_DIR} must contain the directories {sorted(allowed_dirs)}. "
        f"Currently present directories: {sorted(actual_dirs)}"
    )