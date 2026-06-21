# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state that must be present *before* the student performs any action for the
# “backup integrity spot-check” task.
#
# What we assert:
#   1. Directory /home/user/backup_logs/ exists.
#   2. Exactly three .log files are present in that directory and *only* those
#      three (2023-10-21.log, 2023-10-22.log, 2023-10-23.log).
#   3. Every line in every file matches the strict log-line format.
#   4. Across all three files there are exactly four lines whose STATUS field
#      is “FAILED”.
#
# We deliberately **do not** test for the presence of any output files or
# directories that the student is supposed to create (`backup_analysis` etc.).
#
# The tests rely solely on Python’s standard library plus pytest.

import os
import re
from pathlib import Path

import pytest

BACKUP_DIR = Path("/home/user/backup_logs")
EXPECTED_FILES = {
    "2023-10-21.log",
    "2023-10-22.log",
    "2023-10-23.log",
}

# Pre-compiled regex for the exact log-line format
LOG_LINE_RE = re.compile(
    r"""
    ^                               # begin of line
    \d{4}-\d{2}-\d{2}               #   YYYY-MM-DD
    \s
    \d{2}:\d{2}:\d{2}               #   HH:MM:SS
    \s
    STATUS=(OK|FAILED)              #   status field
    \s+                             #   one or more spaces (alignment padding)
    SIZE=\d+                        #   SIZE=<bytes>
    \s+                             #   one or more spaces (alignment padding)
    SHA256=[0-9a-f]{64}             #   full 64-char hex digest
    $                               # end of line
    """,
    re.VERBOSE,
)


def read_lines(path: Path):
    """
    Helper that yields stripped lines from *binary-safe* reading of a file.

    We do not use Path.read_text() because we wish to preserve exact LF endings
    and still remain robust if the file is large.
    """
    with path.open("rt", encoding="utf-8", newline="\n") as fp:
        for line in fp:
            yield line.rstrip("\n")


@pytest.fixture(scope="module")
def log_files():
    """
    Collect the Path objects for all *.log files inside BACKUP_DIR.
    The fixture fails early if the directory does not exist.
    """
    if not BACKUP_DIR.is_dir():
        pytest.fail(
            f"Required directory {BACKUP_DIR} is missing. "
            "Expected it to exist and contain the raw log files."
        )

    log_paths = {p.name: p for p in BACKUP_DIR.glob("*.log")}
    return log_paths


def test_directory_and_file_set(log_files):
    """
    1. Directory /home/user/backup_logs/ must exist.
    2. It must contain *exactly* the three expected .log files—no more, no less.
    """
    found_names = set(log_files.keys())

    missing = EXPECTED_FILES - found_names
    unexpected = found_names - EXPECTED_FILES

    msgs = []
    if missing:
        msgs.append(
            f"Missing expected log files in {BACKUP_DIR}: {', '.join(sorted(missing))}"
        )
    if unexpected:
        msgs.append(
            f"Unexpected extra .log files present in {BACKUP_DIR}: "
            f"{', '.join(sorted(unexpected))}"
        )

    if msgs:
        # Combine into one AssertionError to show all discrepancies at once
        pytest.fail(" | ".join(msgs))


def test_log_line_format_and_failed_count(log_files):
    """
    Validate every line matches the required format and that the aggregate
    number of FAILED lines is exactly four.
    """
    total_failed = 0

    for filename in sorted(EXPECTED_FILES):
        path = log_files.get(filename)
        assert path is not None, f"Internal test error: {filename} unexpectedly missing."

        # Ensure file is a regular file
        assert path.is_file(), f"Expected {path} to be a regular file."

        for lineno, line in enumerate(read_lines(path), start=1):
            if not LOG_LINE_RE.match(line):
                pytest.fail(
                    f"Line {lineno} in {path} does not conform to the exact "
                    f"log format:\n{line!r}"
                )

            # Count failed lines
            if "STATUS=FAILED" in line:
                total_failed += 1

    assert (
        total_failed == 4
    ), f"Across all three log files there must be exactly 4 FAILED lines, got {total_failed}."