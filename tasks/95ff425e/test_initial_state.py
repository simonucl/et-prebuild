# test_initial_state.py
#
# Pytest suite that validates the PRE-exercise operating-system / filesystem
# state for the “support_tickets” assignment.  It checks only the assets that
# must already exist (and nothing that the student is expected to create).
#
# If any test here fails, the sandbox is not in the correct *initial* state
# and the student cannot be expected to complete the task successfully.

import os
import stat
import subprocess
from pathlib import Path

import pytest

# Base directory for the project
BASE_DIR = Path("/home/user/support_tickets")
DATA_DIR = BASE_DIR / "data"
SCRIPTS_DIR = BASE_DIR / "scripts"

TICKETS_CSV = DATA_DIR / "tickets.csv"
RESOLVE_SH = SCRIPTS_DIR / "resolve_ticket.sh"


@pytest.fixture(scope="module")
def expected_csv_text():
    """
    The exact UTF-8 text that must be present in tickets.csv.
    A final newline is required.
    """
    return (
        "id,client,issue\n"
        "101,Acme Corp,Printer not responding\n"
        "102,Globex Inc,VPN disconnecting\n"
        "103,Initech,Email bounce back\n"
    )


def test_tickets_csv_exists_with_exact_content(expected_csv_text):
    """
    Verify that the tickets.csv file exists at the exact path and contains
    the expected byte-for-byte content (UTF-8).
    """
    assert TICKETS_CSV.is_file(), (
        f"Expected file not found: {TICKETS_CSV}"
    )

    try:
        content = TICKETS_CSV.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{TICKETS_CSV} is not valid UTF-8: {exc}")

    assert content == expected_csv_text, (
        "Content of tickets.csv does not match the required initial state.\n"
        "---- Expected ----\n"
        f"{expected_csv_text}"
        "---- Found ----\n"
        f"{content}"
    )


def test_resolve_ticket_script_exists_and_is_executable():
    """
    Ensure resolve_ticket.sh exists, is a file, and is executable by the user.
    """
    assert RESOLVE_SH.is_file(), (
        f"Expected script not found: {RESOLVE_SH}"
    )

    mode = RESOLVE_SH.stat().st_mode
    is_executable = bool(mode & stat.S_IXUSR)
    assert is_executable, (
        f"{RESOLVE_SH} exists but is not marked as executable."
    )


@pytest.mark.parametrize("ticket_id", ["101", "999", "42"])
def test_resolve_ticket_runtime_behavior(ticket_id):
    """
    Invoke the resolve_ticket.sh stub with a few sample IDs and
    confirm its STDOUT and exit status.
    """
    cmd = [str(RESOLVE_SH), ticket_id]
    proc = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        timeout=5,
    )

    assert proc.returncode == 0, (
        f"Running {RESOLVE_SH} with ID {ticket_id} returned "
        f"non-zero exit status {proc.returncode}."
    )

    expected_stdout = f"Ticket {ticket_id} resolved\n"
    assert proc.stdout == expected_stdout, (
        "Unexpected STDOUT from resolve_ticket.sh.\n"
        f"Expected: {expected_stdout!r}\nFound:    {proc.stdout!r}"
    )

    # The stub should not output anything to STDERR
    assert proc.stderr == "", (
        f"resolve_ticket.sh wrote to STDERR: {proc.stderr!r}"
    )