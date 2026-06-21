# test_initial_state.py
#
# Pytest suite that validates the initial state of the filesystem
# PRIOR to the student’s action.  It checks that the tickets
# directory and CSV file exist and contain the expected data.
#
# NOTE: The tests intentionally do NOT look for /home/user/ticket_status.txt
# or any other output artefacts.  They only verify the initial, given state.

import os
import stat
import csv
import pytest

TICKETS_DIR = "/home/user/tickets"
CSV_PATH = os.path.join(TICKETS_DIR, "tickets.csv")

EXPECTED_LINES = [
    "TicketID,User,Issue,Status,Priority",
    "TCK-1001,alice,Cannot login,Open,High",
    "TCK-1002,bob,Printer offline,In Progress,Medium",
    "TCK-1003,charlie,VPN issue,Resolved,Low",
    "TCK-1004,dana,Email bounce,Open,Medium",
    "TCK-1005,ed,Password reset,Resolved,Low",
]

def _mode(path):
    """Return the permission bits (e.g. 0o644) for the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)


@pytest.mark.describe("Initial filesystem layout")
class TestInitialState:
    def test_tickets_directory_exists(self):
        assert os.path.isdir(TICKETS_DIR), (
            f"Required directory {TICKETS_DIR} is missing or not a directory."
        )

    def test_tickets_directory_permissions(self):
        mode = _mode(TICKETS_DIR)
        # Directory should be at least rwx for user and rx for group/other (0755).
        assert mode & 0o777 == 0o755, (
            f"{TICKETS_DIR} should have permissions 755, "
            f"found {oct(mode)} instead."
        )

    def test_csv_file_exists(self):
        assert os.path.isfile(CSV_PATH), (
            f"Required CSV file {CSV_PATH} is missing."
        )

    def test_csv_file_permissions(self):
        mode = _mode(CSV_PATH)
        # File should be readable by everyone and writable by owner (0644).
        assert mode & 0o777 == 0o644, (
            f"{CSV_PATH} should have permissions 644, "
            f"found {oct(mode)} instead."
        )

    def test_csv_file_contents_exact(self):
        with open(CSV_PATH, "r", encoding="utf-8") as fp:
            actual_lines = [line.rstrip("\n") for line in fp.readlines()]

        assert actual_lines == EXPECTED_LINES, (
            "The contents of tickets.csv do not match the expected initial data.\n"
            "Expected:\n"
            + "\n".join(EXPECTED_LINES)
            + "\n\nActual:\n"
            + "\n".join(actual_lines)
        )

    def test_csv_has_five_data_rows(self):
        with open(CSV_PATH, newline="", encoding="utf-8") as fp:
            reader = csv.reader(fp)
            rows = list(reader)

        header, data_rows = rows[0], rows[1:]
        # Sanity checks
        assert header == [
            "TicketID",
            "User",
            "Issue",
            "Status",
            "Priority",
        ], "Header row is incorrect in tickets.csv."

        assert len(data_rows) == 5, (
            f"Expected 5 ticket rows after header, found {len(data_rows)}."
        )

        # Each row should contain exactly 5 columns
        for idx, row in enumerate(data_rows, start=1):
            assert len(row) == 5, (
                f"Row {idx} in tickets.csv does not have 5 columns: {row}"
            )