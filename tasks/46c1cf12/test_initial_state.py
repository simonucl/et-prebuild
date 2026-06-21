# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student performs any action for the “compliance analyst”
# exercise.  Only standard library + pytest are used.

import os
import pytest

CSV_PATH = "/home/user/data/transactions.csv"

# The exact content that must already be present in the CSV file.
EXPECTED_CSV_CONTENT = (
    "transaction_id,account_id,amount,currency,status\n"
    "T1001,AC245,250.00,USD,COMPLETED\n"
    "T1002,AC367,1450.50,USD,PENDING\n"
    "T1003,AC578,322.10,EUR,FAILED\n"
    "T1004,AC245,78.45,USD,COMPLETED\n"
    "T1005,AC367,2300.00,USD,FAILED\n"
)


def test_transactions_csv_exists():
    """
    The source CSV with raw transactions must exist at the exact path and be a file.
    """
    assert os.path.exists(
        CSV_PATH
    ), f"Required CSV not found at {CSV_PATH}"
    assert os.path.isfile(
        CSV_PATH
    ), f"Expected {CSV_PATH} to be a file, but it is not."


def test_transactions_csv_contents():
    """
    The CSV must contain the precise, byte-for-byte contents specified in the task
    description (including trailing newline).
    """
    with open(CSV_PATH, "r", encoding="utf-8") as fp:
        actual = fp.read()

    # Helpful diff in case of mismatch
    assert actual == EXPECTED_CSV_CONTENT, (
        "The contents of /home/user/data/transactions.csv do not match the expected "
        "initial dataset.\n"
        "----- Expected -----\n"
        f"{EXPECTED_CSV_CONTENT}"
        "-----   Got   -----\n"
        f"{actual}"
    )