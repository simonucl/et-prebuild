# test_initial_state.py
#
# Pytest suite that verifies the expected initial state of the filesystem
# before the student performs any action on the authentication log task.
#
# The tests intentionally DO NOT look for the output directory or file that
# the student is supposed to create.  They only assert the presence and
# correctness of the provided sample log file.

import os
from pathlib import Path

LOG_DIR = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "auth_sample.log"
TARGET_PHRASE = b"Failed password"  # bytes for binary comparison
EXPECTED_TOTAL_LINES = 7


def test_log_directory_exists_and_is_directory():
    """Ensure /home/user/logs exists and is a directory."""
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_log_file_exists_and_is_file():
    """Ensure /home/user/logs/auth_sample.log exists and is a regular file."""
    assert LOG_FILE.exists(), f"Required file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_contains_expected_number_of_lines_and_terminating_newlines():
    """
    1. Verify the log file has exactly EXPECTED_TOTAL_LINES lines.
    2. Each line must end with a newline character (\\n).
    3. The last byte of the file must be a newline as well.
    """
    with LOG_FILE.open("rb") as fh:
        contents = fh.read()

    # Make sure the file is not empty
    assert contents, f"{LOG_FILE} is empty."

    # Split into lines keeping the newline characters
    lines = contents.splitlines(keepends=True)
    assert (
        len(lines) == EXPECTED_TOTAL_LINES
    ), f"{LOG_FILE} should contain {EXPECTED_TOTAL_LINES} lines but has {len(lines)}."

    # Check each line ends with b'\n'
    for idx, line in enumerate(lines, start=1):
        assert line.endswith(
            b"\n"
        ), f"Line {idx} of {LOG_FILE} does not end with a newline (\\n)."

    # Verify the very last byte of the file is a newline
    assert contents.endswith(
        b"\n"
    ), f"The last byte of {LOG_FILE} must be a newline character (\\n)."


def test_log_file_failed_password_count_is_correct():
    """
    Count how many lines in the log file contain the exact phrase 'Failed password'
    and assert the count equals EXPECTED_TOTAL_LINES (7 in the provided truth table).
    """
    count = 0
    with LOG_FILE.open("rb") as fh:
        for line in fh:
            if TARGET_PHRASE in line:
                count += 1

    assert (
        count == EXPECTED_TOTAL_LINES
    ), (
        f"Expected {EXPECTED_TOTAL_LINES} occurrences of "
        f"'{TARGET_PHRASE.decode()}' in {LOG_FILE}, but found {count}."
    )