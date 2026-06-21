# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the learner performs any actions for the “avian flu
# dataset re-organisation” exercise.
#
# It asserts that:
# 1. The two raw CSV files exist in /home/user/raw_data/ with the
#    expected, unaltered single-line contents.
# 2. No target directory or files (including organize.log) are
#    present yet under /home/user/datasets/avian_flu.
#
# Only the Python standard library and pytest are used.

import os
import pytest

# Constants -------------------------------------------------------------------

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "raw_data")
DATASETS_DIR = os.path.join(HOME, "datasets")
TARGET_DIR = os.path.join(DATASETS_DIR, "avian_flu")

RAW_FILES = {
    "avian_flu_cases.csv":   "id,country,date,cases",
    "avian_flu_metadata.csv": "source,contact,email",
}

# Helper ----------------------------------------------------------------------


def full(path_fragment: str) -> str:
    """Return an absolute path under /home/user for readability."""
    return os.path.join(HOME, path_fragment.lstrip("/"))


# Tests -----------------------------------------------------------------------


def test_raw_data_directory_exists_and_is_directory():
    assert os.path.isdir(RAW_DIR), (
        f"Expected raw data directory '{RAW_DIR}' to exist and be a directory."
    )


@pytest.mark.parametrize("filename,expected_content", RAW_FILES.items())
def test_raw_csv_files_exist_with_correct_content(filename, expected_content):
    path = os.path.join(RAW_DIR, filename)
    assert os.path.isfile(path), (
        f"Missing expected CSV file: {path}"
    )

    with open(path, "r", encoding="utf-8") as fh:
        contents = fh.read().strip()
    assert contents == expected_content, (
        f"File '{path}' content mismatch.\n"
        f"Expected single line: {expected_content!r}\n"
        f"Got: {contents!r}"
    )


def test_target_directory_does_not_yet_exist():
    assert not os.path.exists(TARGET_DIR), (
        f"Target directory '{TARGET_DIR}' should NOT exist before the task "
        "is attempted."
    )


@pytest.mark.parametrize("filename", RAW_FILES.keys())
def test_no_csv_files_in_target_directory_yet(filename):
    target_path = os.path.join(TARGET_DIR, filename)
    assert not os.path.exists(target_path), (
        f"File '{target_path}' should NOT exist before the task is attempted."
    )


def test_organize_log_absent():
    log_path = os.path.join(TARGET_DIR, "organize.log")
    assert not os.path.exists(log_path), (
        f"Log file '{log_path}' should NOT exist before the task is attempted."
    )