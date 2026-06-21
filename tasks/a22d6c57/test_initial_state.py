# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the correct “starting” state *before* the student performs the
# cleaning task described in the project briefing.
#
# What we check:
#   1.  The required directory layout already exists.
#   2.  The two raw CSV files are present and contain the exact
#       expected content (including the trailing newline).
#   3.  No cleaned CSVs or benchmark log are present yet.
#
# Only the Python standard library plus pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

RAW_DIR = HOME / "data" / "raw"
PROCESSED_DIR = HOME / "data" / "processed"
BENCHMARK_DIR = HOME / "benchmark"

DATASET1_RAW_PATH = RAW_DIR / "dataset1.csv"
DATASET2_RAW_PATH = RAW_DIR / "dataset2.csv"

DATASET1_CLEAN_PATH = PROCESSED_DIR / "dataset1_clean.csv"
DATASET2_CLEAN_PATH = PROCESSED_DIR / "dataset2_clean.csv"
BENCHMARK_LOG_PATH = BENCHMARK_DIR / "cleaning_benchmark.log"

# ---------------------------------------------------------------------------
# Ground-truth content of the *raw* CSV files (including the trailing \n)
# ---------------------------------------------------------------------------
DATASET1_RAW_CONTENT = (
    "id,name,value\n"
    "1,Alice,10\n"
    "2,Bob,NA\n"
    "3,Charlie,30\n"
    "3,Charlie,30\n"
)

DATASET2_RAW_CONTENT = (
    "id,score\n"
    "1,95\n"
    "2,88\n"
    "2,88\n"
    "3,NA\n"
    "4,76\n"
)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def assert_is_dir(path: Path):
    assert path.exists(), f"Required directory missing: {path}"
    assert path.is_dir(), f"Path exists but is not a directory: {path}"


def read_file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_directory_layout_exists():
    """
    Validate that the directory skeleton that the assignment describes
    is already present on the filesystem.
    """
    for folder in (RAW_DIR, PROCESSED_DIR, BENCHMARK_DIR):
        assert_is_dir(folder)


@pytest.mark.parametrize(
    "file_path,expected_content",
    [
        (DATASET1_RAW_PATH, DATASET1_RAW_CONTENT),
        (DATASET2_RAW_PATH, DATASET2_RAW_CONTENT),
    ],
)
def test_raw_csv_files_present_and_correct(file_path: Path, expected_content: str):
    """
    The two raw CSV files must exist *exactly* as provided by the
    exercise starter kit.  This catches accidental edits or corruption.
    """
    assert file_path.exists(), f"Missing raw CSV file: {file_path}"
    assert file_path.is_file(), f"Path exists but is not a file: {file_path}"

    actual_content = read_file_text(file_path)

    # The comparison is strict (byte-for-byte after UTF-8 decoding).
    assert (
        actual_content == expected_content
    ), (
        f"Content mismatch in {file_path}.\n"
        "If you have already started working, make sure you did not "
        "edit the raw data in place."
    )

    # Ensure the file is newline-terminated; many CLI tools rely on this.
    assert actual_content.endswith(
        "\n"
    ), f"{file_path} must end with a single newline character."


def test_no_outputs_exist_yet():
    """
    Before the student performs any action, there must *not* be
    cleaned CSVs or benchmark logs in place.  Detecting their presence
    early avoids false positives later in the grading pipeline.
    """
    unexpected_paths = [
        DATASET1_CLEAN_PATH,
        DATASET2_CLEAN_PATH,
        BENCHMARK_LOG_PATH,
    ]

    for path in unexpected_paths:
        assert not path.exists(), (
            f"Found unexpected file before starting the task: {path}\n"
            "The workspace should be clean — remove any generated files "
            "and re-run the tests."
        )