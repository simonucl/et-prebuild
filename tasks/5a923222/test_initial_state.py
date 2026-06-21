# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state expected by the FinOps cost-summary exercise.

The tests purposefully run **before** the student executes any commands.
They confirm:

1.   Raw-data folder and CSV files already exist.
2.   The “reports” folder and final report file do **not** yet exist.
3.   Each CSV file starts with the exact header line that the exercise
     specification demands.

If any assertion fails, the accompanying failure message explains exactly
what is missing or unexpected so that the learner can rectify the setup
before beginning the task.
"""

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
LOG_DIR = HOME / "cloud_logs"
REPORTS_DIR = LOG_DIR / "reports"
REPORT_FILE = REPORTS_DIR / "cost_summary_report.txt"

CSV_FILES = [
    LOG_DIR / "usage-2023-09.csv",
    LOG_DIR / "usage-2023-10.csv",
]

EXPECTED_HEADER = "resource_id,service,usage_hours,cost\n"


def test_raw_log_directory_exists():
    """The /home/user/cloud_logs directory must already exist."""
    assert LOG_DIR.is_dir(), (
        f"Required directory '{LOG_DIR}' is missing. "
        "Create it and place the raw CSV logs there."
    )


@pytest.mark.parametrize("csv_path", CSV_FILES, ids=[f.name for f in CSV_FILES])
def test_each_raw_csv_exists(csv_path: pathlib.Path):
    """Each expected raw CSV file must already be present."""
    assert csv_path.is_file(), (
        f"Required CSV file '{csv_path}' is missing. "
        "Ensure that the original usage logs are in place and named correctly."
    )


@pytest.mark.parametrize("csv_path", CSV_FILES, ids=[f.name for f in CSV_FILES])
def test_csv_header_is_correct(csv_path: pathlib.Path):
    """
    Verify that every CSV file starts with the exact header specified in
    the assignment. A wrong header will break downstream parsing.
    """
    with csv_path.open("r", encoding="utf-8") as fh:
        first_line = fh.readline()
    assert (
        first_line == EXPECTED_HEADER
    ), (
        f"File '{csv_path}' does not start with the expected header.\n"
        f"Expected: {EXPECTED_HEADER.strip()}\n"
        f"Found:    {first_line.strip()}\n"
        "Fix the header so it exactly matches the specification."
    )


def test_reports_directory_does_not_exist_yet():
    """
    The reports directory must **not** exist yet.
    Its creation is part of the learner's task.
    """
    assert not REPORTS_DIR.exists(), (
        f"Directory '{REPORTS_DIR}' already exists, but it should only be "
        "created by the student as part of the solution."
    )


def test_report_file_does_not_exist_yet():
    """
    The final cost summary report must **not** exist yet.
    Generating it is the goal of the exercise.
    """
    assert not REPORT_FILE.exists(), (
        f"Report file '{REPORT_FILE}' already exists. "
        "Remove it before starting the exercise so the task can be "
        "completed from a clean slate."
    )