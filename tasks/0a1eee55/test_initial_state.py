# test_initial_state.py
#
# This pytest suite validates the *pre-exercise* state of the operating
# system / filesystem for the “capacity-planning analyst” task.  It checks
# that the required data directory and the three source CSV files are present
# and contain exactly the expected headers and rows.  These assertions ensure
# that the student starts from a known, correct baseline before creating any
# output artefacts.

import os
import textwrap

import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")

CPU_CSV = os.path.join(DATA_DIR, "resource_cpu.csv")
MEM_CSV = os.path.join(DATA_DIR, "resource_memory.csv")
DISK_CSV = os.path.join(DATA_DIR, "resource_disk.csv")

# --------------------------------------------------------------------------- #
# Expected file contents (verbatim, including final newline)
# --------------------------------------------------------------------------- #
CPU_EXPECTED = textwrap.dedent("""\
    timestamp,hostname,cpu_percent
    2023-07-01T00:00:00Z,web-1,55
    2023-07-01T01:00:00Z,web-1,60
    2023-07-01T00:00:00Z,db-1,75
    2023-07-01T01:00:00Z,db-1,70
    2023-07-01T00:00:00Z,worker-1,30
    2023-07-01T01:00:00Z,worker-1,40
""")

MEM_EXPECTED = textwrap.dedent("""\
    timestamp,hostname,mem_mb
    2023-07-01T00:00:00Z,web-1,2048
    2023-07-01T01:00:00Z,web-1,2100
    2023-07-01T00:00:00Z,db-1,4096
    2023-07-01T01:00:00Z,db-1,4200
    2023-07-01T00:00:00Z,worker-1,1024
    2023-07-01T01:00:00Z,worker-1,1100
""")

DISK_EXPECTED = textwrap.dedent("""\
    timestamp,hostname,disk_gb
    2023-07-01T00:00:00Z,web-1,120
    2023-07-01T01:00:00Z,web-1,121
    2023-07-01T00:00:00Z,db-1,300
    2023-07-01T01:00:00Z,db-1,302
    2023-07-01T00:00:00Z,worker-1,80
    2023-07-01T01:00:00Z,worker-1,81
""")

# Normalise expected strings: ensure they *all* terminate with exactly one "\n"
CPU_EXPECTED += "" if CPU_EXPECTED.endswith("\n") else "\n"
MEM_EXPECTED += "" if MEM_EXPECTED.endswith("\n") else "\n"
DISK_EXPECTED += "" if DISK_EXPECTED.endswith("\n") else "\n"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def assert_file_exists(path: str) -> None:
    """Assert that `path` exists and is a regular file."""
    assert os.path.exists(path), f"Expected file {path!r} is missing."
    assert os.path.isfile(path), f"Path {path!r} exists but is not a regular file."
    assert os.access(path, os.R_OK), f"File {path!r} exists but is not readable."


def read_file(path: str) -> str:
    """Return the full contents of `path`."""
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_data_directory_exists():
    assert os.path.exists(DATA_DIR), f"Required directory {DATA_DIR!r} is missing."
    assert os.path.isdir(DATA_DIR), f"Path {DATA_DIR!r} exists but is not a directory."
    # Basic sanity: it should be readable
    assert os.access(DATA_DIR, os.R_OK), f"Directory {DATA_DIR!r} is not readable."


@pytest.mark.parametrize(
    "csv_path,expected_content",
    [
        (CPU_CSV, CPU_EXPECTED),
        (MEM_CSV, MEM_EXPECTED),
        (DISK_CSV, DISK_EXPECTED),
    ],
)
def test_csv_file_presence_and_content(csv_path: str, expected_content: str):
    # 1) File exists and is readable
    assert_file_exists(csv_path)

    # 2) Content matches the ground-truth exactly
    actual = read_file(csv_path)
    assert (
        actual == expected_content
    ), f"Content mismatch in {csv_path!r}.\n\nExpected:\n{expected_content}\nActual:\n{actual}"

    # 3) Quick structural sanity: header must be first line with correct columns
    header = actual.splitlines()[0]
    expected_header = expected_content.splitlines()[0]
    assert (
        header == expected_header
    ), f"Header mismatch in {csv_path!r}: expected {expected_header!r} but found {header!r}"

    # 4) Ensure at least one data row exists beyond the header
    assert (
        len(actual.splitlines()) > 1
    ), f"File {csv_path!r} should contain data rows but only the header is present."


def test_no_output_directory_exists_yet():
    """
    The exercise instructions specify that the student *will* create
    /home/user/output and populate it.  Before they start, the output
    directory must *not* exist; otherwise the grader could pick up stale
    artefacts from a previous run.
    """
    output_dir = os.path.join(HOME, "output")
    assert not os.path.exists(
        output_dir
    ), f"Directory {output_dir!r} should not exist prior to the student's work."