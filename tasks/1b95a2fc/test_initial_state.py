# test_initial_state.py
#
# Pytest suite that validates the ORIGINAL filesystem state
# before the student performs any actions.  It checks only the
# provided, pre-existing resources and deliberately ignores every
# path that the student is expected to create or modify later.
#
# Requirements verified:
#   • /home/user/datasets/           must exist and be a directory
#   • /home/user/datasets/raw/       must exist and be a directory
#   • Exactly two CSV files           data1.csv, data2.csv
#   • Each CSV file                   must have octal mode 644
#   • The byte-for-byte contents      must match the specification
#
# NOTE: We DO NOT test for any of the “output” artefacts such as
# /home/user/datasets/clean/ or /home/user/clean_dataset.log
# because those will be produced by the student.


import os
from pathlib import Path
import stat
import pytest


HOME = Path("/home/user")
DATASETS_DIR = HOME / "datasets"
RAW_DIR = DATASETS_DIR / "raw"

EXPECTED_RAW_FILES = {
    "data1.csv": (
        "id,value\n"
        "1,23\n"
        "2,\n"
        "3,45\n"
    ),
    "data2.csv": (
        "id,value,score\n"
        "1,10,0.5\n"
        "2,,0.7\n"
        "3,12,\n"
    ),
}


def octal_mode(path: Path) -> str:
    """Return the final 3-digit octal permission string of a path."""
    return oct(os.stat(path).st_mode & 0o777)[-3:]


def test_directories_present_and_correct_type():
    assert DATASETS_DIR.exists(), f"Missing directory: {DATASETS_DIR}"
    assert DATASETS_DIR.is_dir(), f"{DATASETS_DIR} exists but is not a directory"

    assert RAW_DIR.exists(), f"Missing directory: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory"


def test_exact_raw_csv_files_present():
    raw_files = {p.name for p in RAW_DIR.glob("*.csv")}
    assert raw_files == set(EXPECTED_RAW_FILES), (
        f"CSV files under {RAW_DIR} do not match specification.\n"
        f"Expected: {sorted(EXPECTED_RAW_FILES)}\n"
        f"Found   : {sorted(raw_files)}"
    )


@pytest.mark.parametrize("filename, expected_content", EXPECTED_RAW_FILES.items())
def test_raw_csv_file_permissions_and_contents(filename, expected_content):
    file_path = RAW_DIR / filename
    assert file_path.exists(), f"Expected file is missing: {file_path}"
    assert file_path.is_file(), f"Path exists but is not a file: {file_path}"

    # Check permissions – initial state must be exactly 644
    mode = octal_mode(file_path)
    assert mode == "644", (
        f"File {file_path} has wrong permissions {mode}; "
        f"expected 644 (rw-r--r--)"
    )

    # Check byte-for-byte contents
    actual_content = file_path.read_text(encoding="utf-8")
    assert actual_content == expected_content, (
        f"Contents of {file_path} do not match the expected initial data."
    )