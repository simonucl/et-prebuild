# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system state
# required for the “Shell-scripting automation for a log analyst” task
# is present and correct *before* the student begins writing their
# solution.  It checks only the log-data prerequisites and **does not**
# look for any output artefacts that the student will later create.

import os
import re
from pathlib import Path

import pytest

# Constant paths used throughout the task
LOG_DIR = Path("/home/user/data/logs")

# Expected log files and their contents (totals across *all* .log files)
EXPECTED_FILES = {
    "app1.log",
    "app2.log",
    "app3.log",
}

EXPECTED_COUNTS = {
    "200": 6,
    "404": 3,
    "500": 2,
}

COUNTABLE_CODES = set(EXPECTED_COUNTS.keys())


def read_log_lines(path: Path):
    """Yield stripped lines from a log file."""
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n")


def extract_code(line: str) -> str | None:
    """
    Return the last whitespace-separated token of `line`
    *iff* that token is one of the recognised HTTP status codes;
    otherwise return None.
    """
    if not line:
        return None
    candidate = line.split()[-1]
    return candidate if candidate in COUNTABLE_CODES else None


@pytest.fixture(scope="module")
def log_files():
    """Return Path objects for all *.log files in LOG_DIR."""
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "The test harness should have populated it with log files."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

    # Gather *.log files
    files = sorted(LOG_DIR.glob("*.log"))
    filenames = {f.name for f in files}

    # Confirm that *all* expected log files are present
    missing = EXPECTED_FILES - filenames
    assert not missing, (
        f"The following expected log files are missing from {LOG_DIR}: "
        f"{', '.join(sorted(missing))}"
    )

    # Warn if any extra *.log files appear (not an error, but informative)
    unexpected = filenames - EXPECTED_FILES
    if unexpected:
        pytest.warns(UserWarning, lambda: None)
        print(
            f"NOTE: Unexpected *.log files present in {LOG_DIR}: "
            f"{', '.join(sorted(unexpected))}"
        )

    return files


def test_log_file_permissions_and_non_empty(log_files):
    """
    Each expected log file should be readable by the current user and non-empty.
    """
    for path in log_files:
        assert os.access(path, os.R_OK), f"Log file {path} is not readable."
        size = path.stat().st_size
        assert size > 0, f"Log file {path} is unexpectedly empty (0 bytes)."


def test_status_code_frequencies(log_files):
    """
    Aggregate every *.log file in /home/user/data/logs/ and ensure that the
    total number of lines whose *last* whitespace-separated field is exactly
    200, 404 or 500 matches the canonical truth values.
    """
    aggregated_counts = {code: 0 for code in COUNTABLE_CODES}

    # Parse each file
    for path in log_files:
        for line in read_log_lines(path):
            code = extract_code(line)
            if code:
                aggregated_counts[code] += 1

    # Produce helpful assertion messages per status code
    for code, expected in EXPECTED_COUNTS.items():
        actual = aggregated_counts.get(code, 0)
        assert (
            actual == expected
        ), f"HTTP status {code}: expected {expected} occurrences but found {actual}."

    # Sanity check: no unexpected status codes were counted
    extra_codes = {
        code for code, count in aggregated_counts.items() if code not in EXPECTED_COUNTS and count
    }
    assert (
        not extra_codes
    ), f"Encountered unexpected status codes in logs: {', '.join(sorted(extra_codes))}"


def test_no_carriage_returns(log_files):
    """
    Ensure log files do not contain Windows-style CRLF line endings, which could
    interfere with simple `grep`/`awk` scripts students might write.
    """
    cr_pattern = re.compile(r"\r$")
    offenders = []

    for path in log_files:
        for lineno, line in enumerate(read_log_lines(path), start=1):
            if cr_pattern.search(line):
                offenders.append(f"{path}:{lineno}")

    assert not offenders, (
        "The following lines contain carriage-return characters (\\r), "
        "which should not be present in POSIX text files:\n" + "\n".join(offenders)
    )