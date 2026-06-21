# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem state for the
# CSV-to-report migration task is correct *before* the student’s solution
# is executed.

from pathlib import Path
import pytest


CSV_PATH = Path("/home/user/service_mappings.csv")
REPORT_PATH = Path("/home/user/migration_report.txt")

EXPECTED_CSV_LINES = [
    "Service,OldURL,NewURL\n",
    "auth,https://old.example.com/auth,https://api.new-corp.io/auth\n",
    "billing,https://old.example.com/bill,https://api.new-corp.io/billing\n",
    "catalog,https://old.example.com/catalog,https://api.new-corp.io/catalog\n",
    "inventory,https://old.example.com/inv,https://api.new-corp.io/inventory\n",
    "shipping,https://old.example.com/ship,https://api.new-corp.io/shipping\n",
]


def test_mapping_file_exists_and_is_correct():
    """
    The mapping CSV must exist, be a regular file, and contain exactly
    the six expected lines (each terminated by a single LF character).
    """
    assert CSV_PATH.is_file(), (
        f"Required mapping file {CSV_PATH} is missing or not a regular file."
    )

    # Read as binary to examine exact newlines, then decode once verified.
    content = CSV_PATH.read_bytes()
    assert content.endswith(b"\n"), (
        f"{CSV_PATH} must end with exactly one UNIX newline (LF)."
    )
    assert not content.endswith(b"\n\n"), (
        f"{CSV_PATH} has an extra blank line at the end; "
        "it should contain exactly six lines with a single LF after each."
    )

    # Now decode and split into lines preserving newline characters
    lines = content.decode("utf-8").splitlines(keepends=True)
    assert lines == EXPECTED_CSV_LINES, (
        "Contents of service_mappings.csv are not as expected.\n"
        "Expected:\n"
        + "".join(EXPECTED_CSV_LINES)
        + "\nFound:\n"
        + "".join(lines)
    )


def test_migration_report_does_not_exist_yet():
    """
    Before the student runs their solution there should be NO
    /home/user/migration_report.txt file present.
    """
    assert not REPORT_PATH.exists(), (
        f"Unexpected file {REPORT_PATH} already exists. "
        "The report should be created only after running the required command."
    )