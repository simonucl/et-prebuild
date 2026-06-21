# test_initial_state.py
#
# Pytest suite verifying the initial state of the filesystem **before**
# the student starts working on the task.  Specifically, we ensure that
# the flat-file “database” /home/user/user_db.csv exists and contains
# the exact, line-by-line contents required by the assignment.
#
# NO checks are made for any output/solution files or directories.

import os
import pytest

DB_PATH = "/home/user/user_db.csv"

# The exact contents the CSV file must have, line-by-line.
EXPECTED_LINES = [
    "username,uid,gid,status,fullname,home",
    "john,1001,100,active,John Doe,/home/john",
    "mary,1002,100,inactive,Mary Smith,/home/mary",
    "alice,1003,100,active,Alice Jones,/home/alice",
    "bob,1004,100,active,Bob Brown,/home/bob",
    "eve,1005,100,inactive,Eve Adams,/home/eve",
]


def test_user_db_file_exists():
    """
    The CSV database file must exist at the exact absolute path expected.
    """
    assert os.path.isfile(
        DB_PATH
    ), f"Required database file not found: {DB_PATH!r}"


@pytest.mark.dependency(depends=["test_user_db_file_exists"])
def test_user_db_contents_are_exact():
    """
    The CSV database file must contain exactly the six data lines plus the
    header line shown in the specification—nothing more, nothing less.
    """
    with open(DB_PATH, "r", encoding="utf-8") as fh:
        actual_lines = [line.rstrip("\n") for line in fh]

    # Helpful diff in assertion message if something is off.
    assert (
        actual_lines == EXPECTED_LINES
    ), (
        "Contents of /home/user/user_db.csv do not match the required "
        "initial state.\n"
        "Expected:\n"
        f"{EXPECTED_LINES}\n"
        "Actual:\n"
        f"{actual_lines}"
    )