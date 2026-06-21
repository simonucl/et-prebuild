# test_initial_state.py
"""
Pytest suite that validates the initial, pre-exercise state of the
operating system / file system.

The checks performed here make sure that ONLY the prerequisite input
artifacts are present and that they contain the exact, expected
contents.  No assertions are made about any output files or directories
that the student is supposed to create later.
"""

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INPUT_FILE = Path("/home/user/data/sales_2023.tsv")

EXPECTED_LINES = [
    "order_id\tproduct\tunits\tunit_price\tregion",
    "1001\tWidget-A\t25\t9.99\tNA",
    "1002\tWidget-B\t50\t19.99\tEU",
    "1003\tWidget-C\t10\t4.99\tAPAC",
]
EXPECTED_CONTENT = ("\n".join(EXPECTED_LINES) + "\n").encode()  # POSIX newline


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def read_binary(path: Path) -> bytes:
    """Read *path* in binary mode and return its bytes."""
    with path.open("rb") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_input_file_exists():
    """The source TSV file must be present before the student starts."""
    assert INPUT_FILE.exists(), (
        f"Required input file not found: {INPUT_FILE}. "
        "Make sure the file was copied to the correct location."
    )
    assert INPUT_FILE.is_file(), f"Expected a regular file at {INPUT_FILE}, got something else."


def test_input_file_content_exact_match():
    """Validate that the TSV file content matches the expected bytes EXACTLY."""
    actual_bytes = read_binary(INPUT_FILE)
    assert (
        actual_bytes == EXPECTED_CONTENT
    ), (
        "The content of the input file differs from the expected template.\n"
        f"Expected bytes:\n{EXPECTED_CONTENT!r}\n\n"
        f"Actual bytes:\n{actual_bytes!r}"
    )


@pytest.mark.parametrize("line_number, line_text", enumerate(EXPECTED_LINES, start=1))
def test_each_line_has_five_columns_and_correct_tabs(line_number, line_text):
    """
    Ensure every line in the file has exactly five columns
    (i.e. four TAB characters) and matches the expected text.
    """
    # Retrieve actual line
    with INPUT_FILE.open("r", encoding="utf-8") as fh:
        actual_lines = fh.read().splitlines()

    # Sanity check: correct number of lines
    assert len(actual_lines) == len(
        EXPECTED_LINES
    ), f"Expected {len(EXPECTED_LINES)} lines, found {len(actual_lines)}."

    actual_line = actual_lines[line_number - 1]

    # Check TAB count
    tab_count = actual_line.count("\t")
    assert (
        tab_count == 4
    ), f"Line {line_number} should contain 4 TABs (5 columns), but has {tab_count}."

    # Check exact text
    assert (
        actual_line == line_text
    ), f"Mismatch in line {line_number}.\nExpected: {line_text!r}\nActual:   {actual_line!r}"