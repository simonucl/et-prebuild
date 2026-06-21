# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be present
# before the learner begins the task.  Only the *pre-existing* artefacts are
# inspected; no assertions are made about any file that the learner is supposed
# to create or delete later on.

import os
from pathlib import Path

import pytest

# Constants -------------------------------------------------------------------

LOG_DIR = Path("/home/user/logs")
RAW_LOG = LOG_DIR / "uptime_raw.tsv"

# Helper ----------------------------------------------------------------------

def _load_raw_lines():
    """Read the raw‐log file and return a list of decoded text lines."""
    with RAW_LOG.open("rb") as fh:
        # Decode as UTF-8 — TSV files produced by standard tooling will be UTF-8.
        data = fh.read().decode("utf-8")
    # `splitlines(keepends=True)` keeps the newline character for precise tests.
    return data.splitlines(keepends=True)

# Tests -----------------------------------------------------------------------

def test_log_directory_exists():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"Expected {LOG_DIR} to be a directory."

def test_raw_log_file_exists():
    assert RAW_LOG.exists(), f"Required file {RAW_LOG} is missing."
    assert RAW_LOG.is_file(), f"{RAW_LOG} exists but is not a regular file."

def test_raw_log_line_count_and_trailing_newline():
    lines = _load_raw_lines()
    # The last element in `lines` must terminate with '\n'. If not, splitlines()
    # would have stripped it off.
    assert lines[-1].endswith("\n"), (
        f"{RAW_LOG} must end with a single newline character (\\n)."
    )
    assert len(lines) == 6, (
        f"{RAW_LOG} should contain exactly 6 lines "
        "(1 header + 5 data rows), found {len(lines)}."
    )

def test_raw_log_header():
    header_expected = "timestamp\tservice\tstatus\tresponse_ms\n"
    header_actual = _load_raw_lines()[0]
    assert header_actual == header_expected, (
        f"Header mismatch in {RAW_LOG!s}.\n"
        f"Expected: {header_expected!r}\n"
        f"Found   : {header_actual!r}"
    )

@pytest.mark.parametrize("line_no", range(1, 6))
def test_each_data_row_has_four_columns(line_no):
    """
    Verify each data row has exactly 4 tab-separated columns and that the
    status field is either 'OK' or 'FAIL'.
    """
    line = _load_raw_lines()[line_no].rstrip("\n")  # strip newline only
    cols = line.split("\t")
    assert len(cols) == 4, (
        f"Line {line_no+1} in {RAW_LOG} should have 4 columns "
        f"(found {len(cols)}): {line!r}"
    )

    timestamp, service, status, response_ms = cols
    # Basic ISO-8601 sanity check — must contain 'T' separator and end with 'Z'.
    assert "T" in timestamp and timestamp.endswith("Z"), (
        f"Line {line_no+1}: timestamp field looks malformed: {timestamp!r}"
    )
    assert status in {"OK", "FAIL"}, (
        f"Line {line_no+1}: status must be 'OK' or 'FAIL', found {status!r}"
    )