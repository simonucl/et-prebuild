# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present **before** the student performs any action.  It checks that:
#
# 1. The credential store directory exists and is a directory.
# 2. The CSV file containing the old and new API keys exists.
# 3. The CSV file’s contents match the exact specification
#    (4 lines, 4 comma-separated columns per line, correct order & values).
#
# NOTE: Per the grading rules, we intentionally do **not** test for the
#       presence or absence of any output artefacts (e.g.,
#       rotated_credentials.json).

import os
import stat
import pytest

CRED_DIR = "/home/user/credential_store"
CSV_PATH = os.path.join(CRED_DIR, "old_credentials.csv")

EXPECTED_LINES = [
    "service,username,old_api_key,new_api_key",
    "auth-service,svc-auth,x8fe21ef,NEW-API-KEY-001",
    "payment-gateway,svc-pay,98ab442b,NEW-API-KEY-002",
    "analytics-engine,svc-ana,44cc9911,NEW-API-KEY-003",
]


def test_credential_store_directory_exists():
    """The credential_store directory must exist and be a directory."""
    assert os.path.exists(
        CRED_DIR
    ), f"Required directory {CRED_DIR} is missing."
    assert os.path.isdir(
        CRED_DIR
    ), f"{CRED_DIR} exists but is not a directory."

    # Optional: basic permission sanity check—must at least be readable & executable.
    st_mode = os.stat(CRED_DIR).st_mode
    assert (
        st_mode & stat.S_IRUSR
    ), f"{CRED_DIR} is not readable by its owner (expected 0755 permissions)."
    assert (
        st_mode & stat.S_IXUSR
    ), f"{CRED_DIR} is not accessible/executable by its owner (expected 0755 permissions)."


def test_old_credentials_csv_exists():
    """The source CSV file must exist and be a regular file."""
    assert os.path.exists(
        CSV_PATH
    ), f"Required file {CSV_PATH} is missing."
    assert os.path.isfile(
        CSV_PATH
    ), f"{CSV_PATH} exists but is not a regular file."


def test_old_credentials_csv_content_exact():
    """The CSV file must contain exactly the expected 4 lines/4 columns."""
    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        content_lines = fh.read().splitlines()

    # Exact number of lines
    assert (
        len(content_lines) == 4
    ), f"{CSV_PATH} should contain 4 lines, found {len(content_lines)}."

    # Exact line-by-line comparison
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, content_lines), start=1):
        assert (
            expected == actual
        ), (
            f"Line {idx} of {CSV_PATH} does not match.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )

    # Ensure each line has exactly 4 comma-separated columns
    for idx, line in enumerate(content_lines, start=1):
        columns = line.split(",")
        assert (
            len(columns) == 4
        ), f"Line {idx} of {CSV_PATH} should have 4 columns, found {len(columns)}."