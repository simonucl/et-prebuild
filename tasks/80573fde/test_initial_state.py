# test_initial_state.py
#
# This pytest suite validates the filesystem state *before* the student runs
# any commands.  It checks that the three expected cloud-cost CSV files exist
# in /home/user/cloud_costs and contain the minimal sample data described in
# the task instructions.
#
# NOTE: Per the grading rules we deliberately do NOT look for (or even mention)
# the archive that the student must create later.  We only test pre-existing
# inputs.

import os
import stat
import pytest

CLOUD_COST_DIR = "/home/user/cloud_costs"

# Mapping of expected CSV filenames to their minimal expected contents
EXPECTED_FILES = {
    "aws_cost_report.csv":   "aws,2023-09,123.45\n",
    "azure_cost_report.csv": "azure,2023-09,67.89\n",
    "gcp_cost_report.csv":   "gcp,2023-09,45.67\n",
}


def test_cloud_cost_directory_exists():
    """
    Ensure the /home/user/cloud_costs directory exists and is a directory.
    """
    assert os.path.exists(CLOUD_COST_DIR), (
        f"Expected directory {CLOUD_COST_DIR!r} is missing."
    )
    assert stat.S_ISDIR(os.stat(CLOUD_COST_DIR).st_mode), (
        f"{CLOUD_COST_DIR!r} exists but is not a directory."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_each_cost_csv_exists_with_correct_content(filename, expected_content):
    """
    For each expected cloud-cost CSV, verify:
      1. The file exists at the exact full path.
      2. It is a regular file (not a directory or symlink).
      3. It contains the minimal expected single-line payload.
    """
    full_path = os.path.join(CLOUD_COST_DIR, filename)

    # 1. Existence
    assert os.path.exists(full_path), (
        f"Required CSV file {full_path!r} is missing."
    )

    # 2. Regular file
    assert stat.S_ISREG(os.stat(full_path).st_mode), (
        f"{full_path!r} exists but is not a regular file."
    )

    # 3. Content check (exact match including newline)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == expected_content, (
        f"Contents of {full_path!r} differ from expectation.\n"
        f"Expected: {expected_content!r}\n"
        f"Actual:   {content!r}"
    )