# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state is exactly what
# the assignment expects *before* the student performs any action.

import os
from pathlib import Path

DATASET_DIR = Path("/home/user/datasets")
RAW_FILE = DATASET_DIR / "raw_sales.tsv"
TRIMMED_FILE = DATASET_DIR / "trimmed_sales.tsv"
LOG_FILE = DATASET_DIR / "processing.log"

HEADER = ["Region", "Product", "Q1", "Q2", "Q3", "Q4", "Notes"]
DATA_ROWS = [
    ["North", "Widget", "1200", "1300", "1400", "1500", "High demand"],
    ["South", "Gadget", "900", "950", "970", "980", "Backordered"],
    ["East", "Widget", "1100", "1150", "1200", "1250", "Stable"],
    ["West", "Gadget", "1000", "1020", "1040", "1050", "Promotion planned"],
]


def _read_tsv(path: Path):
    """Return list-of-list where each inner list is the tab-split line contents."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n").split("\t") for line in f.readlines()]


def test_dataset_directory_exists():
    assert DATASET_DIR.exists(), f"Required directory {DATASET_DIR} is missing."
    assert DATASET_DIR.is_dir(), f"{DATASET_DIR} exists but is not a directory."


def test_raw_sales_file_exists_and_contents():
    assert RAW_FILE.exists(), f"Required file {RAW_FILE} is missing."
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."

    # Ensure file ends with a single trailing newline
    with RAW_FILE.open("rb") as f_bin:
        raw_bytes = f_bin.read()
    assert raw_bytes.endswith(b"\n"), (
        f"{RAW_FILE} must be terminated with exactly one newline."
    )

    lines = _read_tsv(RAW_FILE)
    assert (
        len(lines) == 1 + len(DATA_ROWS)
    ), f"{RAW_FILE} should have 5 lines (1 header + 4 rows)."
    assert (
        lines[0] == HEADER
    ), f"Header of {RAW_FILE} is incorrect.\nExpected: {HEADER}\nFound   : {lines[0]}"

    for idx, expected_row in enumerate(DATA_ROWS, start=1):
        assert (
            lines[idx] == expected_row
        ), f"Row {idx} of {RAW_FILE} is incorrect.\nExpected: {expected_row}\nFound   : {lines[idx]}"


def test_trimmed_and_log_files_do_not_exist_yet():
    assert not TRIMMED_FILE.exists(), (
        f"{TRIMMED_FILE} should NOT exist before the student runs their command."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the student runs their command."
    )