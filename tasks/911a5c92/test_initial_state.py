# test_initial_state.py
#
# This test-suite validates the initial state of the grading container **before**
# the student performs any actions.  It checks for:
#
# 1. Presence of the expected data directory.
# 2. Presence of the CSV data file.
# 3. Exact, line-by-line contents of that CSV file.
# 4. Correct kernel/OS name reported by `uname -s`.
#
# NOTE:
# • We deliberately do *not* check for /home/user/output or any artefacts that
#   will be created by the student, per the instructions.

import os
import subprocess
import pytest


DATA_DIR = "/home/user/data"
CSV_FILE = os.path.join(DATA_DIR, "transactions.csv")
EXPECTED_CSV_LINES = [
    "id,product,quantity,price",
    "1,Widget,3,9.99",
    "2,Gadget,2,19.50",
    "3,Doodad,5,4.00",
]
EXPECTED_OS_NAME = "Linux"


def test_data_directory_exists():
    assert os.path.isdir(
        DATA_DIR
    ), f"Required directory {DATA_DIR!r} is missing. It must exist before the student begins."


def test_transactions_csv_exists():
    assert os.path.isfile(
        CSV_FILE
    ), f"Required CSV file {CSV_FILE!r} is missing. It must be present before the student begins."


def test_transactions_csv_content_exact_match():
    with open(CSV_FILE, "r", newline="") as fh:
        lines = fh.read().splitlines()

    # Fail fast with a helpful diff if the content is wrong
    assert (
        lines == EXPECTED_CSV_LINES
    ), (
        f"CSV file {CSV_FILE!r} does not contain the expected contents.\n"
        f"Expected ({len(EXPECTED_CSV_LINES)} lines):\n{EXPECTED_CSV_LINES}\n\n"
        f"Found ({len(lines)} lines):\n{lines}"
    )


def test_uname_s_returns_linux():
    try:
        os_name = (
            subprocess.check_output(["uname", "-s"], text=True, stderr=subprocess.STDOUT)
            .strip()
        )
    except FileNotFoundError as exc:
        pytest.fail(f"'uname' command not found: {exc}")

    assert (
        os_name == EXPECTED_OS_NAME
    ), f"Kernel/OS name mismatch: expected {EXPECTED_OS_NAME!r}, got {os_name!r}"