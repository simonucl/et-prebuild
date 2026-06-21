# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state before the student performs any actions for the “API performance
# summary” task.  If any of these tests fail, the environment is not in
# the expected starting condition.
#
# NOTE:
# • We deliberately *do not* check for the existence (or absence) of the
#   eventual output file `performance_summary.log`; the rules forbid
#   validating artefacts that the student has yet to create.
# • Only Python’s standard library and pytest are used.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
API_TEST_DIR = HOME / "api_test"
DATA_DIR = API_TEST_DIR / "data"
RAW_FILE = DATA_DIR / "response_samples.txt"


@pytest.fixture(scope="module")
def raw_file_contents():
    """
    Read the raw benchmark file once per test-session.

    Returns
    -------
    str
        Entire contents of `response_samples.txt` decoded as UTF-8.
    """
    # If the file does not exist, the assertion in the calling tests
    # will already have failed, but we defensively raise a clear error.
    if not RAW_FILE.is_file():
        raise FileNotFoundError(f"Expected raw data file not found: {RAW_FILE}")
    return RAW_FILE.read_text(encoding="utf-8")


def test_api_test_directory_exists():
    assert API_TEST_DIR.is_dir(), (
        f"Missing directory: {API_TEST_DIR}\n"
        "The base directory for the benchmark files must exist exactly "
        "at this path."
    )


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Missing directory: {DATA_DIR}\n"
        "The data directory should be present inside the api_test folder."
    )


def test_raw_file_exists():
    assert RAW_FILE.is_file(), (
        f"Missing file: {RAW_FILE}\n"
        "The raw benchmark data file must be present before work begins."
    )


def test_raw_file_contents_exact(raw_file_contents):
    expected = (
        "request_id,time_ms\n"
        "1,120\n"
        "2,110\n"
        "3,130\n"
        "4,115\n"
        "5,140\n"
        "6,125\n"
    )
    assert raw_file_contents == expected, (
        f"Contents of {RAW_FILE} do not match the expected initial data.\n\n"
        "Expected exactly:\n"
        "-----------------\n"
        f"{expected!r}\n"
        "-----------------\n"
        "But found:\n"
        "-----------------\n"
        f"{raw_file_contents!r}\n"
        "-----------------\n"
        "Ensure the file has precisely 7 lines and a single trailing "
        "newline, with no extra whitespace."
    )