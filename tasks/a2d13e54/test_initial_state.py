# test_initial_state.py
#
# This test-suite asserts the pristine operating-system / filesystem state
# that must be in place *before* the student performs any work on the
# “CSV → JSON archive” task.
#
# It deliberately checks ONLY the inputs that are guaranteed to exist
# according to the specification and makes sure that none of the required
# output artefacts have been created yet.
#
# If any of these tests fail it means the grading VM is in an unexpected
# state and the subsequent functional tests would be meaningless.

import os
import io
import csv
import json
import re
from pathlib import Path

# Constants
CSV_PATH = Path("/home/user/backups/servers_2023-10-15.csv")
ARCHIVE_DIR = Path("/home/user/backups/archive")
JSON_PATH = ARCHIVE_DIR / "servers_2023-10-15.json"
LOG_PATH = ARCHIVE_DIR / "archive.log"

EXPECTED_CSV_ROWS = [
    ["id", "hostname", "ip"],
    ["1", "web01", "192.168.1.10"],
    ["2", "db01", "192.168.1.20"],
]

EXPECTED_JSON = (
    '[{"id":"1","hostname":"web01","ip":"192.168.1.10"},'
    '{"id":"2","hostname":"db01","ip":"192.168.1.20"}]'
)


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------


def read_csv_rows(path: Path):
    """Read a CSV file using utf-8 and return the rows as lists."""
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh, delimiter=",")
        return [row for row in reader]


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------


def test_csv_file_exists_with_correct_content():
    """The source CSV must exist, be UTF-8 and contain exactly 3 rows."""
    assert CSV_PATH.is_file(), (
        f"Required source CSV {CSV_PATH} is missing."
    )

    rows = read_csv_rows(CSV_PATH)
    assert (
        rows == EXPECTED_CSV_ROWS
    ), "CSV contents differ from the expected truth value."


def test_archive_directory_state_before_execution():
    """
    The /home/user/backups/archive directory may or may not exist yet, but:
    • The converted JSON file must NOT exist.
    • If archive.log exists, it must be empty.
    """
    if ARCHIVE_DIR.exists():
        assert ARCHIVE_DIR.is_dir(), (
            f"{ARCHIVE_DIR} exists but is not a directory."
        )
    # JSON must not yet exist
    assert not JSON_PATH.exists(), (
        f"{JSON_PATH} should NOT exist before the student runs their solution."
    )

    # archive.log: may not exist; if it does, it must be empty
    if LOG_PATH.exists():
        assert LOG_PATH.is_file(), f"{LOG_PATH} exists but is not a regular file."
        size = LOG_PATH.stat().st_size
        assert size == 0, (
            f"{LOG_PATH} should be empty before execution, "
            f"but its size is {size} bytes."
        )


def test_expected_json_constant_is_valid_single_line():
    """
    Sanity-check that our EXPECTED_JSON constant is a valid, single-line JSON
    string matching the CSV data.  This guards against typing errors inside
    the test-suite itself.
    """
    # Must be exactly one physical line (no embedded newlines)
    assert "\n" not in EXPECTED_JSON and "\r" not in EXPECTED_JSON, (
        "EXPECTED_JSON constant must not contain any newline characters."
    )

    # Parse and compare with CSV rows
    parsed = json.loads(EXPECTED_JSON)
    # Convert CSV rows to list of dicts for comparison
    header, *data_rows = EXPECTED_CSV_ROWS
    expected_from_csv = [dict(zip(header, row)) for row in data_rows]
    assert parsed == expected_from_csv, (
        "EXPECTED_JSON constant does not match the data from the CSV file."
    )