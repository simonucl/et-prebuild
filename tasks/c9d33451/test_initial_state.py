# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student performs any actions.  It checks only for
# the existence and integrity of the raw CSV file that is the
# source for the forthcoming audit-trail task.  **It deliberately
# does NOT test for the audit directory or audit log file,** because
# those artefacts must be created by the student solution.

import hashlib
from pathlib import Path

import pytest

CSV_PATH = Path("/home/user/data/transactions_2021-12-31.csv")

# Expected, canonical contents of the CSV file.
EXPECTED_HEADER = "transaction_id,user_id,amount,currency"
EXPECTED_DATA_LINES = [
    "T1001,U23,150.00,USD",
    "T1002,U19,75.50,USD",
    "T1003,U11,20.00,EUR",
    "T1004,U23,125.00,USD",
]
EXPECTED_TOTAL_LINES = 1 + len(EXPECTED_DATA_LINES)  # header + 4 data rows


@pytest.fixture(scope="module")
def csv_lines():
    """
    Read the CSV file and return a list of lines **without** trailing newlines.
    """
    if not CSV_PATH.exists():
        pytest.fail(
            f"Required CSV file is missing: {CSV_PATH}. "
            "Make sure the file exists before running the task."
        )
    if not CSV_PATH.is_file():
        pytest.fail(
            f"Expected a file at {CSV_PATH}, but found a directory or special file."
        )

    with CSV_PATH.open("r", encoding="utf-8") as f:
        # read().splitlines() removes trailing '\n' from each line and handles
        # an optional final newline gracefully.
        return f.read().splitlines()


def test_csv_file_exists_and_is_not_empty(csv_lines):
    """
    Sanity-check that the file exists and contains at least the expected lines.
    """
    assert csv_lines, (
        f"{CSV_PATH} is empty. It must contain a header row and four data rows."
    )


def test_csv_has_expected_number_of_lines(csv_lines):
    assert len(csv_lines) == EXPECTED_TOTAL_LINES, (
        f"{CSV_PATH} should have exactly {EXPECTED_TOTAL_LINES} lines "
        f"(1 header + 4 data rows), but it has {len(csv_lines)}."
    )


def test_csv_header_is_correct(csv_lines):
    header = csv_lines[0]
    assert header == EXPECTED_HEADER, (
        "CSV header mismatch.\n"
        f"Expected: {EXPECTED_HEADER!r}\n"
        f"Found:    {header!r}"
    )


def test_csv_data_rows_are_correct(csv_lines):
    data_rows = csv_lines[1:]
    assert data_rows == EXPECTED_DATA_LINES, (
        "CSV data rows do not match the expected content.\n"
        "Expected:\n"
        + "\n".join(EXPECTED_DATA_LINES)
        + "\nFound:\n"
        + "\n".join(data_rows)
    )


def test_csv_md5_is_reproducible(csv_lines):
    """
    Compute the MD5 digest and check that it is 32 hexadecimal characters.
    This does not assert a hard-coded digest value (to avoid brittleness),
    but it guarantees that the file produces a valid MD5 string that the
    grader can later compare against.
    """
    md5 = hashlib.md5()
    # Re-read the file in binary mode for an exact checksum.
    with CSV_PATH.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    digest = md5.hexdigest()
    assert len(digest) == 32 and all(c in "0123456789abcdef" for c in digest), (
        f"Computed MD5 digest {digest!r} is not a valid 32-character "
        "lowercase hexadecimal string."
    )