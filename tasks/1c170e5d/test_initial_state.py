# test_initial_state.py
#
# This pytest file verifies the *initial* filesystem state that must exist
# before the student begins the shell-scripting exercise.  It checks only
# the raw, unaltered data dump and its containing directory; it
# deliberately avoids looking for any of the files or directories the
# student is expected to create later.

from pathlib import Path
import pytest

RAW_DIR = Path("/home/user/work/raw")
RAW_FILE = RAW_DIR / "employee_records.csv"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_raw_file():
    """Return the entire contents of the raw CSV as a list of lines *with*
    their trailing newline stripped.  If the file cannot be read, pytest will
    fail immediately with a clear message.
    """
    try:
        text = RAW_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file {RAW_FILE} is missing.")
    except PermissionError:
        pytest.fail(f"Required file {RAW_FILE} exists but cannot be read "
                    f"(permission denied).")

    # Preserve blank lines: splitlines(keepends=False) keeps empty lines.
    return text.splitlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Expected directory {RAW_DIR} does not exist. "
        "The raw CSV dump should live here."
    )


def test_raw_file_exists_and_non_empty():
    assert RAW_FILE.is_file(), (
        f"Expected raw CSV file {RAW_FILE} does not exist."
    )
    assert RAW_FILE.stat().st_size > 0, (
        f"Raw CSV file {RAW_FILE} exists but is empty."
    )


def test_raw_file_exact_header():
    lines = _read_raw_file()
    assert lines, "Raw CSV file is empty after reading."
    expected_header = "#id,name,department,salary,join_date"
    assert lines[0] == expected_header, (
        "Header line of raw CSV is incorrect.\n"
        f"Expected: {expected_header!r}\n"
        f"Found   : {lines[0]!r}"
    )


def test_raw_file_records_and_trailing_blank_line():
    lines = _read_raw_file()

    # There must be exactly 1 header + 8 data lines + 1 blank line = 10 lines.
    expected_total = 10
    assert len(lines) == expected_total, (
        f"Raw CSV should have {expected_total} lines "
        f"(1 header, 8 data, 1 trailing blank line) but has {len(lines)}."
    )

    # The last line must be blank (empty string) to represent the trailing
    # blank line in the file.
    assert lines[-1] == "", (
        "Raw CSV should end with a single completely blank line, "
        "but the final line is not blank."
    )

    # Verify that each of the 8 data lines contains exactly 4 commas (5 fields).
    data_lines = lines[1:-1]  # skip header & blank line
    for idx, record in enumerate(data_lines, start=1):
        comma_count = record.count(",")
        assert comma_count == 4, (
            f"Data line {idx} ('{record}') should contain exactly 4 commas "
            f"(5 CSV fields) but contains {comma_count}."
        )