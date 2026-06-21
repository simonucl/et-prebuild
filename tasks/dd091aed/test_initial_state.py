# test_initial_state.py
#
# This test-suite validates that the operating-system / file-system is
# still in the **initial** state – i.e. before the student runs their
# cleaning pipeline.  It confirms that the raw CSV is present and
# unmodified, that the expected duplicate rows and dirty tokens exist,
# and that **no** output directory or files have been created yet.
#
# The tests purposefully fail if any part of the clean-up has already
# been performed.

import pathlib
import pytest

HOME_DIR = pathlib.Path("/home/user")
DATASETS_DIR = HOME_DIR / "datasets"
RAW_DIR = DATASETS_DIR / "raw"
PROCESSED_DIR = DATASETS_DIR / "processed"

RAW_CSV = RAW_DIR / "weird_values.csv"
CLEANED_CSV = PROCESSED_DIR / "cleaned_values.csv"
LOG_FILE = PROCESSED_DIR / "cleaning.log"


def _read_raw_lines():
    """Return the raw CSV lines stripped of the trailing LF."""
    with RAW_CSV.open("r", encoding="utf-8", newline="") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


def test_raw_csv_exists_and_has_header():
    assert RAW_CSV.is_file(), (
        f"Required raw CSV file is missing: {RAW_CSV!s}"
    )

    lines = _read_raw_lines()
    assert lines, "Raw CSV file is empty."
    assert lines[0] == "id,name,value", (
        "The first line in the raw CSV must be exactly 'id,name,value'."
    )


def test_raw_csv_contains_dirty_tokens():
    lines_joined = "\n".join(_read_raw_lines())

    assert "NULL" in lines_joined, (
        "The token 'NULL' expected in the raw CSV was not found."
    )
    assert "N/A" in lines_joined, (
        "The token 'N/A' expected in the raw CSV was not found."
    )


def test_raw_csv_contains_expected_duplicates():
    lines = _read_raw_lines()

    bravo_row = "2,Bravo,NULL"
    charlie_row = "3,Charlie,30"

    assert lines.count(bravo_row) >= 2, (
        f"The row '{bravo_row}' is expected to appear at least twice in the "
        "raw CSV so that the student can demonstrate deduplication."
    )
    assert lines.count(charlie_row) >= 2, (
        f"The row '{charlie_row}' is expected to appear at least twice in the "
        "raw CSV so that the student can demonstrate deduplication."
    )


def test_processed_directory_does_not_exist_yet():
    assert not PROCESSED_DIR.exists(), (
        f"The directory '{PROCESSED_DIR}' should NOT exist before running the "
        "clean-up commands."
    )


def test_no_output_files_yet():
    assert not CLEANED_CSV.exists(), (
        f"The cleaned CSV '{CLEANED_CSV}' should not exist before the "
        "student performs the task."
    )
    assert not LOG_FILE.exists(), (
        f"The log file '{LOG_FILE}' should not exist before the "
        "student performs the task."
    )