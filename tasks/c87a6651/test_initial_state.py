# test_initial_state.py
#
# This test-suite validates that the **initial** filesystem state
# required by the assignment is present _before_ the student’s
# solution is executed.  It deliberately avoids checking for any
# artefacts that the student is expected to create (e.g. the
# `critical.log` file).
#
# Rules adhered to:
#   • Only stdlib + pytest are used.
#   • Full, absolute paths are asserted.
#   • Failure messages are explicit about what is missing / wrong.

import os
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Constants – adjust here if the base location ever changes
# ---------------------------------------------------------------------------
BASE_DIR = Path("/home/user/api_test/logs")
SOURCE_LOG = BASE_DIR / "api_integration.log"


# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------
def _read_lines(file_path: Path):
    """Return all lines from *file_path* decoded as UTF-8."""
    try:
        with file_path.open("r", encoding="utf-8") as fp:
            return fp.readlines()
    except Exception as exc:  # pragma: no cover
        # Using pytest.fail gives a cleaner assert-style failure.
        pytest.fail(f"Log file '{file_path}' exists but could not be read: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_log_directory_exists():
    """The directory that holds the log files must exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory '{BASE_DIR}' does not exist. "
        "Make sure the log directory is in place before running the exercise."
    )


def test_source_log_exists_and_is_readable():
    """The consolidated execution log must exist and be readable."""
    assert SOURCE_LOG.is_file(), (
        f"Expected source log file '{SOURCE_LOG}' to exist, "
        "but it is missing."
    )

    # If we can read at least one line without raising, the file is readable.
    lines = _read_lines(SOURCE_LOG)
    assert lines, (
        f"The source log '{SOURCE_LOG}' is empty; "
        "it should contain the service execution history."
    )


def test_source_log_contains_expected_error_and_fatal_counts():
    """
    The initial source log is expected to contain exactly:
      • 3 lines with the keyword 'ERROR'
      • 1 line with the keyword 'FATAL'
    These counts are required so that the student can later extract four
    critical lines (3 ERROR + 1 FATAL) into *critical.log*.
    """
    lines = _read_lines(SOURCE_LOG)

    error_lines = [ln for ln in lines if "ERROR" in ln]
    fatal_lines = [ln for ln in lines if "FATAL" in ln]

    expected_error_count = 3
    expected_fatal_count = 1

    assert len(error_lines) == expected_error_count, (
        f"Expected {expected_error_count} lines containing 'ERROR' in "
        f"'{SOURCE_LOG}', but found {len(error_lines)}."
    )
    assert len(fatal_lines) == expected_fatal_count, (
        f"Expected {expected_fatal_count} line containing 'FATAL' in "
        f"'{SOURCE_LOG}', but found {len(fatal_lines)}."
    )


def test_chronological_order_is_preserved():
    """
    Verify that the ERROR and FATAL lines occur in the chronological order
    expected by the downstream tests (i.e., they appear in the same order
    they were logged).
    """
    lines = _read_lines(SOURCE_LOG)
    critical_indices = [
        idx
        for idx, line in enumerate(lines)
        if ("ERROR" in line) or ("FATAL" in line)
    ]

    # The indices list should already be sorted because the source log
    # is assumed to be chronological.  If not, that indicates the log
    # was modified or corrupted.
    assert critical_indices == sorted(critical_indices), (
        "The critical log entries (ERROR/FATAL) in "
        f"'{SOURCE_LOG}' are not in chronological order. "
        "Please restore the original log ordering."
    )