# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem
# before the student begins the shell/awk/sed tasks described in
# the assignment.  It checks only the *input* area and never touches
# the output paths, in strict accordance with the instructions.
#
# Requirements verified:
#   • The CSV file /home/user/data/support_tickets.csv exists.
#   • The CSV file contains exactly the expected header and ten data
#     lines (eleven lines total).
#   • The file ends with a single trailing newline (no missing or
#     duplicate newline at EOF).

import os
from pathlib import Path

import pytest


CSV_PATH = Path("/home/user/data/support_tickets.csv")

# Expected file contents (no newline characters).
EXPECTED_LINES = [
    "ticket_id,created_date,assignee,status",
    "TCK-1001,01/13/2022,alice,OPEN",
    "TCK-1002,01/20/2022,bob,CLOSED",
    "TCK-1003,02/05/2022,charlie,OPEN",
    "TCK-1004,03/14/2022,dan,CLOSED",
    "TCK-1005,03/18/2022,alice,CLOSED",
    "TCK-1006,04/07/2023,bob,OPEN",
    "TCK-1007,05/11/2023,charlie,CLOSED",
    "TCK-1008,06/22/2023,dan,OPEN",
    "TCK-1009,07/19/2023,alice,CLOSED",
    "TCK-1010,08/01/2023,bob,OPEN",
]


def test_csv_file_exists():
    """
    The input CSV file must exist and be a regular file.
    """
    assert CSV_PATH.exists(), (
        f"Required file {CSV_PATH} is missing. "
        "Ensure the CSV export is placed in the correct directory."
    )
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."


def test_csv_contents_are_correct():
    """
    The CSV file must contain exactly the expected 11 lines
    (header + 10 records) and no more, no less, in the precise order.
    """
    with CSV_PATH.open("r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()  # strips newline chars

    assert lines == EXPECTED_LINES, (
        "Contents of support_tickets.csv do not match the expected data.\n"
        "Differences:\n"
        f"Expected ({len(EXPECTED_LINES)} lines):\n{EXPECTED_LINES}\n\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )


def test_csv_has_single_trailing_newline():
    """
    The CSV file must end with exactly one trailing newline.

    We read the raw bytes and verify that:
      • the very last byte is a LF (`\\n`)
      • the second-to-last byte is *not* a LF (avoids double newline)
    """
    raw = CSV_PATH.read_bytes()
    assert raw.endswith(b"\n"), (
        f"{CSV_PATH} is missing the required trailing newline at EOF."
    )
    assert not raw.endswith(b"\n\n"), (
        f"{CSV_PATH} ends with multiple newlines; only one trailing newline is allowed."
    )