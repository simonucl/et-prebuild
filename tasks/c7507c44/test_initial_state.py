# test_initial_state.py
#
# This test-suite validates ONLY the *initial* state of the filesystem
# before the student performs any action for the “configuration files” task.
#
# Rules respected:
#   • Uses only stdlib + pytest
#   • Does NOT refer to or touch **any** of the required output files or
#     directories (/home/user/project/**).  It only checks the prerequisite
#     raw-data area that must already be present.
#   • Employs absolute paths.
#   • Provides clear, explicit failure messages.

import os
import pytest
from pathlib import Path

RAW_DATA_DIR = Path("/home/user/data/raw")
EXPECTED_CSVS = [
    "cats_vs_dogs.csv",
    "flowers102.csv",
    "cifar10.csv",
]


def _human_readable_list(paths):
    """Helper to format a list of paths for assertion messages."""
    return ", ".join(str(p) for p in paths)


def test_raw_data_directory_exists():
    """
    The task description states that the raw CSV files have already been
    collected under /home/user/data/raw/.  Therefore that directory must
    exist *before* the student starts creating configuration files.
    """
    assert RAW_DATA_DIR.is_dir(), (
        f"Expected raw-data directory {RAW_DATA_DIR} to exist, "
        "but it is missing."
    )


@pytest.mark.parametrize("csv_name", EXPECTED_CSVS)
def test_expected_raw_csv_files_present(csv_name):
    """
    Each of the three dataset CSVs must already be present.  The student
    should not have to create them as part of this task.
    """
    csv_path = RAW_DATA_DIR / csv_name
    assert csv_path.is_file(), (
        f"Required raw CSV file {csv_path} is missing. "
        "Make sure the initial data collection step succeeded."
    )
    # Optional sanity-check: ensure the file is not empty.
    file_size = csv_path.stat().st_size
    assert file_size > 0, (
        f"The file {csv_path} exists but is empty (0 bytes). "
        "It should contain at least some data."
    )


def test_no_missing_raw_csv_files():
    """
    Provide an aggregated assertion so that if multiple CSVs are missing
    the failure message lists all of them at once.
    """
    missing = [RAW_DATA_DIR / name for name in EXPECTED_CSVS if not (RAW_DATA_DIR / name).is_file()]
    assert not missing, (
        "The following expected raw CSV files are missing before the "
        f"student starts the task: {_human_readable_list(missing)}"
    )