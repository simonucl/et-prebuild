# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the operating system /
filesystem before the student begins the task described in the prompt.

The checks intentionally verify ONLY the pre-existing artefacts and the absence
of the expected output artefacts.

Rules enforced by these tests:
1. The raw CSV file MUST already exist at the exact absolute path
   /home/user/data/raw/net_diag_2023-09.csv.
2. No processed directory or output files must exist yet.
3. The /home/user/data directory must not contain *any* sub-directories other
   than the mandated "raw" directory.
4. The raw CSV must be non-empty, have the correct header, and contain at least
   four data rows (the known fixture shipped with the assignment).
"""

import os
import re
import pytest

# -----------------------------------------------------------------------------
# Helper constants
# -----------------------------------------------------------------------------
HOME           = "/home/user"
DATA_DIR       = os.path.join(HOME, "data")
RAW_DIR        = os.path.join(DATA_DIR, "raw")
RAW_CSV        = os.path.join(RAW_DIR, "net_diag_2023-09.csv")
PROCESSED_DIR  = os.path.join(DATA_DIR, "processed")
SUMMARY_JSON   = os.path.join(PROCESSED_DIR, "net_diag_summary_2023-09.json")
EXEC_LOG       = os.path.join(PROCESSED_DIR, "net_diag_execution.log")

EXPECTED_HEADER = (
    "timestamp,source,destination,transmitted,received,packet_loss_percent,"
    "min_ms,avg_ms,max_ms,mdev_ms"
)

CSV_MIN_ROWS = 4  # We know the fixture has exactly 4 data rows


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_raw_csv_file_exists_and_is_regular_file():
    """
    The raw CSV file must already be present and be a regular file.
    """
    assert os.path.isfile(RAW_CSV), (
        f"Required raw CSV not found at {RAW_CSV}. "
        "The assignment states it must exist before any processing starts."
    )


def test_raw_csv_header_and_minimum_rows():
    """
    Ensure the CSV has the expected header row and at least four data rows.
    This guards against accidental corruption or mis-placement of the fixture.
    """
    with open(RAW_CSV, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    assert lines, (
        f"The file {RAW_CSV} is empty; expected at least a header line."
    )

    header = lines[0]
    assert header == EXPECTED_HEADER, (
        f"Header mismatch in {RAW_CSV}.\n"
        f"Expected: {EXPECTED_HEADER!r}\n"
        f"Found:    {header!r}"
    )

    data_rows = lines[1:]
    assert len(data_rows) >= CSV_MIN_ROWS, (
        f"{RAW_CSV} should contain at least {CSV_MIN_ROWS} data rows; "
        f"found only {len(data_rows)}."
    )


def test_only_raw_directory_present_under_data():
    """
    The /home/user/data directory must contain exactly one sub-directory
    called 'raw' at this stage—no 'processed' directory or any other folders.
    """
    assert os.path.isdir(DATA_DIR), f"Directory {DATA_DIR} is missing."

    subdirs = [
        name
        for name in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, name))
    ]

    # Using sorted lists purely for deterministic error message ordering
    expected_subdirs = ["raw"]
    assert sorted(subdirs) == expected_subdirs, (
        f"{DATA_DIR} must contain only the 'raw' directory at the start.\n"
        f"Expected sub-directories: {expected_subdirs}\n"
        f"Found: {sorted(subdirs)}"
    )


def test_processed_directory_does_not_exist_yet():
    """
    The processed directory and any artefacts inside it should not exist
    before the student runs their solution.
    """
    assert not os.path.exists(PROCESSED_DIR), (
        f"The directory {PROCESSED_DIR} already exists. "
        "It should only be created by the student's script."
    )


def test_summary_json_and_execution_log_absent():
    """
    Neither the summary JSON nor the execution log should exist at this point.
    """
    missing_files = [
        path for path in (SUMMARY_JSON, EXEC_LOG) if os.path.exists(path)
    ]
    assert not missing_files, (
        "Output artefacts already exist but should not be present yet: "
        f"{', '.join(missing_files)}"
    )