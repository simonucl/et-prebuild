# test_initial_state.py
#
# This test-suite validates the pristine operating-system / filesystem
# BEFORE the student’s solution is run.  It asserts that the required
# CSV file and directories are present with the exact expected content
# and that no output artefacts have been created yet.
#
# It must be executed prior to any modification of the filesystem.

import os
import stat
import pytest

HOME = "/home/user"
CSV_PATH = os.path.join(HOME, "network", "logs", "ping_results.csv")
REPORTS_DIR = os.path.join(HOME, "network", "reports")
JSON_OUT = os.path.join(REPORTS_DIR, "unreachable_summary.json")
LOG_OUT = os.path.join(REPORTS_DIR, "generation.log")


@pytest.fixture(scope="module")
def csv_contents():
    """Return the contents of the CSV file as a list of stripped lines."""
    if not os.path.isfile(CSV_PATH):
        pytest.fail(
            f"Required CSV file missing at {CSV_PATH!r}. "
            "Make sure the initial data has been provisioned."
        )
    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        return [line.rstrip("\n\r") for line in fh.readlines()]


def test_csv_file_exists_and_is_regular():
    assert os.path.isfile(CSV_PATH), (
        f"Expected CSV file {CSV_PATH!r} does not exist or is not a regular file."
    )
    # Extra safety: ensure it is not a symlink or device.
    mode = os.stat(CSV_PATH, follow_symlinks=False).st_mode
    assert stat.S_ISREG(mode), f"{CSV_PATH!r} should be a regular file."


def test_csv_file_contents(csv_contents):
    expected_lines = [
        "timestamp,host,latency_ms,packet_loss",
        "2023-07-01T10:00:00Z,host1.example.com,23,0",
        "2023-07-01T10:00:00Z,host2.example.com,,100",
        "2023-07-01T10:00:00Z,host3.example.com,45,0",
        "2023-07-01T10:00:00Z,host4.example.com,,100",
        "2023-07-01T10:00:00Z,host5.example.com,31,0",
    ]
    assert csv_contents == expected_lines, (
        "The contents of ping_results.csv do not match the expected initial dataset.\n"
        f"Expected:\n{expected_lines}\n\nGot:\n{csv_contents}"
    )


def test_reports_directory_exists_and_is_writable():
    assert os.path.isdir(REPORTS_DIR), (
        f"Reports directory {REPORTS_DIR!r} is missing. "
        "It must exist before the exercise starts."
    )
    assert os.access(REPORTS_DIR, os.W_OK), (
        f"Reports directory {REPORTS_DIR!r} is not writable by the current user."
    )


def test_reports_directory_is_empty_before_work():
    # Directory must contain no files yet.
    unexpected_items = os.listdir(REPORTS_DIR)
    assert not unexpected_items, (
        f"Reports directory {REPORTS_DIR!r} should be empty initially, "
        f"but found: {unexpected_items}"
    )


def test_output_files_do_not_exist_yet():
    for path in (JSON_OUT, LOG_OUT):
        assert not os.path.exists(path), (
            f"Output artefact {path!r} already exists before the student runs their solution."
        )