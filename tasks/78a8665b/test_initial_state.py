# test_initial_state.py
#
# Pytest suite that asserts the *initial* file-system state is exactly as the
# exercise description promises.  These tests must pass **before** the student
# performs the migration work.

import csv
import os
from pathlib import Path

DATA_DIR = Path("/home/user/datasets")
CSV_A = DATA_DIR / "species_A.csv"
CSV_B = DATA_DIR / "species_B.csv"
SQLITE_DB = DATA_DIR / "research.db"
VALIDATION_LOG = DATA_DIR / "migration_validation.log"


def test_dataset_directory_exists():
    assert DATA_DIR.exists(), f"Expected directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def test_required_csv_files_exist():
    for csv_path in (CSV_A, CSV_B):
        assert csv_path.exists(), f"Required CSV file {csv_path} is missing."
        assert csv_path.is_file(), f"{csv_path} exists but is not a file."
        assert csv_path.stat().st_size > 0, f"CSV file {csv_path} is empty."


def test_output_files_do_not_yet_exist():
    # Neither the database nor the validation log should be present
    assert not SQLITE_DB.exists(), (
        f"Output database {SQLITE_DB} already exists. "
        "The student must create it during the migration step."
    )
    assert not VALIDATION_LOG.exists(), (
        f"Validation log {VALIDATION_LOG} already exists. "
        "It should be produced only after migration."
    )


def _csv_stats(csv_path):
    """
    Return a tuple:
        (row_count, missing_name, missing_weight, missing_length)
    for the given CSV, excluding the header line.
    """
    row_count = 0
    missing_name = 0
    missing_weight = 0
    missing_length = 0

    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)  # Skip header
        assert header is not None, f"CSV {csv_path} is empty (missing header)."

        for idx, row in enumerate(reader, start=2):  # start=2 => account for header line
            # Expected 4 columns: id, name, weight, length
            assert len(row) == 4, (
                f"CSV {csv_path} line {idx} does not have 4 columns: {row}"
            )

            row_count += 1

            _id, name, weight, length = row
            if name.strip() == "":
                missing_name += 1
            if weight.strip() == "":
                missing_weight += 1
            if length.strip() == "":
                missing_length += 1

    return row_count, missing_name, missing_weight, missing_length


def test_csv_contents_match_ground_truth():
    """
    Ensure the raw CSV files contain exactly the records & NULL patterns
    the exercise description declares.  This prevents students from starting
    with bad input data or an unexpected schema.
    """
    a_rows, a_miss_name, a_miss_weight, a_miss_length = _csv_stats(CSV_A)
    b_rows, b_miss_name, b_miss_weight, b_miss_length = _csv_stats(CSV_B)

    # Ground-truth numbers from the task description
    GT_SPECIES_A_ROWS = 5
    GT_SPECIES_B_ROWS = 4
    GT_COMBINED_ROWS = 9
    GT_MISSING_NAME = 2
    GT_MISSING_WEIGHT = 2
    GT_MISSING_LENGTH = 1

    # Row counts
    assert a_rows == GT_SPECIES_A_ROWS, (
        f"{CSV_A} is expected to have {GT_SPECIES_A_ROWS} data rows "
        f"but has {a_rows}."
    )
    assert b_rows == GT_SPECIES_B_ROWS, (
        f"{CSV_B} is expected to have {GT_SPECIES_B_ROWS} data rows "
        f"but has {b_rows}."
    )
    assert (a_rows + b_rows) == GT_COMBINED_ROWS, (
        "Total rows across both CSV files do not match ground truth: "
        f"{a_rows + b_rows} vs expected {GT_COMBINED_ROWS}."
    )

    # Missing value statistics
    combined_missing_name = a_miss_name + b_miss_name
    combined_missing_weight = a_miss_weight + b_miss_weight
    combined_missing_length = a_miss_length + b_miss_length

    assert combined_missing_name == GT_MISSING_NAME, (
        f"Expected {GT_MISSING_NAME} total missing 'name' values but found "
        f"{combined_missing_name}."
    )
    assert combined_missing_weight == GT_MISSING_WEIGHT, (
        f"Expected {GT_MISSING_WEIGHT} total missing 'weight' values but found "
        f"{combined_missing_weight}."
    )
    assert combined_missing_length == GT_MISSING_LENGTH, (
        f"Expected {GT_MISSING_LENGTH} total missing 'length' values but found "
        f"{combined_missing_length}."
    )