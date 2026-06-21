# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student’s solution is run.  It makes sure that the
# prerequisite log file is present and contains exactly the data that
# the assignment statement is built upon.
#
# IMPORTANT:  Per the rubric we purposely do *not* look for the
#             reports/ directory nor for any of the files the student
#             is supposed to create later on.

import os
from pathlib import Path
import datetime as _dt
import pytest

LOG_PATH = Path("/home/user/project/app.log")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _parse_line(line: str):
    """
    Split a single log line into its four mandatory fields.

    Expected format (single ASCII space between first three fields):
        ISO-8601-UTC-timestamp  LOGLEVEL  ModuleName  Free-form-message
    """
    # Remove the trailing newline but keep internal spacing intact.
    stripped = line.rstrip("\n")

    # Split at most three times so the free-form message (which may
    # itself contain spaces) stays intact.
    parts = stripped.split(" ", 3)
    assert len(parts) == 4, (
        f"Malformed log line (expected 4 space-separated fields, got {len(parts)}):\n{line!r}"
    )
    ts_txt, level, module, message = parts

    # Basic validation of the timestamp (ISO-8601 Zulu).
    try:
        # The standard library cannot parse the trailing 'Z' directly
        # prior to 3.11, so we handle that ourselves.
        if ts_txt.endswith("Z"):
            ts = _dt.datetime.fromisoformat(ts_txt.replace("Z", "+00:00"))
        else:
            ts = _dt.datetime.fromisoformat(ts_txt)
    except ValueError as exc:
        pytest.fail(f"Timestamp {ts_txt!r} is not valid ISO-8601: {exc}")

    return ts, level, module, message, stripped


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def test_log_file_exists_and_is_regular():
    """The source log file must exist and be a regular file."""
    assert LOG_PATH.exists(), f"Required log file {LOG_PATH} is missing."
    assert LOG_PATH.is_file(), f"{LOG_PATH} exists but is not a regular file."
    # Basic permissions: readable by the current user
    assert os.access(LOG_PATH, os.R_OK), f"{LOG_PATH} is not readable."


def test_log_file_has_expected_number_of_lines():
    """The log file must contain exactly 11 lines (as per task description)."""
    with LOG_PATH.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    assert len(lines) == 11, (
        f"{LOG_PATH} is expected to contain 11 lines but has {len(lines)}."
    )

    # Ensure the very last line ends with an LF (use binary mode to be sure).
    with LOG_PATH.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert last_byte == b"\n", (
        f"The final line in {LOG_PATH} must terminate with an LF character."
    )


def test_every_line_conforms_to_expected_format():
    """Each line must parse into the four mandatory fields without error."""
    with LOG_PATH.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            try:
                _parse_line(line)
            except AssertionError as exc:
                pytest.fail(f"Line {lineno} failed validation: {exc}")


def test_error_counts_per_module_match_reference():
    """
    The ERROR counts per module in the initial log are fixed and known.
    This guards against accidental tampering with app.log.
    """
    expected_counts = {
        "AuthService": 3,
        "PaymentService": 3,
        "NotificationService": 1,
    }

    counts = {}
    with LOG_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            _, level, module, *_ = _parse_line(line)
            if level == "ERROR":
                counts[module] = counts.get(module, 0) + 1

    assert counts == expected_counts, (
        "ERROR counts per module do not match the reference data.\n"
        f"Expected: {expected_counts}\n"
        f"Found   : {counts}"
    )


def test_top_three_most_recent_error_lines_are_known():
    """
    The three most recent ERROR lines are predetermined.  Verifying them
    here ensures that later grading (which depends on them) is reliable.
    """
    expected_top3 = [
        "2023-09-30T10:21:33Z ERROR AuthService Invalid credentials for user id=44",
        "2023-09-30T10:22:47Z ERROR AuthService Invalid credentials for user id=45",
        "2023-09-30T10:25:04Z ERROR PaymentService Failed to authorize payment txn=991",
    ]

    # Collect ERROR lines together with their timestamps
    error_records = []
    with LOG_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            ts, level, *_ = _parse_line(line)
            if level == "ERROR":
                error_records.append((ts, line.rstrip("\n")))

    # Sort descending by timestamp to find the most recent ones
    error_records.sort(key=lambda rec: rec[0], reverse=True)
    most_recent_three = [rec[1] for rec in error_records[:3]]

    # Reverse back to chronological order (oldest first, newest last)
    most_recent_three.reverse()

    assert most_recent_three == expected_top3, (
        "The three most recent ERROR log lines are not as expected.\n"
        f"Expected:\n  " + "\n  ".join(expected_top3) +
        "\nFound:\n  " + "\n  ".join(most_recent_three)
    )