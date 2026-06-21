# test_initial_state.py
#
# This test-suite validates that the *initial* operating-system state
# is correct **before** the student launches the throw-away web-server.
#
# What we check for:
#   1. The directory  /home/user/datasets  exists, is a directory,
#      and is readable/executable by the current user.
#   2. The file       /home/user/datasets/sales.csv  exists,
#      is readable, and contains the exact 3 CSV lines specified in
#      the task description.
#
# We deliberately do *not* test for the web-server process or the
# log-file, because those are created *after* the student’s actions.

import os
import stat
from pathlib import Path

import pytest


DATASET_DIR = Path("/home/user/datasets")
SALES_CSV   = DATASET_DIR / "sales.csv"

EXPECTED_SALES_LINES = [
    "date,region,sales",
    "2023-01-01,North,100",
    "2023-01-02,South,150",
]


def _assert_access(path: Path, mode: int, what: str) -> None:
    """
    Helper that asserts `path` grants the given access `mode`
    (e.g. os.R_OK | os.X_OK).  `what` is a human-readable label
    used in assertion messages.
    """
    if not os.access(path, mode):
        perms = [
            ("readable", os.R_OK),
            ("writable", os.W_OK),
            ("executable", os.X_OK),
        ]
        missing = [name for name, bit in perms if mode & bit and not os.access(path, bit)]
        pytest.fail(
            f"{what} {path} exists but is not {' and '.join(missing)} for the current user."
        )


def test_dataset_directory_exists_and_is_accessible():
    """
    The directory /home/user/datasets must exist, be a directory,
    and be readable + executable by the current user.
    """
    assert DATASET_DIR.exists(), (
        f"Required directory {DATASET_DIR} does not exist. "
        "The starter dataset directory must be present before starting the task."
    )
    assert DATASET_DIR.is_dir(), (
        f"{DATASET_DIR} exists but is not a directory. "
        "It must be a directory containing the cleaned CSV files."
    )
    # User must be able to list (read) and traverse (execute) the directory.
    _assert_access(DATASET_DIR, os.R_OK | os.X_OK, "Directory")


def test_sales_csv_exists_and_contents_are_correct():
    """
    Verify that /home/user/datasets/sales.csv exists, is readable,
    and contains the exact 3 lines specified in the task text.
    """
    assert SALES_CSV.exists(), (
        f"CSV file {SALES_CSV} is missing. "
        "It must be present so that the forthcoming web-server can serve it."
    )
    assert SALES_CSV.is_file(), f"{SALES_CSV} exists but is not a regular file."

    _assert_access(SALES_CSV, os.R_OK, "CSV file")

    # Read and validate contents.
    content_bytes = SALES_CSV.read_bytes()
    try:
        content_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"CSV file {SALES_CSV} is not valid UTF-8: {exc}. "
            "It must be UTF-8 encoded plain text."
        )

    lines = [line.rstrip("\r\n") for line in content_text.splitlines()]
    assert lines == EXPECTED_SALES_LINES, (
        f"Contents of {SALES_CSV} do not match the expected data.\n"
        f"Expected lines:\n{EXPECTED_SALES_LINES!r}\n"
        f"Actual lines:\n{lines!r}"
    )