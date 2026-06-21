# test_initial_state.py
#
# Pytest suite to validate the *initial* filesystem / OS state
# before the student’s solution is executed.
#
# These tests intentionally ensure that:
#   • the raw CSV files are present and intact
#   • no output artefacts (database / report file) are present yet
#
# Only Python’s standard library and pytest are used.

import csv
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# CONSTANT PATHS
# ---------------------------------------------------------------------------
BASE_DIR = Path("/home/user/network_diag")
DEVICES_CSV = BASE_DIR / "devices.csv"
PINGS_CSV = BASE_DIR / "pings.csv"
SQLITE_DB = BASE_DIR / "netmon.db"
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "connectivity_summary.log"


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def _read_csv(path: Path):
    """Return a tuple (header, rows) for the CSV at *path*."""
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
        if not rows:
            pytest.fail(f"CSV file {path} is empty.")
        header, *data = rows
    return header, data


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------
def test_base_directory_exists():
    assert BASE_DIR.exists(), f"Required directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_raw_csv_files_present():
    for csv_path in (DEVICES_CSV, PINGS_CSV):
        assert csv_path.exists(), f"Required CSV file {csv_path} is missing."
        assert csv_path.is_file(), f"{csv_path} exists but is not a regular file."
        assert csv_path.stat().st_size > 0, f"CSV file {csv_path} is empty."


def test_devices_csv_content():
    header, rows = _read_csv(DEVICES_CSV)
    expected_header = ["id", "hostname", "mgmt_ip", "site"]
    assert header == expected_header, (
        f"Header mismatch in {DEVICES_CSV}.\n"
        f"Expected: {expected_header}\n"
        f"Found   : {header}"
    )
    expected_row_count = 5
    assert len(rows) == expected_row_count, (
        f"{DEVICES_CSV} should contain {expected_row_count} data rows "
        f"but contains {len(rows)}."
    )


def test_pings_csv_content():
    header, rows = _read_csv(PINGS_CSV)
    expected_header = ["id", "device_id", "rtt_ms", "success", "ts_utc"]
    assert header == expected_header, (
        f"Header mismatch in {PINGS_CSV}.\n"
        f"Expected: {expected_header}\n"
        f"Found   : {header}"
    )
    expected_row_count = 12
    assert len(rows) == expected_row_count, (
        f"{PINGS_CSV} should contain {expected_row_count} data rows "
        f"but contains {len(rows)}."
    )


def test_no_database_yet():
    assert not SQLITE_DB.exists(), (
        f"SQLite database {SQLITE_DB} already exists. "
        f"The student task should create it from scratch."
    )


def test_no_report_file_yet():
    if REPORT_DIR.exists():
        # The directory might be pre-created, but the file must not exist yet.
        assert REPORT_DIR.is_dir(), f"{REPORT_DIR} exists but is not a directory."
    assert not REPORT_FILE.exists(), (
        f"Report file {REPORT_FILE} already exists. "
        f"The student task should generate it during execution."
    )