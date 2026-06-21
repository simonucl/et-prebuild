# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student carries out any actions for the assignment.
#
# It checks that:
#   1. /home/user/training_data/raw exists and is a directory
#   2. Exactly three CSV files are present in that directory:
#        - iris_train.csv
#        - iris_valid.csv
#        - iris_test.csv
#   3. Each of those CSV files contains the precise, expected contents
#      (including the single trailing newline)
#
# NOTE:
# * We intentionally do NOT check for the existence (or absence) of any
#   output artefacts such as /home/user/training_data/checksums, because
#   they are created later by the exercise itself.
# * Only the Python stdlib and pytest are used, per instructions.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "training_data" / "raw"

# Expected file names (alphabetical order for convenience)
EXPECTED_FILES = [
    "iris_test.csv",
    "iris_train.csv",
    "iris_valid.csv",
]

# Expected file contents, including the single trailing newline at EOF.
EXPECTED_CONTENTS = {
    "iris_train.csv": (
        "sepal_length,sepal_width,petal_length,petal_width,species\n"
        "5.1,3.5,1.4,0.2,setosa\n"
        "4.9,3.0,1.4,0.2,setosa\n"
        "6.2,3.4,5.4,2.3,virginica\n"
    ),
    "iris_valid.csv": (
        "sepal_length,sepal_width,petal_length,petal_width,species\n"
        "5.4,3.9,1.3,0.4,setosa\n"
        "6.0,2.2,4.0,1.0,versicolor\n"
        "6.9,3.1,5.1,2.3,virginica\n"
    ),
    "iris_test.csv": (
        "sepal_length,sepal_width,petal_length,petal_width,species\n"
        "4.8,3.0,1.4,0.3,setosa\n"
        "5.5,2.3,4.0,1.3,versicolor\n"
        "7.2,3.0,5.8,1.6,virginica\n"
    ),
}


def test_raw_directory_exists():
    """The /home/user/training_data/raw directory must exist."""
    assert RAW_DIR.is_dir(), (
        f"Expected directory '{RAW_DIR}' to exist, "
        "but it is missing or not a directory."
    )


def test_expected_csv_files_present():
    """All and only the expected CSV files must be present in RAW_DIR."""
    assert RAW_DIR.is_dir(), f"Required directory '{RAW_DIR}' does not exist."

    found_csvs = sorted(p.name for p in RAW_DIR.glob("*.csv"))
    missing = sorted(set(EXPECTED_FILES) - set(found_csvs))
    extra = sorted(set(found_csvs) - set(EXPECTED_FILES))

    if missing:
        pytest.fail(
            "Missing expected CSV file(s): "
            + ", ".join(missing)
        )
    if extra:
        pytest.fail(
            "Found unexpected CSV file(s) in the raw data directory: "
            + ", ".join(extra)
        )


@pytest.mark.parametrize("filename", EXPECTED_FILES)
def test_csv_file_contents(filename):
    """
    Each CSV must contain exactly the specified bytes, including a single
    trailing newline and no extra blank lines.
    """
    file_path = RAW_DIR / filename
    assert file_path.is_file(), f"Expected file '{file_path}' is missing."

    with file_path.open("r", encoding="utf-8") as f:
        actual = f.read()

    expected = EXPECTED_CONTENTS[filename]

    # Detailed comparison so failures show useful diff
    assert actual == expected, (
        f"Contents of '{file_path}' do not match expected reference.\n"
        f"--- Expected ({len(expected)} bytes) ---\n{expected!r}\n"
        f"--- Actual ({len(actual)} bytes) ---\n{actual!r}"
    )