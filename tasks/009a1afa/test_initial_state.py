# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state that must be
# present before the student runs any commands for the assignment.
#
# Expectations:
#   1. The solver log file `/home/user/experiments/opt_solver/solver_run.log`
#      must already exist and contain exactly the seven CSV lines specified
#      in the task description (with LF line endings only).
#   2. The summary file `/home/user/experiments/opt_solver/summary.txt`
#      must NOT exist yet—students are supposed to create it later.
#
# Only the Python stdlib and pytest are used so that the tests run in every
# environment without additional dependencies.

import os
import pathlib
import pytest

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

HOME = pathlib.Path("/home/user")
EXP_DIR = HOME / "experiments" / "opt_solver"
LOG_FILE = EXP_DIR / "solver_run.log"
SUMMARY_FILE = EXP_DIR / "summary.txt"

EXPECTED_LOG_LINES = [
    "iteration,objective,elapsed_sec",
    "1,12.34,0.5",
    "2,7.89,1.0",
    "3,5.67,1.5",
    "4,4.56,2.0",
    "5,4.12,2.5",
    "final,4.12,2.5",
]


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: pathlib.Path) -> str:
    """
    Read a file *as bytes* first to make sure we don't have CRLF (`\r\n`)
    line endings; then decode as UTF-8.

    Raises clear assertion errors if CR characters are detected.
    """
    with path.open("rb") as fh:
        raw = fh.read()

    # Ensure there are no Windows-style line endings.
    assert b"\r" not in raw, (
        f"{path} must use LF (\\n) line endings only; "
        "carriage-return characters (\\r) were found."
    )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(f"{path} is not valid UTF-8: {exc}") from exc

    return text


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_log_file_exists():
    assert LOG_FILE.is_file(), (
        "Pre-existing solver log is missing.\n"
        f"Expected file: {LOG_FILE}\n"
        "Make sure the file is present **before** the student executes anything."
    )


def test_log_file_content_exact():
    # This test only runs if the file exists; marks failure otherwise.
    if not LOG_FILE.is_file():
        pytest.skip("Log file missing; content test skipped because existence test already fails.")

    text = read_text(LOG_FILE)
    lines = text.splitlines()

    assert lines == EXPECTED_LOG_LINES, (
        "The contents of the pre-existing solver log do not match the expected "
        "seven lines.\n\n"
        "Expected:\n"
        + "\n".join(EXPECTED_LOG_LINES)
        + "\n\nFound:\n"
        + "\n".join(lines)
    )

    # Optional: warn if there are trailing blanks at the end of file
    assert text.endswith("\n") or text.endswith("\n"), (
        f"{LOG_FILE} should end with a newline character (LF)."
    )


def test_summary_file_absent():
    assert not SUMMARY_FILE.exists(), (
        f"The summary file {SUMMARY_FILE} should NOT exist yet. "
        "Students are required to create it as part of the task, "
        "so the initial state must not contain this file."
    )