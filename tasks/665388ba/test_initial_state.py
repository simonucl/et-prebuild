# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the filesystem
before the student’s solution is executed.

Checks performed:

1. The sample log file /home/user/sample_app/logs/app.log exists and is a file.
2. The log file contains the *exact* expected number of “ERROR” and “CRITICAL”
   occurrences (case-sensitive).
3. The derived status from those counts matches the specification:
      status = "ALERT" if (error_count + critical_count) > 10 else "OK"

Nothing related to the output artefacts (/home/user/alerts/…) is tested here
because those do **not** exist yet and must be created by the learner.
"""

import os
from pathlib import Path

import pytest

# ---- Constants describing the ground-truth ----------------------------------

LOG_PATH = Path("/home/user/sample_app/logs/app.log")

EXPECTED_ERROR_COUNT = 6
EXPECTED_CRITICAL_COUNT = 5
EXPECTED_STATUS = "ALERT"  # Because 6 + 5 = 11 > 10


# ---- Utility ----------------------------------------------------------------


def _read_log_lines(path: Path):
    """Return a list of all lines (stripped of trailing newlines) in *path*."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return [line.rstrip("\n") for line in fh]
    except FileNotFoundError as exc:
        # Let the caller decide what to do; we only centralise the I/O here.
        raise exc


# ---- Tests ------------------------------------------------------------------


def test_log_file_exists():
    """The sample application log must exist *before* the task is attempted."""
    assert LOG_PATH.exists(), (
        f"Expected log file {LOG_PATH} does not exist. It must be present "
        "before the alert-generation script is run."
    )
    assert LOG_PATH.is_file(), (
        f"Expected {LOG_PATH} to be a regular file, but it is not."
    )


def test_error_and_critical_counts_match_ground_truth():
    """
    Verify that the counts of “ERROR” and “CRITICAL” in the sample log
    match the values specified in the task description.
    """
    lines = _read_log_lines(LOG_PATH)

    error_count = sum(1 for line in lines if "ERROR" in line)
    critical_count = sum(1 for line in lines if "CRITICAL" in line)

    assert error_count == EXPECTED_ERROR_COUNT, (
        f"Mismatch in ERROR count: expected {EXPECTED_ERROR_COUNT}, "
        f"found {error_count}."
    )
    assert critical_count == EXPECTED_CRITICAL_COUNT, (
        f"Mismatch in CRITICAL count: expected {EXPECTED_CRITICAL_COUNT}, "
        f"found {critical_count}."
    )

    derived_status = "ALERT" if (error_count + critical_count) > 10 else "OK"
    assert derived_status == EXPECTED_STATUS, (
        f"Derived status {derived_status!r} does not match expected "
        f"{EXPECTED_STATUS!r}. (ERROR={error_count}, CRITICAL={critical_count})"
    )