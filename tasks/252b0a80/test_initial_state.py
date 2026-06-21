# test_initial_state.py
#
# Pytest suite to assert the machine is in the expected *initial* state
# BEFORE the student starts the assignment.
#
# What we check:
# 1. /home/user/data exists and is a directory with mode 0755.
# 2. /home/user/data/sales.csv exists, is a regular file with mode 0644,
#    has exactly 10 lines and the expected demo contents.
# 3. /home/user/process_log.txt must **NOT** exist yet.
#
# If any of these conditions fail the tests will raise a clear assertion
# error so the learner immediately knows what prerequisite is missing.

import os
import stat
import pytest

DATA_DIR = "/home/user/data"
CSV_PATH = os.path.join(DATA_DIR, "sales.csv")
PROCESS_LOG = "/home/user/process_log.txt"

EXPECTED_LINES = [
    "order_id,region,amount\n",
    "1,North,1200\n",
    "2,South,850\n",
    "3,East,990\n",
    "4,West,640\n",
    "5,North,1330\n",
    "6,South,720\n",
    "7,East,560\n",
    "8,West,410\n",
    "9,North,1500\n",
]


@pytest.fixture(scope="module")
def csv_stat():
    """Return os.stat_result for the CSV file; skip tests cleanly if missing."""
    if not os.path.exists(CSV_PATH):
        pytest.skip(f"Required file {CSV_PATH} does not exist.")
    return os.stat(CSV_PATH)


def test_data_directory_exists():
    assert os.path.exists(DATA_DIR), f"Required directory {DATA_DIR} is missing."
    assert os.path.isdir(DATA_DIR), f"{DATA_DIR} exists but is not a directory."

    mode = stat.S_IMODE(os.stat(DATA_DIR).st_mode)
    expected_mode = 0o755
    assert (
        mode == expected_mode
    ), f"{DATA_DIR} should have permissions 755, found {oct(mode)}."


def test_sales_csv_exists(csv_stat):
    assert os.path.isfile(
        CSV_PATH
    ), f"Expected regular file {CSV_PATH} is missing or not a file."

    mode = stat.S_IMODE(csv_stat.st_mode)
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"{CSV_PATH} should have permissions 644, found {oct(mode)}."


def test_sales_csv_content():
    """Validate the demo CSV contents match the specification exactly."""
    assert os.path.exists(
        CSV_PATH
    ), f"File {CSV_PATH} is missing; cannot validate contents."

    with open(CSV_PATH, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    # Check number of lines first for a concise failure
    assert (
        len(lines) == len(EXPECTED_LINES)
    ), f"{CSV_PATH} should contain {len(EXPECTED_LINES)} lines but has {len(lines)}."

    # Now compare complete content line–by–line
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        assert (
            actual == expected
        ), f"Line {idx} of {CSV_PATH} is incorrect.\nExpected: {expected!r}\nFound   : {actual!r}"


def test_process_log_not_present():
    assert not os.path.exists(
        PROCESS_LOG
    ), f"{PROCESS_LOG} already exists—student must create it during the assignment, not beforehand."