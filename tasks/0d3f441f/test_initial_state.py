# test_initial_state.py
#
# Pytest suite that validates the **initial** on-disk state *before* the
# student runs any commands for the “data-pipeline prototype” exercise.
#
# What we check:
# 1. /home/user/projects/raw_data/ exists and is a directory.
# 2. raw_data/ contains **exactly** the four expected CSV files and nothing else.
# 3. Each expected file exists and is a regular file.
# 4. /home/user/projects/processed/              MUST NOT exist yet.
# 5. /home/user/projects/processing.log          MUST NOT exist yet.
#
# Any deviation from the above means the starting environment is not in the
# correct “clean slate” that the exercise expects.

from pathlib import Path
import os
import stat
import pytest

PROJECT_ROOT = Path("/home/user/projects")
RAW_DATA_DIR = PROJECT_ROOT / "raw_data"
PROCESSED_DIR = PROJECT_ROOT / "processed"
LOG_FILE      = PROJECT_ROOT / "processing.log"

EXPECTED_RAW_FILES = {
    "sales_2023.csv",
    "inventory_2022.csv",
    "finance_2023.csv",
    "broken.csv",
}

def _is_regular_file(path: Path) -> bool:
    """Return True if 'path' exists and is a regular file (not dir, symlink, etc.)."""
    try:
        st = path.lstat()  # do not follow links (shouldn’t be any)
    except FileNotFoundError:
        return False
    return stat.S_ISREG(st.st_mode)


def test_raw_data_directory_exists():
    assert RAW_DATA_DIR.exists(), (
        f"Directory missing: {RAW_DATA_DIR}. The starting state must contain "
        "the raw_data directory."
    )
    assert RAW_DATA_DIR.is_dir(), f"{RAW_DATA_DIR} exists but is not a directory."


def test_raw_data_contains_exact_expected_files():
    present_files = {p.name for p in RAW_DATA_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_RAW_FILES - present_files
    unexpected = present_files - EXPECTED_RAW_FILES

    assert not missing, (
        "The raw_data directory is missing the following required file(s): "
        f"{', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "The raw_data directory contains unexpected extra file(s): "
        f"{', '.join(sorted(unexpected))}"
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_RAW_FILES))
def test_each_expected_file_is_regular(filename):
    path = RAW_DATA_DIR / filename
    assert _is_regular_file(path), (
        f"Expected a regular file at {path}, but it is either missing or not a "
        "regular file."
    )


def test_processed_directory_does_not_exist_yet():
    assert not PROCESSED_DIR.exists(), (
        f"{PROCESSED_DIR} already exists, but it should be created by the "
        "student’s solution as part of the task."
    )


def test_processing_log_does_not_exist_yet():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it must be created fresh by the "
        "student’s solution."
    )