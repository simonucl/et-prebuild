# test_initial_state.py
#
# This test-suite asserts that the environment is in the **initial** state
# expected *before* the student’s ETL solution is executed.
#
# It checks that:
#   • the raw source directory and CSV files exist and have the exact, known
#     content supplied in the assignment;
#   • no output artefacts produced by a yet-to-be-written solution are present.
#
# If any of these tests fail, the submission environment itself is broken, not
# the student’s code.  The failure messages therefore explain precisely what
# is missing or different.

from pathlib import Path
import csv
import pytest

# Fixed absolute paths used throughout the assignment
RAW_DIR = Path("/home/user/raw_data")
Q1_FILE = RAW_DIR / "sales_q1.csv"
Q2_FILE = RAW_DIR / "sales_q2.csv"

PROCESSED_FILE = Path("/home/user/processed/customer_summary.csv")
LOG_DIR = Path("/home/user/etl_logs")
LOG_FILE = LOG_DIR / "etl_2024-08-15T00-00-00Z.log"

# --------------------------------------------------------------------------- #
# Helper data that encodes the *expected* contents of the two source files.
# --------------------------------------------------------------------------- #
_EXPECTED_Q1_LINES = [
    "order_id,customer_id,order_date,item_count,item_total,discount",
    "1001,C001,2024-01-05,3,120.50,5.00",
    "1002,C002,2024-01-07,1,45.00,0.00",
    "1003,C003,2024-02-18,2,89.99,10.00",
    "1004,C001,2024-03-22,5,300.00,15.00",
]

_EXPECTED_Q2_LINES = [
    "order_id,customer_id,order_date,item_count,item_total,discount",
    "1005,C003,2024-04-02,1,40.00,0.00",
    "1006,C004,2024-04-11,2,95.00,5.00",
    "1007,C002,2024-05-27,4,180.00,20.00",
    "1008,C003,2024-06-30,3,135.50,10.50",
]


# --------------------------------------------------------------------------- #
# Tests for the raw input area
# --------------------------------------------------------------------------- #
def test_raw_data_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing. "
        "The assignment expects the raw CSV files to be located here."
    )


@pytest.mark.parametrize(
    ("csv_path", "expected_lines"),
    [
        (Q1_FILE, _EXPECTED_Q1_LINES),
        (Q2_FILE, _EXPECTED_Q2_LINES),
    ],
)
def test_raw_csv_file_exists_and_content(csv_path: Path, expected_lines):
    # 1. Existence
    assert csv_path.is_file(), f"Expected source file {csv_path} does not exist."

    # 2. Read the file and normalise line endings (strip trailing '\n' or '\r\n')
    with csv_path.open("r", encoding="utf-8") as fp:
        actual_lines = [line.rstrip("\n\r") for line in fp.readlines()]

    # 3. Content equality
    assert actual_lines == expected_lines, (
        f"File {csv_path} has unexpected contents.\n"
        "Expected lines:\n"
        + "\n".join(expected_lines)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )

    # 4. Quick structural sanity-check: every line must contain exactly 6 commas
    for ln, text in enumerate(actual_lines, start=1):
        comma_count = text.count(",")
        assert comma_count == 5, (
            f"Line {ln} of {csv_path} should contain 5 commas "
            f"(6 CSV columns) but has {comma_count} commas."
        )

    # 5. Verify header fields individually to aid in clearer error reporting
    header = actual_lines[0]
    header_fields = header.split(",")
    expected_header = [
        "order_id",
        "customer_id",
        "order_date",
        "item_count",
        "item_total",
        "discount",
    ]
    assert header_fields == expected_header, (
        f"The header of {csv_path} is incorrect.\n"
        f"Expected: {expected_header}\nActual:   {header_fields}"
    )


# --------------------------------------------------------------------------- #
# Tests that ensure *output* artefacts are NOT present yet.
# --------------------------------------------------------------------------- #
def test_processed_customer_summary_does_not_yet_exist():
    assert not PROCESSED_FILE.exists(), (
        f"The output file {PROCESSED_FILE} already exists before the ETL job "
        f"has run.  The environment must start clean."
    )


def test_etl_log_does_not_yet_exist():
    # The logs directory itself may or may not exist beforehand, but the
    # specific log file must certainly not exist yet.
    assert not LOG_FILE.exists(), (
        f"The log file {LOG_FILE} already exists before the ETL job has run.  "
        "The environment must start clean."
    )