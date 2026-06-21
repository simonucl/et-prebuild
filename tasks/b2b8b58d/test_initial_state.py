# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state before the student
carries out the assignment.

Expected initial conditions
---------------------------
1. The staging directory and CSV already exist:
      /home/user/edge_staging/devices.csv

2. The deployment directory has NOT been created yet:
      /home/user/edge_deploy   (must be absent)

The checks below ensure the starting environment is correct so the grader can
later verify the student's work unambiguously.
"""
import csv
import os
from pathlib import Path

STAGING_DIR = Path("/home/user/edge_staging")
DEVICES_CSV = STAGING_DIR / "devices.csv"
DEPLOY_DIR = Path("/home/user/edge_deploy")


def test_staging_directory_exists():
    assert STAGING_DIR.exists(), (
        f"Required staging directory {STAGING_DIR} is missing. "
        "It must be pre-created by the exercise setup."
    )
    assert STAGING_DIR.is_dir(), (
        f"{STAGING_DIR} exists but is not a directory."
    )


def test_devices_csv_exists_and_is_file():
    assert DEVICES_CSV.exists(), (
        f"CSV file {DEVICES_CSV} is missing. "
        "It must be present before the student starts."
    )
    assert DEVICES_CSV.is_file(), (
        f"{DEVICES_CSV} exists but is not a regular file."
    )


def test_devices_csv_content():
    """
    Validate the CSV structure and row count exactly match the specification.
    """
    # Read the file using csv module to ensure valid UTF-8 and comma-separated format
    with DEVICES_CSV.open("r", encoding="utf-8") as fp:
        reader = csv.reader(fp)
        rows = list(reader)

    # Expected header and rows (order matters)
    expected_rows = [
        ["id", "hw_rev", "location"],
        ["1", "A1", "rack-01"],
        ["2", "B2", "rack-02"],
        ["3", "A1", "rack-03"],
    ]

    assert rows == expected_rows, (
        f"Content of {DEVICES_CSV} is not as expected.\n"
        f"Expected rows:\n{expected_rows}\n"
        f"Actual rows:\n{rows}"
    )


def test_deploy_directory_absent_initially():
    """
    The deployment directory must NOT exist before the student runs their
    transformation script. Its presence would indicate the environment was
    already modified.
    """
    assert not DEPLOY_DIR.exists(), (
        f"Deployment directory {DEPLOY_DIR} should NOT exist yet. "
        "It will be created by the student's solution."
    )