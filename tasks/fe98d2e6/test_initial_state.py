# test_initial_state.py
#
# This test-suite validates the *pre-exercise* state of the filesystem for the
# “AWS EC2 cost for first week of June 2023” task.  It intentionally **avoids**
# checking for any output/work artefacts that the student is expected to
# create later on.  Only the raw input area is inspected.
#
# Requirements verified:
#   • /home/user/cloud_costs/raw/ exists and is a directory
#   • Exactly seven daily log files are present, one per day 2023-06-01 … 2023-06-07
#   • Each file contains the exact expected lines (no extra / missing / re-ordered
#     records, no header, no blank lines)
#
# The test fails with a clear message whenever something is missing or differs
# from the canonical specification.
#
# NOTE:  We deliberately do *not* look at /home/user/cloud_costs/work/ or
#        /home/user/cloud_costs/reports/ because those locations are meant to
#        be populated by the student’s solution code later on.

import pathlib
import pytest

BASE_DIR = pathlib.Path("/home/user/cloud_costs/raw")


# Canonical truth data: mapping from file name to an ordered list of log lines.
TRUTH_LOGS = {
    "2023-06-01.log": [
        "2023-06-01T01:15:30Z,EC2,us-east-1,0.120",
        "2023-06-01T02:45:10Z,S3,us-east-1,0.005",
        "2023-06-01T03:30:00Z,EC2,us-west-2,0.200",
    ],
    "2023-06-02.log": [
        "2023-06-02T13:00:00Z,EC2,us-east-1,0.150",
        "2023-06-02T15:30:00Z,EC2,us-east-1,0.200",
        "2023-06-02T16:00:00Z,S3,us-east-1,0.010",
    ],
    "2023-06-03.log": [
        "2023-06-03T23:59:59Z,EC2,us-east-1,0.300",
    ],
    "2023-06-04.log": [
        "2023-06-04T00:00:01Z,EC2,us-east-1,0.050",
        "2023-06-04T12:00:00Z,BigQuery,us-central1,2.500",
    ],
    "2023-06-05.log": [
        "2023-06-05T08:15:00Z,EC2,us-east-1,0.400",
        "2023-06-05T10:00:00Z,EC2,us-east-2,0.080",
    ],
    "2023-06-06.log": [
        "2023-06-06T14:00:00Z,S3,us-east-1,0.015",
        "2023-06-06T18:45:00Z,EC2,us-east-1,0.250",
    ],
    "2023-06-07.log": [
        "2023-06-07T23:59:00Z,EC2,us-east-1,0.500",
        "2023-06-07T23:59:30Z,EC2,us-east-1,0.100",
    ],
}


def _read_file_lines(path: pathlib.Path):
    """
    Read *all* lines from a text file and return them without trailing newlines.
    This neutralises differences in newline style and presence/absence of a final
    newline character.
    """
    return path.read_text().splitlines()


@pytest.fixture(scope="module")
def raw_dir():
    """Return the pathlib.Path object for the raw directory after basic sanity checks."""
    if not BASE_DIR.exists():
        pytest.fail(f"Required directory {BASE_DIR} is missing.")
    if not BASE_DIR.is_dir():
        pytest.fail(f"{BASE_DIR} exists but is not a directory.")
    return BASE_DIR


def test_expected_files_present(raw_dir):
    """
    Verify that exactly the seven expected .log files are present in the raw
    directory and nothing else has crept in.
    """
    expected = set(TRUTH_LOGS.keys())
    present = {p.name for p in raw_dir.iterdir() if p.is_file()}
    missing = expected - present
    extra = present - expected
    if missing:
        pytest.fail(
            "Missing expected log files in {0}: {1}".format(raw_dir, ", ".join(sorted(missing)))
        )
    if extra:
        pytest.fail(
            "Unexpected extra files present in {0}: {1}".format(raw_dir, ", ".join(sorted(extra)))
        )
    # If neither missing nor extra, the directory contents match expectation.


@pytest.mark.parametrize("filename,truth_lines", TRUTH_LOGS.items())
def test_file_contents(raw_dir, filename, truth_lines):
    """
    Confirm that each log file contains the exactly expected lines in order,
    with no extras or omissions.
    """
    file_path = raw_dir / filename
    assert file_path.exists(), f"Expected file {file_path} not found."
    assert file_path.is_file(), f"Path {file_path} exists but is not a regular file."

    actual_lines = _read_file_lines(file_path)

    assert (
        actual_lines == truth_lines
    ), f"Contents of {file_path} differ from the canonical specification."