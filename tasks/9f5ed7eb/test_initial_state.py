# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the learner performs any actions.  It confirms that the required
# source data files are present and contain the exact expected contents.
#
# IMPORTANT:
# • We intentionally do NOT check for the existence (or non-existence) of
#   any files in /home/user/output because those are “output” artefacts
#   that will be created by the learner.
# • Only Python’s stdlib and pytest are used.

from pathlib import Path
import pytest

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def load_csv_lines(path: Path):
    """
    Read a CSV file and return a list of its lines without the trailing
    newline characters.  This makes comparison platform-agnostic while
    still asserting exact textual content for each line.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


# --------------------------------------------------------------------------- #
# Expected values for the two quarterly extracts
# --------------------------------------------------------------------------- #
EXPECTED_Q1_LINES = [
    "id,user_id,amount,status,date",
    "1,alice,120.00,COMPLETED,2023-01-15",
    "2,bob,75.50,FAILED,2023-02-03",
    "3,charlie,560.20,COMPLETED,2023-03-22",
]

EXPECTED_Q2_LINES = [
    "id,user_id,amount,status,date",
    "4,alice,310.00,FAILED,2023-04-02",
    "5,bob,40.00,COMPLETED,2023-05-14",
    "6,diana,88.10,FAILED,2023-06-30",
]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "file_path, expected_lines",
    [
        (Path("/home/user/compliance_data/transactions_q1.csv"), EXPECTED_Q1_LINES),
        (Path("/home/user/compliance_data/transactions_q2.csv"), EXPECTED_Q2_LINES),
    ],
)
def test_source_csv_files_exist_and_match_expected_content(file_path: Path, expected_lines):
    """
    Verify that the two source CSV files are present, readable, and that
    their byte content matches exactly what the project specification
    states they should contain.
    """
    # 1. Presence & type
    assert file_path.exists(), f"Required source file is missing: {file_path}"
    assert file_path.is_file(), f"Expected a regular file at {file_path}, but it is not a file."

    # 2. Content accuracy
    actual_lines = load_csv_lines(file_path)
    assert (
        actual_lines == expected_lines
    ), (
        f"File {file_path} does not match the expected contents.\n\n"
        "Expected lines:\n"
        + "\n".join(expected_lines)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
    )


def test_compliance_data_directory_exists():
    """
    Sanity-check that the parent directory for the source extracts exists.
    """
    dir_path = Path("/home/user/compliance_data")
    assert dir_path.exists(), f"Directory {dir_path} is missing."
    assert dir_path.is_dir(), f"Expected {dir_path} to be a directory."