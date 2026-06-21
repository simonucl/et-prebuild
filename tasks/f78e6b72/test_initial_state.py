# test_initial_state.py
#
# This pytest suite verifies **only** the pre-existing state of the filesystem
# before the student starts working.  It intentionally ignores all files that
# the student is expected to create later.
#
# Requirements it checks:
#   1. /home/user/capacity/ exists and is a directory
#   2. /home/user/capacity/raw_usage.log exists, is a regular file, and
#      contains exactly the eight expected lines (LF endings implied)
#   3. Each line in raw_usage.log has exactly four whitespace-separated columns
#   4. Exactly one line has the literal string “N/A” in the third column
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import re
import pytest

CAPACITY_DIR = Path("/home/user/capacity")
RAW_LOG = CAPACITY_DIR / "raw_usage.log"

# The canonical list of expected lines (without the trailing LF)
EXPECTED_LINES = [
    "2023-09-01T00:00 serverA 45 70",
    "2023-09-01T01:00 serverB 60 65",
    "2023-09-01T02:00 serverA 55 85",
    "2023-09-01T03:00 serverC N/A 40",
    "2023-09-01T04:00 serverB 75 82",
    "2023-09-01T05:00 serverC 30 90",
    "2023-09-01T06:00 serverA 65 75",
    "2023-09-01T07:00 serverB 50 79",
]

@pytest.fixture(scope="module")
def raw_log_lines():
    """Return the contents of raw_usage.log split into lines (without newlines)."""
    if not RAW_LOG.exists():
        pytest.fail(f"Required file {RAW_LOG} is missing.")
    if not RAW_LOG.is_file():
        pytest.fail(f"{RAW_LOG} exists but is not a regular file.")
    content = RAW_LOG.read_text(encoding="utf-8").splitlines()
    return content


def test_capacity_directory_exists():
    assert CAPACITY_DIR.exists(), f"Directory {CAPACITY_DIR} is missing."
    assert CAPACITY_DIR.is_dir(), f"{CAPACITY_DIR} exists but is not a directory."


def test_raw_usage_log_exists_and_length(raw_log_lines):
    assert len(raw_log_lines) == 8, (
        f"{RAW_LOG} should contain exactly 8 lines, "
        f"but {len(raw_log_lines)} were found."
    )


def test_raw_usage_log_exact_content(raw_log_lines):
    # Compare line-for-line to catch any deviation (whitespace included)
    assert raw_log_lines == EXPECTED_LINES, (
        f"{RAW_LOG} contents do not match the expected baseline.\n\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LINES)
        + "\n\nActual:\n"
        + "\n".join(raw_log_lines)
    )


def test_each_line_has_four_columns(raw_log_lines):
    for idx, line in enumerate(raw_log_lines, start=1):
        cols = re.split(r"\s+", line.strip())
        assert len(cols) == 4, (
            f"Line {idx} in {RAW_LOG} does not have exactly 4 columns:\n{line}"
        )


def test_exactly_one_na_in_cpu_column(raw_log_lines):
    na_count = 0
    for idx, line in enumerate(raw_log_lines, start=1):
        timestamp, server, cpu, mem = re.split(r"\s+", line.strip())
        if cpu == "N/A":
            na_count += 1
    assert na_count == 1, (
        f"There should be exactly one line with 'N/A' in the CPU column; "
        f"found {na_count}."
    )