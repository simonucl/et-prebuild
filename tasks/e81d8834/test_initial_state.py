# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating
# system / filesystem **before** the student creates the frequency
# report requested in the exercise description.
#
# The checks performed here purposely **do not** look for the presence
# of the output report that the student will generate later.  Instead
# they make sure the raw input log exists and is well-formed, and that
# the output location is still clean.

import os
import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constant paths used throughout the tests
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
LOG_DIR = HOME / "observability" / "logs"
LOG_FILE = LOG_DIR / "app_events.log"

REPORT_DIR = HOME / "observability" / "reports"
REPORT_FILE = REPORT_DIR / "event_code_frequency.log"

# Expected event codes and their counts (ground-truth for the initial state).
EXPECTED_COUNTS = {
    "EVT_DATA_SYNC": 20,
    "EVT_LOGIN": 14,
    "EVT_LOGOUT": 11,
    "EVT_ERROR": 9,
    "EVT_TIMEOUT": 6,
}

# Regular expression that each log line must match.
LINE_REGEX = re.compile(
    r"""
    ^                                   # start of line
    \d{4}-\d{2}-\d{2}T                  # YYYY-MM-DDT
    \d{2}:\d{2}:\d{2}Z                  # HH:MM:SSZ
    \s+                                 # one or more spaces
    (?P<code>EVT_[A-Z_]+)               # event code (captured)
    (\s+.*)?                            # the rest of the line (optional)
    $                                   # end of line
    """,
    re.VERBOSE,
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def read_log_lines():
    """Return a list with *all* lines in the raw log file (stripped of \n)."""
    with LOG_FILE.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_log_file_exists_and_is_regular():
    """The raw application event log must exist and be a regular file."""
    assert LOG_FILE.exists(), f"Expected log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_directory_is_correct():
    """The log directory path must exist and be a directory."""
    assert LOG_DIR.exists(), f"Log directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_report_file_does_not_exist_yet():
    """
    Before the student runs their solution, the report directory may or may
    not exist, but the *report file* itself must NOT be present.
    """
    assert not REPORT_FILE.exists(), (
        f"Output report {REPORT_FILE} already exists; the student should "
        f"create it as part of the exercise, so it must be absent beforehand."
    )


def test_log_file_has_exactly_60_lines():
    """The input log is expected to contain exactly 60 lines."""
    lines = read_log_lines()
    assert len(lines) == 60, (
        f"Log file {LOG_FILE} should contain exactly 60 lines, "
        f"found {len(lines)} lines instead."
    )


def test_each_line_matches_required_format():
    """Every line must conform to the timestamp + event-code format."""
    lines = read_log_lines()

    for idx, line in enumerate(lines, start=1):
        m = LINE_REGEX.match(line)
        assert m, (
            f"Line {idx} in {LOG_FILE} does not match the required format:\n"
            f"    {line}"
        )
        code = m.group("code")
        assert code in EXPECTED_COUNTS, (
            f"Line {idx} contains unknown event code '{code}'. "
            f"Allowed codes: {sorted(EXPECTED_COUNTS)}."
        )


def test_event_code_frequencies_are_as_expected():
    """
    Verify that the frequency of each event code in the initial log file
    matches the ground-truth counts provided by the task description.
    """
    counts = {code: 0 for code in EXPECTED_COUNTS}
    lines = read_log_lines()

    for line in lines:
        code = LINE_REGEX.match(line).group("code")
        counts[code] += 1

    # First, check that **only** the expected codes are present.
    extra_codes = set(counts) - set(EXPECTED_COUNTS)
    assert not extra_codes, (
        f"Unexpected event codes found in log: {sorted(extra_codes)}"
    )

    # Now, compare individual counts.
    mismatches = [
        (code, counts[code], EXPECTED_COUNTS[code])
        for code in EXPECTED_COUNTS
        if counts[code] != EXPECTED_COUNTS[code]
    ]

    assert not mismatches, (
        "Event-code frequency mismatch detected in the log file:\n"
        + "\n".join(
            f"  {code}: expected {exp}, found {got}"
            for code, got, exp in mismatches
        )
    )