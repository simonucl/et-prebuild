# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must
# exist *before* the student begins any work.  It deliberately avoids
# touching the output artefacts (files or directories) that the student
# will create later on.

import os
from pathlib import Path

RAW_DIR   = Path("/home/user/finops/raw")
WORK_DIR  = Path("/home/user/finops/work")

USAGE_CSV   = RAW_DIR / "usage_report.csv"
PRICING_CSV = RAW_DIR / "pricing.csv"


def _read_lines(path: Path):
    """
    Helper that returns the file's lines **without** trailing newline
    characters, so comparisons are easier and cross-platform safe.
    """
    return path.read_text(encoding="utf-8").splitlines()


def test_directories_exist_and_are_dirs():
    """Ensure the required base directories exist and are directories."""
    assert RAW_DIR.exists(), f"Required directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."

    assert WORK_DIR.exists(), f"Required directory {WORK_DIR} is missing."
    assert WORK_DIR.is_dir(), f"{WORK_DIR} exists but is not a directory."


def test_usage_report_csv_exists_with_expected_content():
    """Validate /finops/raw/usage_report.csv header and data rows."""
    assert USAGE_CSV.exists(), f"Source file {USAGE_CSV} is missing."
    assert USAGE_CSV.is_file(), f"{USAGE_CSV} exists but is not a regular file."

    lines = _read_lines(USAGE_CSV)

    # The file must contain exactly 4 lines:
    expected_line_count = 4
    assert len(lines) == expected_line_count, (
        f"{USAGE_CSV} should have {expected_line_count} lines "
        f"(1 header + 3 data), found {len(lines)}."
    )

    # Validate header row.
    expected_header = "Service,ResourceID,HoursUsed,Region"
    assert lines[0] == expected_header, (
        f"Header of {USAGE_CSV} is incorrect.\n"
        f"Expected: {expected_header!r}\nFound:    {lines[0]!r}"
    )

    # Required data lines (order-agnostic).
    expected_rows = {
        "EC2,i-123456,720,us-east-1",
        "S3,bucket-abc,0,us-east-1",
        "RDS,db-654321,300,us-west-2",
    }
    actual_rows = set(lines[1:])

    missing = expected_rows - actual_rows
    extra   = actual_rows   - expected_rows
    assert not missing, f"{USAGE_CSV} is missing data rows: {missing}"
    assert not extra,   f"{USAGE_CSV} contains unexpected rows: {extra}"


def test_pricing_csv_exists_with_expected_content():
    """Validate /finops/raw/pricing.csv header and data rows."""
    assert PRICING_CSV.exists(), f"Source file {PRICING_CSV} is missing."
    assert PRICING_CSV.is_file(), f"{PRICING_CSV} exists but is not a regular file."

    lines = _read_lines(PRICING_CSV)

    # The file must contain exactly 4 lines:
    expected_line_count = 4
    assert len(lines) == expected_line_count, (
        f"{PRICING_CSV} should have {expected_line_count} lines "
        f"(1 header + 3 data), found {len(lines)}."
    )

    # Validate header row.
    expected_header = "Service,PricePerHourUSD,Region,LastUpdated"
    assert lines[0] == expected_header, (
        f"Header of {PRICING_CSV} is incorrect.\n"
        f"Expected: {expected_header!r}\nFound:    {lines[0]!r}"
    )

    # Required data lines (order-agnostic).
    expected_rows = {
        "EC2,0.023,us-east-1,2023-09-01",
        "S3,0.000,us-east-1,2023-09-01",
        "RDS,0.250,us-west-2,2023-09-01",
    }
    actual_rows = set(lines[1:])

    missing = expected_rows - actual_rows
    extra   = actual_rows   - expected_rows
    assert not missing, f"{PRICING_CSV} is missing data rows: {missing}"
    assert not extra,   f"{PRICING_CSV} contains unexpected rows: {extra}"