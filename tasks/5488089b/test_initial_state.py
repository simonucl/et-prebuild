# test_initial_state.py
#
# This pytest suite validates that the staging environment already contains the
# expected input files for the student’s task _before_ any action is taken.
#
# What we check (and ONLY what we check):
#   • /home/user/ci/ exists and is a directory.
#   • /home/user/ci/logs/ exists and is a directory.
#   • Exactly two *.log files are present in that directory:
#         – service-auth.log
#         – service-payment.log
#   • Each of those log files contains the correct number of lines that include
#     the literal substring "ERROR" (2 in each file).
#
# We deliberately DO NOT look for, or even mention, any output files or the
# /home/user/ci/summary/ directory, because those are produced by the
# student’s solution and must not be part of the initial-state checks.
#
# If a test fails, the assertion message will clearly indicate what is wrong.

from pathlib import Path
import pytest

CI_DIR = Path("/home/user/ci")
LOG_DIR = CI_DIR / "logs"

EXPECTED_LOG_FILES = {
    "service-auth.log": 2,     # each has 2 lines containing the literal 'ERROR'
    "service-payment.log": 2,
}


def test_ci_directory_exists():
    assert CI_DIR.is_dir(), f"Expected base directory {CI_DIR} to exist and be a directory."


def test_logs_directory_exists():
    assert LOG_DIR.is_dir(), f"Expected logs directory {LOG_DIR} to exist and be a directory."


def test_exact_log_files_present():
    """Ensure that exactly the expected *.log files are present—no more, no less."""
    found_logs = {p.name for p in LOG_DIR.glob("*.log")}
    expected_logs = set(EXPECTED_LOG_FILES.keys())

    missing = expected_logs - found_logs
    extra = found_logs - expected_logs

    assert not missing, (
        "The following expected log files are missing from "
        f"{LOG_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Found unexpected *.log files in "
        f"{LOG_DIR}: {', '.join(sorted(extra))}"
    )
    assert found_logs == expected_logs  # defensive; should be true if previous asserts passed


@pytest.mark.parametrize("log_name,expected_error_count", EXPECTED_LOG_FILES.items())
def test_error_line_counts(log_name, expected_error_count):
    """Each log file must contain the correct number of lines with the substring 'ERROR'."""
    log_path = LOG_DIR / log_name
    assert log_path.is_file(), f"Expected log file {log_path} to exist."

    with log_path.open("r", encoding="utf-8") as fh:
        error_lines = [line for line in fh if "ERROR" in line]

    actual_count = len(error_lines)
    assert (
        actual_count == expected_error_count
    ), (
        f"File {log_path} should contain {expected_error_count} lines with 'ERROR', "
        f"but found {actual_count}."
    )