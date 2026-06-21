# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating-system /
# file-system _before_ the learner starts working on the task described in the
# README.  These checks make sure the starting conditions are exactly as the
# exercise expects.
#
# Rules enforced:
#   • Only stdlib + pytest are used.
#   • Tests reference full, absolute paths.
#   • No output-file / output-directory (items the learner must create) is
#     referenced—only prerequisite assets are inspected.
#
# To run:
#     pytest -q
#
# ---------------------------------------------------------------------------

import os
import textwrap
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
USERS_CSV = HOME / "site" / "config" / "users.csv"

# Expected initial content (no trailing blank lines, no charlie yet)
EXPECTED_INITIAL_CSV = textwrap.dedent(
    """\
    username,email,role
    alice,alice@example.com,editor
    bob,bob@example.com,viewer"""
).splitlines()  # list without newline characters


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_nonblank_stripped_lines(fp: Path):
    """
    Read a text file and return a list of lines with:
      • universal newline handling,
      • trailing newline removed,
      • blank lines omitted.
    """
    with fp.open("r", encoding="utf-8") as f:
        return [ln.rstrip("\n\r") for ln in f if ln.strip() != ""]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_users_csv_exists_and_is_regular_file():
    """The prerequisite CSV file must exist and be a regular file."""
    assert USERS_CSV.exists(), (
        f"Required file is missing: {USERS_CSV}. "
        "The exercise cannot proceed without this seed data."
    )
    assert USERS_CSV.is_file(), f"Expected {USERS_CSV} to be a regular file."


def test_users_csv_initial_content_exactly_two_user_records():
    """
    The initial CSV must contain exactly:
        • the header line,
        • two user records (alice, bob),
        • NO record for 'charlie' yet,
        • lines in alphabetical order.
    Blank lines are not allowed.
    """
    lines = _read_nonblank_stripped_lines(USERS_CSV)

    # Overall line count
    assert (
        len(lines) == 3
    ), f"Expected 3 non-blank lines (header + 2 records) in {USERS_CSV}, found {len(lines)}."

    # Exact match with the expected starting content
    assert (
        lines == EXPECTED_INITIAL_CSV
    ), textwrap.dedent(
        f"""\
        Unexpected contents in {USERS_CSV}.

        Expected:
        {EXPECTED_INITIAL_CSV}

        Found:
        {lines}
        """
    )

    # Sanity: ensure 'charlie' is indeed absent
    assert all(
        "charlie," not in ln for ln in lines
    ), "'charlie' record should NOT be present before the learner adds it."