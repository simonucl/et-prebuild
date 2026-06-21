# test_initial_state.py
#
# This pytest suite verifies that the initial operating-system / filesystem
# state required by the assignment is present **before** the student starts
# writing their solution.
#
# Rules we follow (see prompt):
#   • Only the *input* directory (/home/user/logs/) and its files are checked.
#   • We intentionally do **not** touch /home/user/output/ or any other
#     soon-to-be-generated artefacts.
#   • All paths are absolute and the tests are self-contained, relying on
#     nothing but the Python stdlib and pytest.
#
# If any of these tests fail, the student’s environment is not in the
# expected pristine state, so subsequent grading could be misleading.

import os
from pathlib import Path

import pytest


LOG_DIR = Path("/home/user/logs")

# Expected per-file contents (exact, without trailing newlines)
EXPECTED_FILES = {
    "service-auth.log": [
        "[2024-06-01 10:00:00] INFO User login successful",
        "[2024-06-01 10:01:00] ERROR Invalid credentials",
        "[2024-06-01 10:02:00] INFO Token issued",
        "[2024-06-01 10:03:00] ERROR Session expired",
        "[2024-06-01 10:04:00] ERROR Invalid credentials",
    ],
    "service-payment.log": [
        "[2024-06-01 10:05:00] INFO Payment initiated",
        "[2024-06-01 10:06:00] ERROR Card declined",
        "[2024-06-01 10:07:00] ERROR Timeout contacting bank",
        "[2024-06-01 10:08:00] INFO Payment retried",
        "[2024-06-01 10:09:00] ERROR Card declined",
    ],
    "service-order.log": [
        "[2024-06-01 10:10:00] INFO Order placed",
        "[2024-06-01 10:11:00] ERROR Inventory shortage",
        "[2024-06-01 10:12:00] ERROR Inventory shortage",
        "[2024-06-01 10:13:00] INFO Order cancelled",
        "[2024-06-01 10:14:00] ERROR Payment pending",
    ],
}


def read_file_lines(path: Path):
    """
    Helper that returns the file content as a list of lines *without*
    trailing newline characters.
    """
    with path.open("r", encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp.readlines()]


def test_logs_directory_present_and_is_directory():
    """Confirm `/home/user/logs/` exists and is a directory."""
    assert LOG_DIR.exists(), "Directory /home/user/logs/ is missing."
    assert LOG_DIR.is_dir(), "/home/user/logs/ exists but is not a directory."


@pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
def test_log_file_exists(filename):
    """Each expected .log file must exist."""
    full_path = LOG_DIR / filename
    assert full_path.exists(), f"Required log file {full_path} does not exist."
    assert full_path.is_file(), f"{full_path} exists but is not a regular file."


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES.items())
def test_log_file_contents_exact_match(filename, expected_lines):
    """
    The content of every log file must match the reference snapshot exactly.
    This guards against accidental mutations of the fixture data.
    """
    full_path = LOG_DIR / filename
    actual_lines = read_file_lines(full_path)

    assert (
        actual_lines == expected_lines
    ), f"Content mismatch in {full_path}. Expected lines:\n{expected_lines}\n\nActual lines:\n{actual_lines}"


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES.items())
def test_log_file_statistics(filename, expected_lines):
    """
    Validate per-file statistics that downstream tasks rely on:
      • total line count
      • ERROR line count
    """
    full_path = LOG_DIR / filename
    lines = read_file_lines(full_path)

    total_lines = len(lines)
    error_lines = sum(" ERROR " in line for line in lines)

    # Derive expected counts from the snapshot to avoid duplication errors
    expected_total = len(expected_lines)
    expected_error = sum(" ERROR " in line for line in expected_lines)

    assert (
        total_lines == expected_total
    ), f"{full_path}: expected {expected_total} total lines, found {total_lines}."
    assert (
        error_lines == expected_error
    ), f"{full_path}: expected {expected_error} ERROR lines, found {error_lines}."