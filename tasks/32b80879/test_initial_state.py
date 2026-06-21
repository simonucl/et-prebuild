# test_initial_state.py
#
# Pytest suite to verify the operating-system state **before** the student
# starts the assignment.
#
# It checks that:
# 1. The datasets directory and the CSV file exist.
# 2. The CSV file’s contents are *exactly* as specified (including the
#    trailing newline on the last line).
# 3. The output directory **does not** yet exist.
# 4. The target JSON and log files do **not** yet exist.
#
# If any of these assertions fail, the error messages will make clear
# what is missing or unexpectedly present.

import os
from pathlib import Path

DATASETS_DIR = Path("/home/user/datasets")
CSV_PATH = DATASETS_DIR / "temperature_readings.csv"

OUTPUT_DIR = Path("/home/user/output")
JSON_PATH = OUTPUT_DIR / "temperature_f.json"
LOG_PATH = OUTPUT_DIR / "conversion.log"

EXPECTED_CSV_CONTENT = (
    "Date,City,TempC\n"
    "2023-01-01,Paris,5\n"
    "2023-01-01,New York,-3\n"
    "2023-01-02,Paris,6.5\n"
    "2023-01-02,New York,-1\n"
)


def test_datasets_directory_exists():
    assert DATASETS_DIR.exists(), f"Required directory missing: {DATASETS_DIR}"
    assert DATASETS_DIR.is_dir(), f"{DATASETS_DIR} exists but is not a directory"


def test_csv_file_exists_with_exact_content():
    assert CSV_PATH.exists(), f"Required CSV file missing: {CSV_PATH}"
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a file"

    actual = CSV_PATH.read_text(encoding="utf-8")
    assert (
        actual == EXPECTED_CSV_CONTENT
    ), (
        "CSV file content does not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "---- Actual ----\n"
        f"{actual!r}\n"
    )


def test_output_directory_does_not_exist_yet():
    # The /home/user/output/ directory should not exist before the student runs anything.
    assert not OUTPUT_DIR.exists(), (
        f"Output directory {OUTPUT_DIR} should NOT exist before the task starts, "
        "but it is already present."
    )


def test_target_files_do_not_exist_yet():
    # Neither the JSON nor the log file should exist at the outset.
    for path in (JSON_PATH, LOG_PATH):
        assert not path.exists(), (
            f"File {path} should not be present before the student performs the task."
        )