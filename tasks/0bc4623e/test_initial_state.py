# test_initial_state.py
"""
Pytest suite that validates the filesystem *before* the student has carried
out any processing steps.  It checks that the raw data are present and that
none of the artefacts the student must create exist yet.

The tests purposefully avoid looking for any output files the student is
expected to create; instead, they confirm that those files are currently
absent so that later tests (or the grader) can be sure the student produced
them.
"""

from pathlib import Path
import os
import platform
import pytest

HOME = Path("/home/user")

RAW_DIR = HOME / "data" / "raw"
COMBINED_DIR = HOME / "data" / "combined"
PROCESSED_DIR = HOME / "data" / "processed"

RAW_2021 = RAW_DIR / "products_2021.csv"
RAW_2022 = RAW_DIR / "products_2022.csv"

OUTPUT_PRODUCTS_ALL = COMBINED_DIR / "products_all.csv"
OUTPUT_CLEAN_JSONL = PROCESSED_DIR / "products_clean.jsonl"
OUTPUT_PREP_LOG = PROCESSED_DIR / "prep.log"


@pytest.fixture(scope="module")
def raw_2021_expected():
    return (
        "id,product_name,price,category,discontinued\n"
        "1,Widget,19.99,gadgets,no\n"
        "2,Gizmo,29.99,gadgets,no\n"
        "3,OldThing,9.99,antiques,yes\n"
    )


@pytest.fixture(scope="module")
def raw_2022_expected():
    return (
        "id,product_name,price,category,discontinued\n"
        "4,Widget Pro,24.99,gadgets,no\n"
        "5,Gizmo Plus,34.99,gadgets,no\n"
        "6,AncientThing,49.99,antiques,no\n"
    )


def test_running_on_linux():
    """The grading environment must be a Unix-like OS (Linux)."""
    assert platform.system() == "Linux", (
        f"Expected to run on Linux, but platform.system() returned "
        f"{platform.system()!r}"
    )


def test_raw_directory_exists():
    """The /home/user/data/raw directory must exist."""
    assert RAW_DIR.is_dir(), f"Required directory {RAW_DIR} is missing."


@pytest.mark.parametrize("csv_path", [RAW_2021, RAW_2022])
def test_raw_csv_files_exist(csv_path: Path):
    """Both raw CSV files must exist."""
    assert csv_path.is_file(), f"Required raw CSV file {csv_path} is missing."


def test_raw_2021_content(raw_2021_expected):
    """products_2021.csv must contain the expected data exactly."""
    contents = RAW_2021.read_text(encoding="utf-8")
    assert contents == raw_2021_expected, (
        f"Content of {RAW_2021} differs from the expected template.\n"
        "If the file looks correct, check for whitespace or newline issues."
    )


def test_raw_2022_content(raw_2022_expected):
    """products_2022.csv must contain the expected data exactly."""
    contents = RAW_2022.read_text(encoding="utf-8")
    assert contents == raw_2022_expected, (
        f"Content of {RAW_2022} differs from the expected template.\n"
        "If the file looks correct, check for whitespace or newline issues."
    )


def _assert_missing(path: Path):
    assert not path.exists(), (
        f"{path} already exists, but it should NOT be present before the "
        "student processes the data."
    )


def test_combined_products_all_absent():
    """products_all.csv should not exist yet."""
    _assert_missing(OUTPUT_PRODUCTS_ALL)


def test_processed_products_clean_absent():
    """products_clean.jsonl should not exist yet."""
    _assert_missing(OUTPUT_CLEAN_JSONL)


def test_processed_prep_log_absent():
    """prep.log should not exist yet."""
    _assert_missing(OUTPUT_PREP_LOG)