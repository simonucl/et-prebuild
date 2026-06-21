# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# for the “SSH hardening assessment” task *before* the student’s solution runs.
#
# It checks:
#   • Presence of the input CSV file and its exact contents.
#   • Presence (and writability) of the target directories for reports & logs.
#
# Only stdlib + pytest are used, and no output artefacts are referenced.

import os
import csv
import stat
from pathlib import Path

INPUT_CSV_PATH = Path("/home/user/hardening/input/ssh_audit.csv")
REPORTS_DIR = Path("/home/user/hardening/reports")
LOGS_DIR = Path("/home/user/hardening/logs")

EXPECTED_HEADER = [
    "line_number",
    "hostname",
    "PermitRootLogin",
    "PasswordAuthentication",
    "Port",
]

# Expected rows in the same order they appear in the file.
EXPECTED_ROWS = [
    ("1", "server1", "yes", "yes", "22"),
    ("2", "server2", "no", "no", "2222"),
    ("3", "server3", "yes", "no", "22"),
    ("4", "server4", "no", "yes", "22"),
]


def _check_writable(path: Path) -> bool:
    """
    Helper that returns True iff `path` is writable by the current user.
    """
    return os.access(path, os.W_OK)


def test_input_csv_exists_and_is_readable():
    """Confirm the input CSV file exists, is a file, and is readable."""
    assert INPUT_CSV_PATH.exists(), (
        f"Required input CSV file not found at {INPUT_CSV_PATH}."
    )
    assert INPUT_CSV_PATH.is_file(), (
        f"{INPUT_CSV_PATH} exists but is not a regular file."
    )
    assert os.access(INPUT_CSV_PATH, os.R_OK), (
        f"{INPUT_CSV_PATH} exists but is not readable."
    )


def test_reports_and_logs_directories_exist_and_writable():
    """Verify that required output directories exist and are writable."""
    for directory in (REPORTS_DIR, LOGS_DIR):
        assert directory.exists(), (
            f"Expected directory {directory} is missing."
        )
        assert directory.is_dir(), (
            f"{directory} exists but is not a directory."
        )
        assert _check_writable(directory), (
            f"Directory {directory} is not writable by the current user."
        )


def test_csv_header_and_rows_are_correct():
    """Validate the exact header and row contents of the input CSV."""
    with INPUT_CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    # Split header vs. data rows
    assert rows, f"{INPUT_CSV_PATH} appears to be empty."
    header, data_rows = rows[0], rows[1:]

    # Header validation
    assert header == EXPECTED_HEADER, (
        f"CSV header mismatch.\n  Expected: {EXPECTED_HEADER}\n  Found   : {header}"
    )

    # Row count validation
    assert len(data_rows) == len(
        EXPECTED_ROWS
    ), (
        f"CSV should contain {len(EXPECTED_ROWS)} data rows but contains {len(data_rows)}."
    )

    # Per-row content validation
    for idx, (expected, actual) in enumerate(zip(EXPECTED_ROWS, data_rows), start=1):
        assert tuple(actual) == expected, (
            f"Row {idx} content mismatch.\n  Expected: {expected}\n  Found   : {tuple(actual)}"
        )