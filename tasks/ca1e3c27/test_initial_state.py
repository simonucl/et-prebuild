# test_initial_state.py
#
# Pytest suite that verifies the expected *initial* state of the filesystem
# before the student starts working.  It checks that the raw input data is
# present with the exact expected contents and that none of the artefacts
# which the student has to create exist yet.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
DATASETS_DIR = Path("/home/user/datasets")
LOGS_DIR = Path("/home/user/logs")

RAW_FILE = DATASETS_DIR / "raw_sales.csv"
CLEANED_FILE = DATASETS_DIR / "cleaned_sales.csv"
SUMMARY_FILE = DATASETS_DIR / "summary_stats.json"
LOG_FILE = LOGS_DIR / "cleaning.log"

EXPECTED_RAW_LINES = [
    "order_id,order_date,region,sales",
    "A001,2020-01-02,North,100.50",
    "A002,2020/01/05,South,200",
    "A003,2020-01-07,,150",
    ",2020-01-10,East,250.75",
    "A005,2020-01-12,West,",
]


# -----------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------
def test_raw_sales_file_exists_and_is_readable():
    """raw_sales.csv must exist, be a regular file and be world-readable."""
    assert RAW_FILE.exists(), f"Expected {RAW_FILE} to exist."
    assert RAW_FILE.is_file(), f"Expected {RAW_FILE} to be a file, not a directory."
    # Read permission for owner is enough to open; world-readable will be checked below.
    assert os.access(RAW_FILE, os.R_OK), f"{RAW_FILE} is not readable."
    # Optional: Check world-readable bit (others can read).
    st_mode = RAW_FILE.stat().st_mode
    assert (
        st_mode & 0o004
    ), f"{RAW_FILE} should be world-readable (mode -----r--)."


def test_raw_sales_file_content_matches_expected():
    """The content of raw_sales.csv must exactly match the expected lines."""
    with RAW_FILE.open("r", encoding="utf-8") as f:
        actual_lines = [line.rstrip("\n") for line in f]

    assert (
        actual_lines == EXPECTED_RAW_LINES
    ), (
        f"Contents of {RAW_FILE} are not as expected.\n\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_RAW_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )


@pytest.mark.parametrize(
    "path_, description",
    [
        (CLEANED_FILE, "cleaned_sales.csv"),
        (SUMMARY_FILE, "summary_stats.json"),
        (LOG_FILE, "cleaning.log"),
    ],
)
def test_output_files_do_not_exist_yet(path_: Path, description: str):
    """Before the student runs their commands, no output artefacts should exist."""
    assert (
        not path_.exists()
    ), f"{description} should NOT exist yet at {path_}. It must be created by the student's solution."