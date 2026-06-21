# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before* the student
# starts working on the “log-cleanup” exercise.  These tests assert that the
# starting directory structure and files are present and that no output files
# have been created yet.  If any test fails, the student’s environment is
# incorrect or somebody has already begun modifying it.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_DIR = HOME / "datasets" / "log_cleanup"
RAW_FILE = DATA_DIR / "raw_web_events.log"
CLEANED_FILE = DATA_DIR / "cleaned_web_events.log"
PROCESSING_FILE = DATA_DIR / "processing.log"


@pytest.fixture(scope="module")
def raw_lines():
    """
    Return the list of lines in the raw Apache log file.

    The fixture raises an explicit assertion if the file cannot be read so that
    downstream tests fail with a clear, single root cause.
    """
    assert RAW_FILE.exists(), (
        f"Expected raw log file at {RAW_FILE}, but it does not exist."
    )
    assert RAW_FILE.is_file(), (
        f"Expected {RAW_FILE} to be a regular file, but it is not."
    )

    try:
        with RAW_FILE.open("r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {RAW_FILE}: {exc}")

    return lines


def test_log_cleanup_directory_exists():
    """The log-cleanup data directory must exist and be a directory."""
    assert DATA_DIR.exists(), (
        f"Directory {DATA_DIR} is missing. "
        "The dataset directory has to be present before starting the exercise."
    )
    assert DATA_DIR.is_dir(), (
        f"Expected {DATA_DIR} to be a directory, but something else exists at that path."
    )


def test_raw_log_file_present(raw_lines):
    """
    Ensure the raw input file exists and contains exactly the expected number of
    lines (15 lines according to the specification).
    """
    expected_line_count = 15
    actual = len(raw_lines)
    assert (
        actual == expected_line_count
    ), f"{RAW_FILE} should contain {expected_line_count} lines, but found {actual}."


def test_raw_log_file_is_non_empty(raw_lines):
    """A sanity-check that the raw log file is not empty."""
    assert raw_lines, f"{RAW_FILE} appears to be empty."


def test_output_files_absent():
    """
    Prior to running the student solution, the output artefacts must *not* yet
    exist.  Their presence would indicate that somebody has already generated
    results, which would invalidate the “initial state”.
    """
    assert not CLEANED_FILE.exists(), (
        f"Output file {CLEANED_FILE} already exists. "
        "Remove it to restore the initial state before starting the task."
    )

    assert not PROCESSING_FILE.exists(), (
        f"Output file {PROCESSING_FILE} already exists. "
        "Remove it to restore the initial state before starting the task."
    )