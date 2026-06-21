# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student performs any actions for the “IT-support
# technician” exercise.

import csv
from pathlib import Path

import pytest

HELPDESK_DIR = Path("/home/user/helpdesk")
RAW_CSV_PATH = HELPDESK_DIR / "tickets_raw.csv"

# Files that must NOT exist yet (they are the student's deliverables)
MISSING_OUTPUT_FILES = [
    HELPDESK_DIR / "daily_summary.json",
    HELPDESK_DIR / "unresolved_report.txt",
    HELPDESK_DIR / "process.log",
]

# Exact CSV content expected in the initial state
EXPECTED_CSV_LINES = [
    ["TicketID", "Submitted", "Resolved", "Agent", "Priority", "Status"],
    ["1001", "2023-06-01 09:15", "2023-06-01 10:20", "alice", "HIGH", "RESOLVED"],
    ["1002", "2023-06-01 11:05", "", "bob", "LOW", "OPEN"],
    ["1003", "2023-06-01 12:30", "2023-06-02 08:45", "charlie", "MEDIUM", "RESOLVED"],
    ["1004", "2023-06-02 09:45", "", "alice", "HIGH", "OPEN"],
    ["1005", "2023-06-02 10:00", "2023-06-02 16:10", "bob", "LOW", "RESOLVED"],
    ["1006", "2023-06-03 14:20", "", "charlie", "MEDIUM", "PENDING"],
    ["1007", "2023-06-03 15:55", "", "alice", "CRITICAL", "OPEN"],
    ["1008", "2023-06-03 16:05", "2023-06-04 09:00", "bob", "LOW", "RESOLVED"],
]


def read_csv(path: Path):
    """Return list-of-lists representation of the CSV, preserving empty strings."""
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        return [row for row in reader]


@pytest.mark.dependency(name="dir_and_file_exist")
def test_helpdesk_directory_and_raw_csv_exist():
    assert HELPDESK_DIR.exists() and HELPDESK_DIR.is_dir(), (
        f"Directory {HELPDESK_DIR} is missing. "
        "The starter project should contain this directory."
    )

    assert RAW_CSV_PATH.exists() and RAW_CSV_PATH.is_file(), (
        f"File {RAW_CSV_PATH} is missing. "
        "The raw CSV must be present before the student starts."
    )


@pytest.mark.dependency(depends=["dir_and_file_exist"], name="csv_content_correct")
def test_raw_csv_has_exact_expected_content():
    actual_lines = read_csv(RAW_CSV_PATH)

    # Helpful failure if number of lines is off
    assert len(actual_lines) == len(EXPECTED_CSV_LINES), (
        f"{RAW_CSV_PATH} should have {len(EXPECTED_CSV_LINES)} lines "
        f"(header + 8 data rows), but it has {len(actual_lines)}."
    )

    # Compare line-by-line & cell-by-cell for maximum clarity on failure
    for idx, (expected, actual) in enumerate(zip(EXPECTED_CSV_LINES, actual_lines), start=1):
        assert expected == actual, (
            f"Line {idx} of {RAW_CSV_PATH} is incorrect.\n"
            f"Expected: {expected}\n"
            f"Actual  : {actual}"
        )


@pytest.mark.dependency(depends=["dir_and_file_exist", "csv_content_correct"])
def test_student_output_files_do_not_yet_exist():
    """
    The deliverable files must *not* exist in the initial state.
    Their absence proves the student has not started the task.
    """
    for path in MISSING_OUTPUT_FILES:
        assert not path.exists(), (
            f"{path} should NOT exist before the student begins. "
            "Detected an unexpected file in the initial state."
        )