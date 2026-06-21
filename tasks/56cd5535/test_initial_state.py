# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state for the
# “ticket-processing” exercise.  It guarantees that the starting data the
# student must work with is present and correct *before* any commands are run.
#
# Rules satisfied:
#   • Uses only stdlib + pytest
#   • Checks for required directories / files, but **does not** reference
#     any of the files the student is expected to create later.
#   • Provides clear assertion messages for any failure.

from pathlib import Path
import pytest

HOME = Path("/home/user")
TICKETS_DIR = HOME / "tickets"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _read_nonblank_lines(path: Path):
    """
    Return the file's lines with trailing newlines stripped and
    skip completely blank lines (if any).
    """
    with path.open("r", encoding="utf-8") as f:
        return [ln.rstrip("\n\r") for ln in f if ln.strip()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_tickets_directory_exists_and_is_directory():
    assert TICKETS_DIR.exists(), f"Required directory missing: {TICKETS_DIR}"
    assert TICKETS_DIR.is_dir(), f"{TICKETS_DIR} exists but is not a directory"


@pytest.mark.parametrize(
    "csv_name",
    ["open_tickets.csv", "closed_tickets.csv"],
)
def test_csv_files_exist(csv_name):
    csv_path = TICKETS_DIR / csv_name
    assert csv_path.exists(), f"Required file missing: {csv_path}"
    assert csv_path.is_file(), f"{csv_path} exists but is not a regular file"


def test_open_tickets_csv_contents():
    """
    Validate that /home/user/tickets/open_tickets.csv contains exactly the
    expected header and ticket rows (blank lines are ignored).
    """
    expected_lines = [
        "ticket_id,priority,assigned_to,customer,issue_type,status",
        "TCK-1001,High,alice,Acme Corp,Network,Open",
        "TCK-1002,Medium,bob,Globex Inc,Hardware,Open",
        "TCK-1003,Low,,Initech,Software,Open",
        'TCK-1004,High,charlie,"A&B Consulting",Network,Open',
    ]

    csv_path = TICKETS_DIR / "open_tickets.csv"
    actual_lines = _read_nonblank_lines(csv_path)

    # Ensure line-for-line equality (order matters)
    assert actual_lines == expected_lines, (
        f"Contents of {csv_path} do not match the expected initial data.\n"
        f"Expected ({len(expected_lines)} lines):\n  " + "\n  ".join(expected_lines) +
        f"\n\nActual ({len(actual_lines)} lines):\n  " + "\n  ".join(actual_lines)
    )


def test_closed_tickets_csv_contents():
    """
    Validate that /home/user/tickets/closed_tickets.csv contains exactly the
    expected header and ticket rows (blank lines are ignored).
    """
    expected_lines = [
        "ticket_id,resolution_time_min,assigned_to,customer,issue_type,status",
        "TCK-0901,45,dan,Acme Corp,Network,Closed",
        "TCK-0902,120,alice,Globex Inc,Hardware,Closed",
        "TCK-0903,30,alice,Initech,Software,Closed",
        "TCK-0904,15,bob,Acme Corp,Hardware,Closed",
    ]

    csv_path = TICKETS_DIR / "closed_tickets.csv"
    actual_lines = _read_nonblank_lines(csv_path)

    assert actual_lines == expected_lines, (
        f"Contents of {csv_path} do not match the expected initial data.\n"
        f"Expected ({len(expected_lines)} lines):\n  " + "\n  ".join(expected_lines) +
        f"\n\nActual ({len(actual_lines)} lines):\n  " + "\n  ".join(actual_lines)
    )