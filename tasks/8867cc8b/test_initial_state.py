# test_initial_state.py
#
# This test-suite validates that the filesystem is in the correct *initial*
# state before the student starts their work on the compliance task.  It
# verifies that:
#   1. The input CSV file exists and looks sane.
#   2. No output artefacts or directories have been created yet.
#
# Only modules from the Python standard library and pytest are used.

import csv
from pathlib import Path

import pytest

# ---------- Paths used throughout the tests ----------
HOME = Path("/home/user")
COMPLIANCE_DIR = HOME / "compliance"
RAW_CSV = COMPLIANCE_DIR / "audit_raw.csv"

REPORTS_DIR = COMPLIANCE_DIR / "reports"
COMPLIANCE_JSON = REPORTS_DIR / "compliance_report.json"
SUMMARY_CSV = REPORTS_DIR / "summary.csv"
GEN_LOG = REPORTS_DIR / "generation.log"


# ---------- Helper functions ----------
def read_csv_rows(path: Path):
    """Read a CSV file and return a list of rows (each row is a list)."""
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        return list(reader)


# ---------- Tests ----------
def test_raw_csv_exists_and_is_readable():
    """
    The raw audit CSV must already be present *before* the student begins the
    task.  This test confirms:
        • The file exists and is a regular file.
        • It contains the expected header.
        • It has exactly 6 data rows (one per server).
        • Each row has exactly 7 columns.
    """
    assert RAW_CSV.is_file(), (
        f"Expected input file {RAW_CSV} is missing. "
        "The student cannot begin without the raw scan data."
    )

    rows = read_csv_rows(RAW_CSV)
    assert rows, f"{RAW_CSV} appears to be empty."

    expected_header = [
        "system_id",
        "hostname",
        "os",
        "patch_level",
        "encrypted_disk",
        "antivirus_status",
        "last_audit_date",
    ]
    assert rows[0] == expected_header, (
        "Header mismatch in audit_raw.csv.\n"
        f"Expected: {expected_header}\n"
        f"Found   : {rows[0]}"
    )

    data_rows = rows[1:]
    assert len(data_rows) == 6, (
        "audit_raw.csv should contain exactly 6 data rows "
        f"(one per server) but found {len(data_rows)}."
    )

    for idx, row in enumerate(data_rows, start=2):  # start=2 for human-friendly CSV line numbers
        assert len(row) == 7, (
            f"Row {idx} in {RAW_CSV} does not have 7 columns: {row}"
        )


@pytest.mark.parametrize(
    "path_desc,path_obj",
    [
        ("reports directory", REPORTS_DIR),
        ("compliance_report.json", COMPLIANCE_JSON),
        ("summary.csv", SUMMARY_CSV),
        ("generation.log", GEN_LOG),
    ],
)
def test_output_artefacts_do_not_exist_yet(path_desc, path_obj):
    """
    None of the output artefacts should exist prior to the student's work.
    The task explicitly instructs the student to create them.  Their presence
    now would indicate leftover files from a previous run, which would make
    grading ambiguous.
    """
    assert not path_obj.exists(), (
        f"Pre-existing {path_desc} found at {path_obj}. "
        "Please start with a clean state (remove old artefacts) before beginning the task."
    )