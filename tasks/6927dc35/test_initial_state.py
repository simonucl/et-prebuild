# test_initial_state.py
"""
Pytest suite that validates the initial, pre-task filesystem state.

This file MUST be executed before the student attempts the assignment.
It checks only the pre-existing inputs and makes no assertions about any
artifacts the student is expected to create later.
"""

import os
from pathlib import Path

DATA_DIR = Path("/home/user/data")
FILELIST = Path("/home/user/filelist.txt")


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), f"Expected directory {DATA_DIR} to exist."


def test_expected_files_and_sizes():
    """
    Validate the three seed files and their approximate sizes.
    The ranges include a little slack to accommodate minor tooling
    differences when the fixtures were generated.
    """
    files_expected = {
        "big1.txt": (1_400_000, 1_600_000),  # ≈1.5 MiB
        "big2.log": (1_600_000, 1_800_000),  # ≈1.7 MiB
        "small.txt": (0, 10_000),            # ≈5 KiB
    }

    for filename, (low, high) in files_expected.items():
        full_path = DATA_DIR / filename
        assert full_path.is_file(), f"Missing required file: {full_path}"
        size = full_path.stat().st_size
        assert low <= size <= high, (
            f"{full_path} size {size} bytes out of expected range "
            f"{low}–{high} bytes."
        )


def test_missing_doc_absent():
    missing = DATA_DIR / "missing.doc"
    assert not missing.exists(), (
        f"{missing} should not exist in the initial state; it is purposely "
        "absent to test error handling."
    )


def test_filelist_contents():
    assert FILELIST.is_file(), f"Required file list {FILELIST} is missing."

    with FILELIST.open("r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    # Strip only the trailing newline and validate exact paths remain.
    lines = [ln.rstrip("\n") for ln in raw_lines]

    expected_lines = [
        "/home/user/data/big1.txt",
        "/home/user/data/big2.log",
        "/home/user/data/missing.doc",
    ]

    assert lines == expected_lines, (
        "Contents of filelist.txt do not match the expected paths.\n"
        f"Expected lines:\n{expected_lines}\nFound lines:\n{lines}"
    )