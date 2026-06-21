# test_initial_state.py
#
# This pytest suite validates the initial, pre-task state of the filesystem.
# It makes sure that the raw log directory and the three expected “.log”
# files exist and that the textual content of those log files exactly matches
# what the subsequent grading logic relies on.
#
# NOTE:  Per project rules we deliberately do **not** check for the existence
#        (or absence) of any output / summary artefacts; we only assert the
#        presence and correctness of the raw inputs.

import os
import textwrap
import pytest

RAW_DIR = "/home/user/test_results/raw_logs"

# --------------------------------------------------------------------------- #
# Helper data: the exact expected content of each raw log file as a list of
# individual lines (sans trailing newline characters).
# --------------------------------------------------------------------------- #
EXPECTED_LOGS = {
    "run1.log": textwrap.dedent(
        """\
        [2024-01-01 10:00:00] INFO Starting test suite
        [2024-01-01 10:00:01] TESTCASE: login_functionality RESULT: PASS TIME: 1.2
        [2024-01-01 10:00:02] TESTCASE: payment_gateway RESULT: FAIL TIME: 3.8
        [2024-01-01 10:00:03] INFO Suite finished"""
    ).splitlines(),
    "run2.log": textwrap.dedent(
        """\
        [2024-01-01 11:00:00] INFO Starting test suite
        [2024-01-01 11:00:01] TESTCASE: search_functionality RESULT: PASS TIME: 0.9
        [2024-01-01 11:00:02] TESTCASE: checkout_process RESULT: PASS TIME: 2.5
        [2024-01-01 11:00:03] ERROR Unexpected timeout in payment_gateway
        [2024-01-01 11:00:04] INFO Suite finished"""
    ).splitlines(),
    "run3.log": textwrap.dedent(
        """\
        [2024-01-01 12:00:00] INFO Starting test suite
        [2024-01-01 12:00:01] TESTCASE: user_profile RESULT: PASS TIME: 1.7
        [2024-01-01 12:00:02] TESTCASE: password_reset RESULT: PASS TIME: 2.1
        [2024-01-01 12:00:03] INFO Suite finished"""
    ).splitlines(),
}

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_raw_logs_directory_exists():
    assert os.path.isdir(
        RAW_DIR
    ), f"Required directory '{RAW_DIR}' is missing or is not a directory."


@pytest.mark.parametrize("filename", EXPECTED_LOGS.keys())
def test_each_log_file_exists(filename):
    path = os.path.join(RAW_DIR, filename)
    assert os.path.isfile(
        path
    ), f"Expected log file '{path}' is missing."


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_LOGS.items())
def test_log_file_content_exact_match(filename, expected_lines):
    """
    Compare each file’s content line-by-line (ignoring the trailing newline that
    most editors add). This guards against accidental edits in the fixture
    directory that would break downstream parsing logic.
    """
    path = os.path.join(RAW_DIR, filename)

    # Read raw file, strip one trailing newline if present, then split lines.
    with open(path, "r", encoding="utf-8") as fh:
        raw_text = fh.read()

    actual_lines = raw_text.rstrip("\n").splitlines()

    assert (
        actual_lines == expected_lines
    ), (
        f"Content mismatch in '{path}'.\n"
        "Expected:\n"
        + "\n".join(expected_lines)
        + "\n\nActual:\n"
        + "\n".join(actual_lines)
    )