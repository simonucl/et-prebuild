# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state
# matches the specification *before* the learner begins any work.
# It intentionally does NOT check for the presence or absence of any
# output files or directories the learner is expected to create later.

import pathlib
import pytest
import os

# --------- Constants describing the expected initial fixture ---------

DATA_DIR = pathlib.Path("/home/user/data")
USAGE_REPORT = DATA_DIR / "usage_report.tsv"

# Exact, byte-for-byte content expected in the fixture file.
EXPECTED_CONTENT = (
    "Timestamp\tServerID\tCPU_Usage\tMem_Usage\tDisk_Usage\tNetwork_In\tNetwork_Out\n"
    "2023-07-01T00:15:00Z\tsrv-001\t52.5\t68.2\t70.1\t120.4\t98.6\n"
    "2023-07-01T00:15:00Z\tsrv-002\t33.0\t44.5\t60.0\t80.2\t60.0\n"
    "2023-07-01T00:15:00Z\tsrv-003\t85.2\t90.1\t88.5\t200.1\t150.2\n"
    "2023-07-01T00:15:00Z\tsrv-004\t10.5\t25.3\t30.5\t40.4\t30.1\n"
    "2023-07-01T00:15:00Z\tsrv-005\t67.7\t75.0\t79.2\t130.2\t110.7\n"
).encode("utf-8")


# ------------------------------- Tests --------------------------------

def test_data_directory_exists():
    """Ensure /home/user/data directory already exists."""
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "The initial fixture directory must be present before starting the task."
    )


def test_usage_report_file_exists_and_is_file():
    """Verify that the TSV fixture file exists and is a regular file."""
    assert USAGE_REPORT.exists(), (
        f"Expected file {USAGE_REPORT} does not exist. "
        "Without this file the learner cannot complete the exercise."
    )
    assert USAGE_REPORT.is_file(), (
        f"{USAGE_REPORT} exists but is not a regular file."
    )


def test_usage_report_file_readable():
    """The fixture file must be readable by the current process."""
    can_read = os.access(USAGE_REPORT, os.R_OK)
    assert can_read, (
        f"Cannot read {USAGE_REPORT}. "
        "Check file permissions; it should be world-readable (mode 0644 or similar)."
    )


def test_usage_report_content_exact_match():
    """
    The fixture file must match the exact expected content, including:
      • Tab delimiters (0x09 bytes)
      • A final LF (0x0A) newline on each line
      • Exactly six lines (one header + five data)
    """
    actual = USAGE_REPORT.read_bytes()
    assert actual == EXPECTED_CONTENT, (
        f"The content of {USAGE_REPORT} does not match the expected initial data.\n"
        "If you modified this file, restore it to the original state shown in the "
        "project description."
    )