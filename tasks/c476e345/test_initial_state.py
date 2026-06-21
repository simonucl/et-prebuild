# test_initial_state.py
#
# This pytest suite validates the **initial** on-disk state that must be
# present before the student begins the shell exercise.  It deliberately
# avoids checking for any *result* artefacts (e.g. cleaned_files.log) and
# focuses solely on the raw data tree that the student is asked to clean.

import os
from pathlib import Path

import pytest

RAW_ROOT = Path("/home/user/projects/data/raw")

# --------------------------------------------------------------------------- #
# Helper data structures describing the ground-truth initial dataset layout
# --------------------------------------------------------------------------- #

YEARS = {
    "2020": {
        "csv":  ("q1_sales.csv",),
        "bak":  ("q1_sales.csv.bak",),
        "zero": ("empty.csv",),
        "other": ("README.txt",),
    },
    "2021": {
        "csv":  ("q2_sales.csv",),
        "bak":  ("q2_sales.csv.bak",),
        "zero": ("empty.csv",),
        "other": (".hidden",),
    },
    "2022": {
        "csv":  ("q3_sales.csv",),
        "bak":  ("q3_sales.csv.bak",),
        "zero": ("empty.csv",),
        "other": (),
    },
}

# --------------------------------------------------------------------------- #
# Generic helpers
# --------------------------------------------------------------------------- #


def assert_exists(path: Path, msg: str = ""):
    assert path.exists(), msg or f"Expected {path} to exist"


def assert_file_size(path: Path, expected_size: int):
    actual_size = path.stat().st_size
    assert actual_size == expected_size, (
        f"Expected {path} to be {expected_size} bytes, "
        f"but it is {actual_size} bytes"
    )


def assert_file_nonempty(path: Path):
    assert path.stat().st_size > 0, f"Expected {path} to be non-empty"


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_raw_root_exists_and_is_directory():
    assert RAW_ROOT.is_dir(), f"{RAW_ROOT} should exist and be a directory"


def test_exact_year_directories_present():
    expected_year_dirs = {RAW_ROOT / year for year in YEARS}
    actual_year_dirs = {p for p in RAW_ROOT.iterdir() if p.is_dir()}
    assert actual_year_dirs == expected_year_dirs, (
        "Year directories under {RAW_ROOT} do not match expectation.\n"
        f"Expected: {sorted(map(str, expected_year_dirs))}\n"
        f"Found:    {sorted(map(str, actual_year_dirs))}"
    )


@pytest.mark.parametrize("year", YEARS.keys())
def test_expected_files_for_each_year(year):
    year_dir = RAW_ROOT / year
    expected = YEARS[year]

    # Check CSVs (non-empty)
    for fname in expected["csv"]:
        fpath = year_dir / fname
        assert_exists(fpath, f"Missing non-empty CSV file: {fpath}")
        assert_file_nonempty(fpath)

    # Check .bak files (non-empty)
    for fname in expected["bak"]:
        fpath = year_dir / fname
        assert_exists(fpath, f"Missing .bak file: {fpath}")
        assert_file_nonempty(fpath)

    # Check zero-byte CSV files
    for fname in expected["zero"]:
        fpath = year_dir / fname
        assert_exists(fpath, f"Missing zero-byte CSV file: {fpath}")
        assert_file_size(fpath, 0)

    # Check other miscellaneous files
    for fname in expected["other"]:
        fpath = year_dir / fname
        assert_exists(fpath, f"Missing ancillary file: {fpath}")
        # No size check; they may be empty or not.


def test_no_extra_bak_or_zero_byte_csv_files():
    """
    Guard against unexpected additional files.  There must be:
    • exactly three '.bak' files
    • exactly three zero-byte '.csv' files
    across the entire raw tree.
    """
    bak_files = [p for p in RAW_ROOT.rglob("*.bak") if p.is_file()]
    zero_csv_files = [
        p for p in RAW_ROOT.rglob("*.csv")
        if p.is_file() and p.stat().st_size == 0
    ]

    expected_bak_paths = {
        RAW_ROOT / year / YEARS[year]["bak"][0] for year in YEARS
    }
    expected_zero_csv_paths = {
        RAW_ROOT / year / YEARS[year]["zero"][0] for year in YEARS
    }

    assert set(bak_files) == expected_bak_paths, (
        "The set of '.bak' files is not exactly as expected.\n"
        f"Expected: {sorted(map(str, expected_bak_paths))}\n"
        f"Found:    {sorted(map(str, bak_files))}"
    )

    assert set(zero_csv_files) == expected_zero_csv_paths, (
        "The set of zero-byte '*.csv' files is not exactly as expected.\n"
        f"Expected: {sorted(map(str, expected_zero_csv_paths))}\n"
        f"Found:    {sorted(map(str, zero_csv_files))}"
    )