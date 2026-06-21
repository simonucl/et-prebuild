# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “awk & sed QA-reports” assignment _before_ the student writes
# any solution code.
#
# What we expect _to exist_ when the student starts:
#   • /home/user/qa_reports/            (directory)
#   • /home/user/qa_reports/run1.log   (file)
#   • /home/user/qa_reports/run2.log   (file)
#   • /home/user/qa_reports/run3.log   (file)
#
# What we expect _NOT_ to exist yet:
#   • /home/user/qa_reports/failed/    (directory, will be created later)
#   • /home/user/qa_reports/summary.csv
#
# We also verify that the three raw *.log files contain the exact lines that
# the assignment text claims they do—no more, no less—so that follow-up tests
# can rely on their content.
#
# NOTE:
#   • Only Python’s standard library plus pytest is used.
#   • All “missing/extra” situations produce clear assertion messages.

import os
from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/qa_reports")

# --------------------------------------------------------------------------- #
# Fixtures & helpers                                                          #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def expected_logs():
    """
    Return a mapping filename -> list-of-expected-lines (without trailing \n).
    """
    return {
        "run1.log": [
            "2023-07-01 10:00:01 [INFO] TESTCASE Login PASS",
            "2023-07-01 10:00:05 [INFO] TESTCASE Logout PASS",
            "2023-07-01 10:00:07 [INFO] TESTCASE ProfileUpdate FAIL",
            "2023-07-01 10:00:10 [INFO] Environment cleanup complete",
        ],
        "run2.log": [
            "2023-07-01 11:00:01 [INFO] TESTCASE Signup PASS",
            "2023-07-01 11:00:05 [INFO] TESTCASE PasswordReset FAIL",
            "2023-07-01 11:00:07 [INFO] TESTCASE TwoFactorAuth FAIL",
            "2023-07-01 11:00:10 [INFO] Environment cleanup complete",
        ],
        "run3.log": [
            "2023-07-01 12:00:01 [INFO] TESTCASE Search PASS",
            "2023-07-01 12:00:05 [INFO] TESTCASE AddToCart PASS",
            "2023-07-01 12:00:07 [INFO] TESTCASE Checkout PASS",
            "2023-07-01 12:00:10 [INFO] Environment cleanup complete",
        ],
    }


def read_log_lines(path: Path):
    """
    Read a text file and return its lines stripped from their trailing newlines.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected directory {BASE_DIR} to exist. "
        "Create it and put the raw *.log files there."
    )


@pytest.mark.parametrize("fname", ["run1.log", "run2.log", "run3.log"])
def test_raw_log_files_exist(fname):
    path = BASE_DIR / fname
    assert path.is_file(), f"Missing mandatory log file: {path}"


def test_failed_directory_not_yet_present():
    failed_dir = BASE_DIR / "failed"
    assert not failed_dir.exists(), (
        f"{failed_dir} should NOT exist before the student runs their solution "
        "—it will be created by the assignment script."
    )


def test_summary_csv_not_yet_present():
    csv_path = BASE_DIR / "summary.csv"
    assert not csv_path.exists(), (
        f"{csv_path} should NOT exist before the student runs their solution."
    )


def test_log_file_contents(expected_logs):
    """
    Verify that each *.log file contains exactly the expected four lines
    (including order and text).  This guarantees that downstream checks can
    rely on predictable input.
    """
    for fname, expected_lines in expected_logs.items():
        path = BASE_DIR / fname
        actual_lines = read_log_lines(path)

        # 1. Check line count first—gives a clearer error if the file is too
        #    short/long.
        assert len(actual_lines) == len(
            expected_lines
        ), f"{fname} should have {len(expected_lines)} lines, found {len(actual_lines)}."

        # 2. Check each line verbatim.
        for idx, (exp, act) in enumerate(zip(expected_lines, actual_lines), start=1):
            assert (
                exp == act
            ), f"Mismatch in {fname} at line {idx}:\n  expected: {exp!r}\n  actual:   {act!r}"