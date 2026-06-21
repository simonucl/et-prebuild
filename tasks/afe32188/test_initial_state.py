# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student starts working on the assignment.
#
# It explicitly checks only the pre-existing data that the task
# description guarantees to be present and **does not** look for any
# artefacts that the student is supposed to create later.

import os
import textwrap
import pytest

CSV_PATH = "/home/user/data/db_backups_2023.csv"

EXPECTED_CSV_CONTENT = textwrap.dedent(
    """\
    database,last_backup,size_mb
    customers,2023-11-15T14:03:00Z,512
    orders,2023-10-01T02:11:00Z,256
    inventory,2023-11-29T05:45:00Z,128
    analytics,2023-09-20T00:00:00Z,2048
    sessions,2023-11-30T12:00:00Z,64
    """
)

@pytest.fixture(scope="module")
def csv_contents():
    """
    Read the CSV file once for all tests.
    """
    if not os.path.exists(CSV_PATH):
        pytest.skip(f"Expected CSV file {CSV_PATH} does not exist in this environment.")
    with open(CSV_PATH, "r", encoding="utf-8") as fp:
        return fp.read()

def test_csv_file_exists():
    """
    The database backup listing CSV must exist and be a regular file.
    """
    assert os.path.exists(CSV_PATH), (
        f"Required file {CSV_PATH} is missing."
    )
    assert os.path.isfile(CSV_PATH), (
        f"Expected {CSV_PATH} to be a regular file, but it's not."
    )

def test_csv_exact_content(csv_contents):
    """
    The content of the CSV must match the specification exactly,
    including newlines.
    """
    # Normalize the expected string to ensure it ends with a single LF.
    expected = EXPECTED_CSV_CONTENT
    assert csv_contents == expected, (
        "The contents of /home/user/data/db_backups_2023.csv do not match "
        "the expected data defined in the task description.\n"
        "If the file was modified, restore it to the original state before "
        "running the solution."
    )

def test_csv_row_count(csv_contents):
    """
    Sanity-check: the CSV must have a header plus exactly 5 data rows.
    """
    lines = csv_contents.strip("\n").split("\n")
    assert len(lines) == 6, (
        f"Expected 6 lines (header + 5 rows) in {CSV_PATH}, "
        f"found {len(lines)}."
    )