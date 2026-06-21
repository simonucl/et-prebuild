# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / file-system
# state before the student starts working on the task.  These tests make
# sure the input artefacts are present and correct.  They deliberately
# DO NOT look for any of the output artefacts that the student is asked
# to create later on.

import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

LOG_FILE = Path("/home/user/project/logs/access.log")

# Expected frequency tables derived from the log file -----------------------
EXPECTED_STATUS_COUNTS = {
    "200": 13,
    "404": 6,
    "301": 4,
    "500": 2,
}

EXPECTED_ENDPOINT_COUNTS = {
    "/index.html":     11,
    "/products.html":   4,
    "/contact.html":    3,
    "/favicon.ico":     3,
    "/about.html":      2,
    "/blog.html":       2,
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

LOG_PATTERN = re.compile(
    r'''
    "                       # opening double quote
    (?P<method>[A-Z]+)\     # HTTP method followed by a space
    (?P<endpoint>/[^ ]+)\   # request target (endpoint) followed by a space
    HTTP/[^"]*"             # protocol part until the closing quote
    \s+
    (?P<status>\d{3})       # HTTP status code
    \s+
    (?P<size>\d+|-)         # response size or dash
    ''',
    re.VERBOSE,
)


def _read_log_lines():
    """Yield stripped log lines one by one."""
    with LOG_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n")


def _parse_line(line):
    """
    Try to parse a single Apache combined-log line.

    Returns a tuple (endpoint, status) on success.
    Raises AssertionError with a helpful message on failure.
    """
    m = LOG_PATTERN.search(line)
    assert m, f"Log line does not match expected format:\n{line}"
    return m.group("endpoint"), m.group("status")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_log_file_exists_and_is_readable():
    """The access.log file must exist and be a regular file."""
    assert LOG_FILE.exists(), f"Missing log file at expected path: {LOG_FILE}"
    assert LOG_FILE.is_file(), f"Expected a regular file, found something else: {LOG_FILE}"


def test_status_code_frequencies():
    """
    The status-code distribution in the initial log file must match the
    ground-truth so downstream tasks are graded correctly.
    """
    counts = {}
    for line in _read_log_lines():
        _, status = _parse_line(line)
        counts[status] = counts.get(status, 0) + 1

    # Helpful diff for failures
    assert counts == EXPECTED_STATUS_COUNTS, (
        "Status-code frequency table does not match the expected initial state.\n"
        f"Expected: {EXPECTED_STATUS_COUNTS}\n"
        f"Observed: {counts}"
    )


def test_endpoint_frequencies():
    """
    The endpoint distribution in the initial log file must match the
    ground-truth so that further computations (by the student) work out.
    """
    counts = {}
    for line in _read_log_lines():
        endpoint, _ = _parse_line(line)
        counts[endpoint] = counts.get(endpoint, 0) + 1

    assert counts == EXPECTED_ENDPOINT_COUNTS, (
        "Endpoint frequency table does not match the expected initial state.\n"
        f"Expected: {EXPECTED_ENDPOINT_COUNTS}\n"
        f"Observed: {counts}"
    )