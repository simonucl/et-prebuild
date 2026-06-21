# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the OS / file-system
# before the student performs any action for:
# “Generate an error–frequency summary from an application log”.
#
# The checks performed here guarantee that the resources the student must
# read from (and the ones they must create) are in the expected state.
#
# Rules enforced:
#   • The logs directory and the source log file must already exist.
#   • The output file must *not* exist yet.
#   • The source log file must contain [ERROR] lines whose error-codes and
#     counts exactly match the ground-truth that the grader will later use.

import re
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "dev_project"
LOGS_DIR = PROJECT_DIR / "logs"
SERVER_LOG = LOGS_DIR / "server.log"
SUMMARY_LOG = LOGS_DIR / "error_summary.log"

# Ground-truth mapping that the student’s script is expected to reproduce.
EXPECTED_ERROR_COUNTS = {
    "E1001": 2,
    "E2345": 2,
    "E7777": 1,
}

ERROR_LINE_REGEX = re.compile(
    r"""
    ^\d{4}-\d{2}-\d{2}\s                   # date
    \d{2}:\d{2}:\d{2}\s                    # time
    \[ERROR\]\s
    \[([A-Z]\d{4})\]\s                     # capture error-code
    .*$                                    # rest of the line
    """,
    re.VERBOSE,
)


def test_logs_directory_exists():
    """The logs directory must already exist."""
    assert LOGS_DIR.is_dir(), (
        f"Required directory '{LOGS_DIR}' is missing. "
        "It must be present before the student starts."
    )


def test_server_log_exists():
    """The source server.log file must already exist."""
    assert SERVER_LOG.is_file(), (
        f"Required log file '{SERVER_LOG}' is missing. "
        "Provide this file so the student can read it."
    )


def test_error_summary_does_not_exist_yet():
    """The output file must not exist before the student runs their solution."""
    assert not SUMMARY_LOG.exists(), (
        f"Output file '{SUMMARY_LOG}' already exists, "
        "but it should be created by the student's work, not beforehand."
    )


def test_server_log_error_counts_match_ground_truth():
    """
    The [ERROR] lines in server.log must contain exactly the expected
    error-codes and counts so the grader can validate the student’s output.
    """
    found_counts = {}

    with SERVER_LOG.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if "[ERROR]" not in line:
                continue

            match = ERROR_LINE_REGEX.match(line)
            assert match, (
                f"Line {line_no} in '{SERVER_LOG}' is marked as [ERROR] "
                "but does not conform to the expected format:\n"
                f"    {line.rstrip()}"
            )

            code = match.group(1)
            found_counts[code] = found_counts.get(code, 0) + 1

    # Ensure we found at least one error line.
    assert found_counts, (
        f"No valid [ERROR] lines were found in '{SERVER_LOG}'. "
        "The student needs these lines to generate a summary."
    )

    # Compare against the ground truth.
    assert found_counts == EXPECTED_ERROR_COUNTS, (
        "The [ERROR] counts in 'server.log' do not match the ground-truth "
        "expected by the grader.\n"
        f"Expected: {EXPECTED_ERROR_COUNTS}\n"
        f"Found:    {found_counts}"
    )