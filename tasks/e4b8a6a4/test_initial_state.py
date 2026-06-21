# test_initial_state.py
#
# Pytest suite that validates the operating–system / file-system state
# BEFORE the student writes any code for the FinOps “Makefile” task.
#
# • Uses only pytest + Python stdlib.
# • Fails clearly if the required initial artefacts are missing or if
#   files that should NOT exist are already present.

import os
from pathlib import Path

RAW_CSV_PATH = Path("/home/user/finops/raw/usage_2023-07.csv")
REPORTS_DIR   = Path("/home/user/finops/reports")
SUMMARY_PATH  = REPORTS_DIR / "2023-07-summary.log"
MAKEFILE_PATH = Path("/home/user/finops/Makefile")

EXPECTED_CSV_LINES = [
    "date,service,cost_usd",
    "2023-07-01,Compute,200.00",
    "2023-07-02,Compute,300.00",
    "2023-07-03,Storage,500.00",
    "2023-07-04,Network,23.45",
    "2023-07-05,Compute,500.00",
]


def test_raw_csv_exists_and_is_file():
    assert RAW_CSV_PATH.exists(), (
        f"Expected raw CSV file {RAW_CSV_PATH} is missing."
    )
    assert RAW_CSV_PATH.is_file(), (
        f"Path {RAW_CSV_PATH} exists but is not a regular file."
    )


def test_raw_csv_contents_are_exact():
    with RAW_CSV_PATH.open("r", encoding="utf-8") as fp:
        lines = [ln.rstrip("\n") for ln in fp.readlines()]

    assert lines == EXPECTED_CSV_LINES, (
        "The contents of the raw CSV file do not match the expected "
        "initial state.\n"
        f"Expected lines:\n{EXPECTED_CSV_LINES!r}\n\n"
        f"Actual lines:\n{lines!r}"
    )


def test_summary_file_does_not_preexist():
    # The reports directory itself is allowed to be absent or present,
    # but the final summary artefact must not pre-exist.
    assert not SUMMARY_PATH.exists(), (
        f"Summary file {SUMMARY_PATH} already exists, but it should not "
        "be present before the student runs `make july_summary`."
    )


def test_makefile_does_not_preexist():
    assert not MAKEFILE_PATH.exists(), (
        f"Makefile {MAKEFILE_PATH} already exists. The student is "
        "expected to create it from scratch."
    )