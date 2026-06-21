# test_initial_state.py
#
# This test-suite validates the **initial** operating-system / filesystem
# state *before* the student performs any actions.
#
# It checks that the raw ticket dump exists exactly as expected and that
# it still contains the duplicated TicketID rows and mixed date formats
# which the student is supposed to fix later on.
#
# NOTE:
# * We purposefully do NOT test for the presence (or absence) of any
#   output files or the “processed” directory, in accordance with the
#   grading-specification rules.
# * Only stdlib + pytest are used.

import os
import csv
import pytest
from collections import Counter

HELPDESK_DIR = "/home/user/helpdesk"
TICKETS_CSV = os.path.join(HELPDESK_DIR, "tickets.csv")

# ---------------------------------------------------------------------------
# Static expectation for the raw CSV file (exact byte-for-byte content)
# ---------------------------------------------------------------------------
EXPECTED_RAW_CONTENT = (
    "TicketID,User,Status,Priority,Date\n"
    "101,alice,Open,High,18/09/2023\n"
    "102,bob,Closed,Low,18-09-2023\n"
    "103,charlie,Open,Medium,2023/09/17\n"
    "104,dave,Closed,High,2023-09-17\n"
    "101,alice,Open,High,18/09/2023\n"
    "105,alice,Closed,Low,2023-09-16\n"
    "106,erin,Open,High,16-09-2023\n"
    "107,frank,Open,Low,2023/09/15\n"
    "106,erin,Open,High,16-09-2023\n"
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def read_file_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def read_file_text(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Actual tests
# ---------------------------------------------------------------------------

def test_helpdesk_directory_exists():
    assert os.path.isdir(
        HELPDESK_DIR
    ), f"Required directory '{HELPDESK_DIR}' is missing."


def test_tickets_csv_exists():
    assert os.path.isfile(
        TICKETS_CSV
    ), f"Required raw CSV '{TICKETS_CSV}' is missing."


def test_tickets_csv_exact_content():
    actual = read_file_bytes(TICKETS_CSV)
    expected = EXPECTED_RAW_CONTENT.encode("utf-8")
    assert (
        actual == expected
    ), (
        f"Content of '{TICKETS_CSV}' does not match the expected initial "
        "state. If the file was modified, replace it with the original "
        "raw dump before proceeding."
    )


def test_tickets_csv_contains_duplicate_ticket_ids():
    # Read via csv module for robustness
    with open(TICKETS_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        ticket_ids = [row["TicketID"] for row in reader]

    counter = Counter(ticket_ids)
    duplicated = [tid for tid, cnt in counter.items() if cnt > 1]
    assert duplicated, (
        "The raw CSV should contain duplicated TicketID rows so the "
        "student can practise de-duplication, but none were found."
    )
    # For additional clarity we expect 101 and 106 duplicates
    expected_dupes = {"101", "106"}
    assert expected_dupes.issubset(
        duplicated
    ), (
        f"Expected duplicated TicketIDs {sorted(expected_dupes)} not found. "
        "File may have been altered."
    )


@pytest.mark.parametrize(
    "date_fragment",
    [
        "/",        # indicates formats with slashes e.g. 18/09/2023 or 2023/09/17
        "-",        # indicates formats with hyphens e.g. 18-09-2023 or 2023-09-17
    ],
)
def test_tickets_csv_has_mixed_date_formats(date_fragment):
    with open(TICKETS_CSV, encoding="utf-8") as fh:
        text = fh.read()

    assert (
        date_fragment in text
    ), (
        f"No '{date_fragment}' character found in Date column values. "
        "The initial CSV is supposed to contain mixed date formats "
        "using both '/' and '-' so the student can normalise them."
    )