# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem **before** the student performs any action for the task
# “Generate one-line regression summary”.
#
# What we assert:
#   1. /home/user/reports/test_report.txt
#        • exists and is a regular, readable file
#        • can be decoded as UTF-8
#        • every non-blank line matches the required pattern
#        • overall there are exactly 10 executed test-case lines
#        • exactly 3 of those lines have status FAIL
#   2. /home/user/reports/test_summary.txt
#        • MUST NOT exist yet (it will be created by the student’s solution)
#
# If any of these assertions fails the test will emit a clear, actionable
# message so the student knows what needs to be fixed.

import os
import re
from pathlib import Path

REPORT_PATH = Path("/home/user/reports/test_report.txt")
SUMMARY_PATH = Path("/home/user/reports/test_summary.txt")

LINE_REGEX = re.compile(r"^TC-\d{4} : (PASS|FAIL) : \d+\s*$")


def test_report_file_exists_and_is_regular():
    """The regression report must exist and be a regular file."""
    assert REPORT_PATH.exists(), f"Expected report file {REPORT_PATH} to exist."
    assert REPORT_PATH.is_file(), f"{REPORT_PATH} exists but is not a regular file."


def test_report_is_valid_utf8():
    """Report must be decodable as UTF-8."""
    try:
        REPORT_PATH.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        pytest.fail(f"Report file {REPORT_PATH} is not valid UTF-8: {e}")


def test_report_line_format_and_counts():
    """Every non-blank line must match the required format; counts must be correct."""
    content = REPORT_PATH.read_text(encoding="utf-8").splitlines()

    non_blank_lines = [ln for ln in content if ln.strip()]
    total_tests = len(non_blank_lines)
    assert total_tests == 10, (
        f"Expected 10 executed test lines, found {total_tests}. "
        "Check that the report is complete and that blank lines are handled correctly."
    )

    for idx, line in enumerate(non_blank_lines, start=1):
        assert LINE_REGEX.match(line), (
            f"Line {idx!r} in {REPORT_PATH} does not conform to the required pattern:\n"
            f"    {line}\n"
            "Expected format: 'TC-1234 : PASS|FAIL : <duration_ms>'"
        )

    failed_tests = sum(1 for ln in non_blank_lines if " FAIL " in ln)
    assert failed_tests == 3, (
        f"Expected 3 failed tests, found {failed_tests}. "
        "Verify the status field in each line."
    )


def test_summary_file_absent_initially():
    """The summary file must NOT exist before the student runs their solution."""
    assert not SUMMARY_PATH.exists(), (
        f"Summary file {SUMMARY_PATH} already exists, "
        "but the task requires it to be created by the student's solution."
    )