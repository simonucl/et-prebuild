# test_initial_state.py
#
# This test-suite checks the *initial* state of the operating system / file-system
# before the student runs any commands.  It validates that the raw input data
# needed for the exercise is present and unmodified.
#
# DO **NOT** add tests for any output / result files that the student is
# supposed to create later on.  We only verify the GIVEN snapshot.

import pathlib
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DATA_DIR = pathlib.Path("/home/user/data")
SNAPSHOT_FILE = DATA_DIR / "process_snapshot.txt"

EXPECTED_HEADER = "PID USER     COMMAND"
EXPECTED_LINE_COUNT = 12  # 1 header line + 11 process lines
EXPECTED_USER_COUNTS = {
    "daemon": 2,
    "root": 5,
    "user": 4,
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _read_snapshot_lines():
    """Read the snapshot file and return a list of stripped lines."""
    try:
        text = SNAPSHOT_FILE.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        pytest.fail(f"Required file {SNAPSHOT_FILE} is missing.")  # noqa: B009
    return [ln.rstrip("\n") for ln in text.splitlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_snapshot_file_exists_and_is_regular_file():
    """The raw process snapshot must exist and be a regular file."""
    assert SNAPSHOT_FILE.exists(), f"Expected file {SNAPSHOT_FILE} does not exist."
    assert SNAPSHOT_FILE.is_file(), f"{SNAPSHOT_FILE} exists but is not a regular file."


def test_snapshot_header_is_correct():
    """Verify that the first line is the expected header."""
    lines = _read_snapshot_lines()
    assert lines, f"{SNAPSHOT_FILE} is empty."
    header = lines[0]
    assert (
        header == EXPECTED_HEADER
    ), f"Header mismatch in {SNAPSHOT_FILE!s}.\nExpected: {EXPECTED_HEADER!r}\nFound:    {header!r}"


def test_snapshot_has_expected_number_of_lines():
    """Sanity-check the total number of lines (header + process lines)."""
    lines = _read_snapshot_lines()
    assert len(lines) == EXPECTED_LINE_COUNT, (
        f"{SNAPSHOT_FILE} should contain {EXPECTED_LINE_COUNT} lines "
        f"(1 header + 11 process lines), but it has {len(lines)}."
    )


def test_user_process_counts_match_expected():
    """
    Parse the snapshot and make sure the per-user process counts are unchanged.

    This guarantees that the student works against the exact, unmodified data
    that the grading rubric expects.
    """
    lines = _read_snapshot_lines()[1:]  # skip header
    user_counts = {}

    for idx, line in enumerate(lines, start=2):  # start=2 to account for header as line 1
        # Split on arbitrary whitespace; there should be at least 3 columns.
        parts = line.split()
        assert (
            len(parts) >= 3
        ), f"Line {idx} in {SNAPSHOT_FILE} should have at least 3 columns (PID USER COMMAND). Found: {line!r}"

        pid, user, *_ = parts

        # Basic PID sanity
        assert pid.isdigit(), f"PID field on line {idx} is not numeric: {pid!r}"

        # Accumulate user count
        user_counts[user] = user_counts.get(user, 0) + 1

    # Final comparison with the expected dictionary
    assert (
        user_counts == EXPECTED_USER_COUNTS
    ), f"Per-user process counts differ from expected.\nExpected: {EXPECTED_USER_COUNTS}\nFound:    {user_counts}"