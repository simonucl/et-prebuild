# test_initial_state.py
#
# Pytest suite to validate the starting filesystem state for the
# “container cost-report” exercise *before* the student creates any
# new files or scripts.
#
# These tests assert that the provided input data and directory
# structure exactly match the specification.  Any failure pin-points
# precisely what is missing or malformed so the learner can correct
# their environment before beginning the task.
#
# Requirements verified:
#   • /home/user/container_usage/usage.log exists with the exact header
#     and five data rows shown in the spec.
#   • usage.log has permissions 600 (-rw-------).
#   • /home/user/bin/ exists as a directory.
#
# NOTE:  We intentionally DO NOT test for the presence of the
#        deliverables (generate_cost_report.sh or cost_report.txt)
#        because they have not been created yet.

import os
import stat
import csv
from pathlib import Path

USAGE_LOG_PATH = Path("/home/user/container_usage/usage.log")
BIN_DIR_PATH   = Path("/home/user/bin")

EXPECTED_LINES = [
    "container_id,image,cpu_percent,mem_mb,runtime_hours,cost_per_hour",
    "a1b2c3,nginx:1.21,15,128,50,0.05",
    "d4e5f6,redis:6,25,256,120,0.03",
    "g7h8i9,postgres:13,55,512,200,0.1",
    "j0k1l2,customapp:latest,65,1024,75,0.2",
    "m3n4o5,python:3.9,10,256,30,0.04",
]

def test_bin_directory_exists():
    """
    /home/user/bin must already exist so the student can place their
    script there.
    """
    assert BIN_DIR_PATH.exists(), f"Expected directory {BIN_DIR_PATH} is missing."
    assert BIN_DIR_PATH.is_dir(), f"{BIN_DIR_PATH} exists but is not a directory."

def test_usage_log_exists():
    """
    Verify the usage.log file exists and is a regular file.
    """
    assert USAGE_LOG_PATH.exists(), f"Expected file {USAGE_LOG_PATH} is missing."
    assert USAGE_LOG_PATH.is_file(), f"{USAGE_LOG_PATH} exists but is not a regular file."

def test_usage_log_permissions():
    """
    usage.log must have mode 600 so only the user can read/write it.
    """
    mode = USAGE_LOG_PATH.stat().st_mode
    expected_mode = stat.S_IRUSR | stat.S_IWUSR  # 0o600
    assert (mode & 0o777) == expected_mode, (
        f"{USAGE_LOG_PATH} should have permissions 600 "
        f"(rw-------) but has {oct(mode & 0o777)}."
    )

def test_usage_log_contents_exact_lines():
    """
    Validate that the file has exactly the six expected lines
    (header + 5 data rows) and that they are byte-for-byte correct.
    """
    with USAGE_LOG_PATH.open("r", encoding="utf-8") as fh:
        file_lines = [ln.rstrip("\n") for ln in fh.readlines()]

    # Helpful assertion messages:
    assert file_lines == EXPECTED_LINES, (
        "The contents of usage.log do not match the expected specification.\n"
        f"Expected lines:\n{EXPECTED_LINES}\n\nActual lines:\n{file_lines}"
    )

def test_usage_log_has_trailing_newline():
    """
    Many UNIX tools expect the final newline to be present.
    """
    with USAGE_LOG_PATH.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert last_byte == b"\n", "usage.log must end with a newline (\\n)."

def test_usage_log_is_valid_csv():
    """
    Perform a sanity check using the csv module:
    * Header has exactly six columns in the specified order.
    * Each data row also has six columns.
    """
    with USAGE_LOG_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    header = rows[0]
    expected_header = EXPECTED_LINES[0].split(",")
    assert header == expected_header, (
        "CSV header mismatch.\n"
        f"Expected: {expected_header}\nActual:   {header}"
    )

    data_rows = rows[1:]
    assert len(data_rows) == 5, (
        f"Expected 5 data rows, found {len(data_rows)}."
    )
    for idx, row in enumerate(data_rows, start=1):
        assert len(row) == 6, (
            f"Row {idx} ('{','.join(row)}') should have 6 columns "
            f"but has {len(row)}."
        )