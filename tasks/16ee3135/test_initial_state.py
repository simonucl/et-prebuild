# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state **before**
# the student performs any action for the “ERROR counter” task.
#
# Rules being enforced:
# 1. Required directories exist.
# 2. The analysis directory is empty (no output yet).
# 3. The system log exists with the exact, known contents.
# 4. Exactly three “ERROR” events are present in the log.

import os
import re
from pathlib import Path

HOME = Path("/home/user")
TICKETS_DIR = HOME / "tickets"
LOGS_DIR = TICKETS_DIR / "logs"
ANALYSIS_DIR = TICKETS_DIR / "analysis"
LOG_FILE = LOGS_DIR / "system.log"
OUTPUT_FILE = ANALYSIS_DIR / "error_summary.txt"

EXPECTED_LOG_LINES = [
    "2023-04-18 10:15:23 INFO User login successful",
    "2023-04-18 10:16:12 ERROR Database connection failed",
    "2023-04-18 10:17:01 WARN Disk space low",
    "2023-04-18 10:18:45 ERROR Timeout while fetching data",
    "2023-04-18 10:20:10 INFO User logout",
    "2023-04-18 10:22:05 ERROR Failed to send email",
]

ERROR_REGEX = re.compile(r"\bERROR\b")


def _read_file_lines(path: Path):
    """Return a list of lines **without** their trailing newline."""
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


def test_directories_exist_and_are_correct_type():
    assert TICKETS_DIR.is_dir(), (
        f"Required directory {TICKETS_DIR} is missing or not a directory."
    )
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} is missing or not a directory."
    )
    assert ANALYSIS_DIR.is_dir(), (
        f"Required directory {ANALYSIS_DIR} is missing or not a directory."
    )


def test_analysis_directory_is_empty():
    # Ensure the student has not produced any output yet.
    contents = list(ANALYSIS_DIR.iterdir())
    assert not contents, (
        f"{ANALYSIS_DIR} must be empty before the task starts; "
        f"found unexpected item(s): {[p.name for p in contents]}"
    )
    assert not OUTPUT_FILE.exists(), (
        f"Output file {OUTPUT_FILE} should not exist before the student runs "
        f"their command."
    )


def test_log_file_exists_with_expected_contents():
    assert LOG_FILE.is_file(), (
        f"Expected log file {LOG_FILE} does not exist."
    )

    lines = _read_file_lines(LOG_FILE)

    # 1. Exact number of lines matches expectation.
    assert len(lines) == len(EXPECTED_LOG_LINES), (
        f"{LOG_FILE} should contain {len(EXPECTED_LOG_LINES)} lines, "
        f"but {len(lines)} were found."
    )

    # 2. Content comparison line‐by‐line.
    for idx, (actual, expected) in enumerate(zip(lines, EXPECTED_LOG_LINES), start=1):
        assert actual == expected, (
            f"Line {idx} of {LOG_FILE} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}"
        )

    # 3. Ensure each original line terminated only with LF (already stripped).
    with LOG_FILE.open("rb") as fh:
        raw = fh.read()
    assert b"\r\n" not in raw, (
        f"{LOG_FILE} must use Unix LF (0x0A) line endings, "
        f"but CRLF sequences were detected."
    )

    # 4. Verify the number of ERROR lines is exactly three.
    error_matches = [line for line in lines if ERROR_REGEX.search(line)]
    assert len(error_matches) == 3, (
        f"{LOG_FILE} should contain exactly 3 lines with the whole word "
        f"'ERROR', but {len(error_matches)} such lines were found: {error_matches}"
    )