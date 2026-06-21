# test_initial_state.py
#
# This pytest suite verifies that the OS / filesystem is in the correct
# initial state *before* the student starts working on the assignment.
#
# What we check:
#   1. The working directory /home/user/cloud_costs exists and is a directory.
#   2. /home/user/cloud_costs/costs.csv exists, is a regular file, and is
#      readable by the current user.
#   3. The permissions on costs.csv are at least 0o644 (owner read-write,
#      group/other read).
#   4. The contents of costs.csv match the specification exactly
#      (header + 7 data rows, in the correct order, with the expected values).
#
# NOTE: We deliberately do *not* test for the presence or absence of any
#       output artefacts (monthly_summary.json, summary.log, …) because
#       those are produced *after* the student completes the task.
#
# The tests will fail with clear, actionable messages if any part of the
# expected state is missing or incorrect.

import os
import stat
import pytest

CLOUD_COSTS_DIR = "/home/user/cloud_costs"
COSTS_FILE = os.path.join(CLOUD_COSTS_DIR, "costs.csv")

# -----------------------------------------------------------------------------


def test_cloud_costs_directory_exists():
    """The /home/user/cloud_costs directory must exist."""
    assert os.path.exists(CLOUD_COSTS_DIR), (
        f"The directory {CLOUD_COSTS_DIR} is missing. "
        "It should be created before the exercise begins."
    )
    assert os.path.isdir(CLOUD_COSTS_DIR), (
        f"{CLOUD_COSTS_DIR} exists but is not a directory."
    )


def test_costs_csv_exists_and_readable():
    """costs.csv must exist and be readable."""
    assert os.path.exists(COSTS_FILE), (
        f"The file {COSTS_FILE} is missing. "
        "It should be provided to the student."
    )
    assert os.path.isfile(COSTS_FILE), f"{COSTS_FILE} exists but is not a regular file."

    # Check readability
    assert os.access(COSTS_FILE, os.R_OK), f"{COSTS_FILE} is not readable by the current user."


def test_costs_csv_permissions():
    """costs.csv should have permissions rw-r--r-- (>= 0o644)."""
    mode = stat.S_IMODE(os.stat(COSTS_FILE).st_mode)
    expected_min_mode = 0o644
    assert mode & 0o777 >= expected_min_mode, (
        f"{COSTS_FILE} has permissions {oct(mode)}, expected at least {oct(expected_min_mode)} "
        "(owner read/write, group and world read)."
    )


def test_costs_csv_content_exact():
    """Verify that costs.csv content matches the specification exactly."""
    expected_lines = [
        "service,date,cost",
        "EC2,2023-09-01,10.50",
        "EC2,2023-09-15,20.00",
        "EC2,2023-08-20,5.00",
        "RDS,2023-09-05,30.00",
        "RDS,2023-09-20,40.00",
        "S3,2023-09-10,50.11",
        "S3,2023-09-11,52.11",
    ]

    with open(COSTS_FILE, "r", encoding="utf-8") as f:
        file_lines = [line.rstrip("\n") for line in f]

    assert file_lines == expected_lines, (
        f"The contents of {COSTS_FILE} do not match the expected data.\n"
        "Expected lines:\n"
        + "\n".join(expected_lines)
        + "\n\nActual lines:\n"
        + "\n".join(file_lines)
    )