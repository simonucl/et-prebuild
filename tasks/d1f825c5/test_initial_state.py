# test_initial_state.py
#
# This pytest suite validates the initial operating-system / filesystem
# state *before* the student begins the exercise.  It makes sure the
# raw dataset exists exactly as specified and that no output artefacts
# are present yet.  Failures include clear messages so the student
# immediately knows what is missing or unexpected.
#
# Rules respected:
# • stdlib + pytest only
# • absolute paths used
# • does **not** test for any artefacts that must be created later
#   (cleaned CSV, benchmark log, etc.)

import os
from pathlib import Path

import pytest

# Constant paths used in all tests
RAW_DIR = Path("/home/user/datasets/raw")
RAW_FILE = RAW_DIR / "sales.csv"

CLEAN_FILE = Path("/home/user/datasets/clean/sales_clean.csv")
BENCHMARK_LOG = Path("/home/user/benchmark/cleaning_benchmark.log")

# Exact, byte-for-byte contents expected in /home/user/datasets/raw/sales.csv
EXPECTED_CSV = (
    "id,region,sales\n"
    "1,North,100\n"
    "2,South,200\n"
    "3,,150\n"
    "4,East,\n"
    "5,West,300\n"
)


def test_raw_directory_exists():
    """Verify that the raw data directory exists."""
    assert RAW_DIR.is_dir(), (
        f"Required directory '{RAW_DIR}' is missing. "
        "Create it and place the raw CSV inside."
    )


def test_sales_csv_exists():
    """Verify that the sales.csv file exists in the raw directory."""
    assert RAW_FILE.is_file(), (
        f"Required file '{RAW_FILE}' is missing. "
        "Make sure the raw sales.csv is present before running the task."
    )


def test_sales_csv_content_exact():
    """Verify that the raw CSV file content is exactly as expected."""
    with RAW_FILE.open("r", encoding="utf-8") as fh:
        content = fh.read()

    assert content == EXPECTED_CSV, (
        "The contents of 'sales.csv' do not match the expected initial state.\n\n"
        "Expected (byte-for-byte):\n"
        f"{EXPECTED_CSV!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )


def test_sales_csv_line_count():
    """Sanity-check that the raw CSV has exactly 6 lines (header + 5 rows)."""
    with RAW_FILE.open("r", encoding="utf-8") as fh:
        line_count = sum(1 for _ in fh)

    assert line_count == 6, (
        f"'sales.csv' should contain exactly 6 lines (found {line_count}). "
        "Verify that the file has not been modified."
    )


def test_clean_csv_not_yet_present():
    """The cleaned CSV should NOT exist before the student runs their solution."""
    assert not CLEAN_FILE.exists(), (
        f"Output file '{CLEAN_FILE}' already exists before the task begins. "
        "Remove it so the exercise starts from a clean state."
    )


def test_benchmark_log_not_yet_present():
    """The benchmark log should NOT exist before the student runs their solution."""
    assert not BENCHMARK_LOG.exists(), (
        f"Benchmark log '{BENCHMARK_LOG}' already exists before the task begins. "
        "Remove it so the exercise starts from a clean state."
    )