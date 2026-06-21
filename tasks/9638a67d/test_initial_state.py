# test_initial_state.py
#
# This pytest suite validates that the sample log file required for the
# “log-analysis exercise” is present *before* the learner starts work and that
# its contents match the values the grader will later expect.
#
# IMPORTANT:  These tests intentionally do **not** look for the student’s
#             output file (test_summary.txt); they only verify the existing
#             environment.

import os
import re
import pytest

LOG_DIR = "/home/user/app/logs"
LOG_PATH = os.path.join(LOG_DIR, "app.log")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_log_lines():
    """Return the log file’s lines stripped of their trailing newlines."""
    with open(LOG_PATH, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_log_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory missing: {LOG_DIR} "
        "(the application log directory must already exist)."
    )


def test_log_file_exists_and_is_file():
    assert os.path.isfile(LOG_PATH), (
        f"Required log file missing: {LOG_PATH} "
        "(it should be provided to the learner)."
    )


@pytest.fixture(scope="module")
def log_lines():
    """Provide the list of log lines to the other tests."""
    return _read_log_lines()


def test_expected_line_counts(log_lines):
    """Verify the counts of INFO, WARN and ERROR lines in the sample log."""
    error_count = sum("[ERROR]" in ln for ln in log_lines)
    warn_count = sum("[WARN]" in ln for ln in log_lines)
    info_count = sum("[INFO]" in ln for ln in log_lines)

    assert error_count == 4, (
        f"The log should contain exactly 4 '[ERROR]' lines, "
        f"but {error_count} were found."
    )
    assert warn_count == 3, (
        f"The log should contain exactly 3 '[WARN]' lines, "
        f"but {warn_count} were found."
    )
    assert info_count == 9, (
        f"The log should contain exactly 9 '[INFO]' lines, "
        f"but {info_count} were found."
    )


def test_last_three_error_lines_match_spec(log_lines):
    """
    The grader will expect these to become the last-three-errors section of
    the summary file.  Ensure the source data is exactly as documented.
    """
    expected_last_errors = [
        "2023-09-16 09:00:02 [ERROR] Disk write failed",
        "2023-09-15 10:16:05 [ERROR] Unexpected null pointer",
        "2023-09-15 10:15:26 [ERROR] Failed to connect to database",
    ]

    # Extract ERROR lines preserving original order (already chronological).
    error_lines = [ln for ln in log_lines if "[ERROR]" in ln]

    # Latest errors in reverse-chronological order (newest first).
    last_three = list(reversed(error_lines))[:3]

    assert last_three == expected_last_errors, (
        "The last three error lines in app.log do not match the specification:\n"
        f"Expected:\n  {expected_last_errors}\n"
        f"Found:\n  {last_three}"
    )


def test_log_lines_are_not_padded(log_lines):
    """
    Quick sanity-check: no log line should start or end with whitespace,
    which could trip simple parsing during the exercise.
    """
    offenders = [ln for ln in log_lines if ln != ln.strip()]
    assert not offenders, (
        "Some log lines contain unexpected leading/trailing whitespace:\n"
        + "\n".join(offenders[:5])  # Show up to first 5 offenders.
    )


def test_dates_are_iso_like(log_lines):
    """
    Ensure every log line begins with a YYYY-MM-DD date so that the learner
    can rely on chronological ordering.
    """
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2} ")
    bad_lines = [ln for ln in log_lines if not date_re.match(ln)]
    assert not bad_lines, (
        "Some lines do not start with the expected 'YYYY-MM-DD' date format:\n"
        + "\n".join(bad_lines[:5])
    )