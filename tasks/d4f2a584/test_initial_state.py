# test_initial_state.py
#
# This test-suite validates the pre-exercise state of the filesystem.
# It asserts that the directory /home/user/test_data/ exists, that it
# contains exactly one file called test_results.csv, and that this CSV
# file’s content matches the specification given in the task
# description.  These checks guarantee that students start from the
# expected clean slate.

import os
import pytest

HOME_DIR = "/home/user"
TEST_DIR = os.path.join(HOME_DIR, "test_data")
CSV_PATH = os.path.join(TEST_DIR, "test_results.csv")


@pytest.fixture(scope="module")
def csv_contents():
    """Return the contents of test_results.csv as a list of stripped lines."""
    if not os.path.isfile(CSV_PATH):
        pytest.skip(f"{CSV_PATH} is missing – cannot read contents.")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]


def test_test_data_directory_exists():
    assert os.path.isdir(TEST_DIR), (
        f"Required directory {TEST_DIR} is missing. "
        "Create it before proceeding with the exercise."
    )


def test_directory_contains_only_csv():
    assert os.path.exists(TEST_DIR), f"{TEST_DIR} does not exist."

    entries = sorted(os.listdir(TEST_DIR))
    assert entries, f"{TEST_DIR} is empty; expected {CSV_PATH}."

    assert entries == ["test_results.csv"], (
        f"{TEST_DIR} must contain exactly one file 'test_results.csv' and nothing else.\n"
        f"Current contents: {entries}"
    )


def test_csv_file_exists():
    assert os.path.isfile(CSV_PATH), (
        f"Required file {CSV_PATH} is missing. "
        "It should be present before the task begins."
    )


def test_csv_content(csv_contents):
    expected_lines = [
        "TC_ID,Status",
        "TC001,PASS",
        "TC002,FAIL",
        "TC003,PASS",
        "TC004,FAIL",
        "TC005,SKIP",
        "TC006,FAIL",
        "TC007,PASS",
        "TC008,SKIP",
        "TC009,PASS",
        "TC010,PASS",
    ]

    assert csv_contents == expected_lines, (
        f"{CSV_PATH} does not match the expected initial content.\n\n"
        "Expected lines:\n"
        + "\n".join(expected_lines)
        + "\n\nActual lines:\n"
        + "\n".join(csv_contents)
        + "\n\nEnsure the file is unmodified before starting the task."
    )