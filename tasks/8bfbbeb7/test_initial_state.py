# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state for the ETL
# disk-usage exercise.  It checks that:
#   • /home/user/etl_data/ exists and is a directory;
#   • its three immediate sub-directories (raw, processed, temp) exist;
#   • each of those sub-directories contains the **expected files** with the
#     exact byte sizes required for the assignment;
#   • the summed byte-size per sub-directory matches the ground-truth values.
#
# The tests purposefully do NOT look for the output file
# /home/user/etl_data_disk_usage.log — that file is supposed to be created by
# the student **after** this initial state is confirmed.

import os
from pathlib import Path

import pytest

ROOT_DIR = Path("/home/user/etl_data")

# Expected structure (file_name, byte_size) for each immediate sub-directory.
EXPECTED_STRUCTURE = {
    "raw": [
        ("raw_1.csv", 1024),
        ("raw_2.csv", 2048),
    ],
    "processed": [
        ("processed_2023-01.parquet", 4096),
    ],
    "temp": [
        ("temp_abc.tmp", 512),
    ],
}

# Derived expected totals (pre-computed to avoid duplication of literals)
EXPECTED_TOTALS = {
    subdir: sum(size for _, size in files)
    for subdir, files in EXPECTED_STRUCTURE.items()
}


def test_root_directory_exists_and_is_dir():
    assert ROOT_DIR.exists(), f"Directory {ROOT_DIR} is missing."
    assert ROOT_DIR.is_dir(), f"{ROOT_DIR} exists but is not a directory."


@pytest.mark.parametrize("subdir_name", ["raw", "processed", "temp"])
def test_subdirectories_exist(subdir_name):
    sub_path = ROOT_DIR / subdir_name
    assert sub_path.exists(), f"Expected sub-directory {sub_path} is missing."
    assert sub_path.is_dir(), f"{sub_path} exists but is not a directory."


@pytest.mark.parametrize(
    "subdir_name, expected_files",
    list(EXPECTED_STRUCTURE.items()),
)
def test_expected_files_exist_with_correct_size(subdir_name, expected_files):
    """
    For each expected file, assert it exists, is a regular file,
    and has the exact byte size specified.
    """
    sub_path = ROOT_DIR / subdir_name
    for file_name, byte_size in expected_files:
        file_path = sub_path / file_name
        assert file_path.exists(), f"Expected file {file_path} is missing."
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."
        actual_size = file_path.stat().st_size
        assert (
            actual_size == byte_size
        ), f"Size mismatch for {file_path}: expected {byte_size} bytes, got {actual_size} bytes."


@pytest.mark.parametrize(
    "subdir_name, expected_total",
    list(EXPECTED_TOTALS.items()),
)
def test_total_byte_size_per_subdirectory(subdir_name, expected_total):
    """
    Confirm that the total size (in bytes) of *immediate* regular files in each
    sub-directory matches the expected truth values.  Nested directories (none
    should exist today) are ignored.
    """
    sub_path = ROOT_DIR / subdir_name
    total = 0
    for child in sub_path.iterdir():
        if child.is_file():
            total += child.stat().st_size
    assert (
        total == expected_total
    ), f"Total size for {sub_path} is {total} bytes; expected {expected_total} bytes."