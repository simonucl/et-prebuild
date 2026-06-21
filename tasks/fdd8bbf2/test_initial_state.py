# test_initial_state.py
#
# This pytest suite validates that the OS / filesystem is in the expected
# initial state *before* the student performs any action for the “disk
# reports” exercise.  It checks that:
#
# 1. The /home/user/disk_reports directory exists.
# 2. The three source CSV files (server_a/b/c.csv) exist and contain the
#    exact expected data (header + three data rows each).
# 3. No output artefacts (combined_usage.csv, high_usage.json, process.log)
#    are present yet.
#
# Failing tests will provide clear, actionable messages.

import csv
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/disk_reports").resolve()

# --------------------------------------------------------------------------- #
# Helper data – the exact expected contents of the three input CSV files
# --------------------------------------------------------------------------- #

EXPECTED_CSV_CONTENT = {
    "server_a.csv": [
        ["mount_point", "total_gb", "used_gb"],
        ["/", "50", "30"],
        ["/home", "200", "150"],
        ["/var", "100", "90"],
    ],
    "server_b.csv": [
        ["mount_point", "total_gb", "used_gb"],
        ["/", "60", "20"],
        ["/home", "250", "240"],
        ["/opt", "80", "30"],
    ],
    "server_c.csv": [
        ["mount_point", "total_gb", "used_gb"],
        ["/", "40", "35"],
        ["/data", "500", "450"],
        ["/backup", "300", "100"],
    ],
}

OUTPUT_FILES = [
    "combined_usage.csv",
    "high_usage.json",
    "process.log",
]

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Expected directory {BASE_DIR} to exist."


@pytest.mark.parametrize("filename", list(EXPECTED_CSV_CONTENT))
def test_input_file_exists(filename):
    fpath = BASE_DIR / filename
    assert fpath.is_file(), f"Expected input file {fpath} to exist."


@pytest.mark.parametrize("filename", list(EXPECTED_CSV_CONTENT))
def test_input_file_contents_exact(filename):
    """
    Ensure each CSV file contains exactly the expected header and data rows,
    in the correct order, with integer‐like numeric values stored as strings.
    """
    fpath = BASE_DIR / filename
    with fpath.open(newline="") as fh:
        reader = list(csv.reader(fh))
    expected = EXPECTED_CSV_CONTENT[filename]
    assert reader == expected, (
        f"Contents of {fpath} do not match the expected initial data.\n"
        f"Expected:\n{expected}\nGot:\n{reader}"
    )


@pytest.mark.parametrize("filename", list(EXPECTED_CSV_CONTENT))
def test_input_file_numeric_fields_are_ints(filename):
    """
    Verify that total_gb and used_gb fields contain integers (no floats,
    no extra whitespace).
    """
    fpath = BASE_DIR / filename
    with fpath.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            for field in ("total_gb", "used_gb"):
                value = row[field]
                assert value.isdigit(), (
                    f"Field '{field}' in {fpath} must be an integer. "
                    f"Got '{value}' in row {row}"
                )


@pytest.mark.parametrize("filename", OUTPUT_FILES)
def test_output_files_do_not_exist_yet(filename):
    """
    The student has not run their consolidation script yet, so none of the
    expected output artefacts should exist.
    """
    fpath = BASE_DIR / filename
    assert not fpath.exists(), (
        f"Output file {fpath} already exists, but it should be created only "
        "after the student runs their solution."
    )