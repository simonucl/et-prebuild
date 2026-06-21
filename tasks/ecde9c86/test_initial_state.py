# test_initial_state.py
#
# This pytest suite verifies that the operating‐system state **before**
# the student starts working on the assignment is exactly what the
# automated grader expects.
#
# WHAT WE CHECK
# 1. The input file /home/user/data/usage.tsv must exist and contain
#    exactly four tab-separated columns with the required header and
#    three data rows (4 lines total).
# 2. The work directory /home/user/capacity_planner **must not yet
#    exist** (or at least must not contain a Makefile or summary.log),
#    ensuring the student starts from a clean slate.
#
# No other checks are performed: we explicitly avoid asserting the
# existence of any artefacts that the student is supposed to create
# (Makefile, build directory, summary.log, …).

import os
from pathlib import Path

import pytest

# Constants
INPUT_FILE = Path("/home/user/data/usage.tsv")
WORK_DIR = Path("/home/user/capacity_planner")
MAKEFILE = WORK_DIR / "Makefile"
SUMMARY_LOG = WORK_DIR / "summary.log"

EXPECTED_HEADER = (
    "timestamp\tcpu_percent\tmem_percent\tdisk_percent"
)  # exact header row expected
EXPECTED_ROWS = 4  # 1 header + 3 data lines


def test_usage_file_present_and_correct():
    """Verify that the TSV input file exists and has the expected format."""
    assert INPUT_FILE.is_file(), (
        f"Required input file {INPUT_FILE} is missing. "
        "The assignment expects this file to be present before the student starts."
    )

    # Read all non-empty lines
    lines = [line.rstrip("\n") for line in INPUT_FILE.read_text().splitlines()]
    assert (
        len(lines) == EXPECTED_ROWS
    ), f"{INPUT_FILE} should contain {EXPECTED_ROWS} lines (1 header + 3 data), found {len(lines)}."

    # Check header
    header = lines[0]
    assert (
        header == EXPECTED_HEADER
    ), f"Header of {INPUT_FILE} is incorrect.\nExpected: {EXPECTED_HEADER!r}\nFound   : {header!r}"

    # Validate that each data row has exactly 4 columns separated by tabs
    for lineno, row in enumerate(lines[1:], start=2):  # start=2 for human-friendly line numbers
        cols = row.split("\t")
        assert len(cols) == 4, (
            f"Line {lineno} of {INPUT_FILE} should have 4 tab-separated columns, "
            f"found {len(cols)} columns instead."
        )
        # Simple type check: columns 2-4 should be numbers (int or float)
        for col_index, raw in enumerate(cols[1:], start=2):
            try:
                float(raw)
            except ValueError:
                raise AssertionError(
                    f"Line {lineno}, column {col_index} of {INPUT_FILE} "
                    f"should be numeric, got {raw!r}."
                )


def test_work_directory_absent_or_clean():
    """
    The /home/user/capacity_planner directory (and its artefacts) should
    NOT exist yet, because the student has not run their solution.
    """
    # Directory must not contain artefacts. If directory doesn't exist at all, that is fine.
    if not WORK_DIR.exists():
        # Nothing to assert: clean starting state.
        return

    # Directory exists – ensure it does NOT yet contain the output files.
    assert not MAKEFILE.exists(), (
        f"Found unexpected {MAKEFILE}. The initial state should not include any Makefile; "
        "students are expected to create it themselves."
    )
    assert not SUMMARY_LOG.exists(), (
        f"Found unexpected {SUMMARY_LOG}. The summary log must be produced by the student's Makefile, "
        "so it should be absent in the initial state."
    )

    # Additionally, ensure no build directory is present.
    build_dir = WORK_DIR / "build"
    assert not build_dir.exists(), (
        f"Found unexpected directory {build_dir}. The 'collect' target should create it, "
        "so it must not exist before the student begins."
    )