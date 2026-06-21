# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student carries out the task described in the prompt.
#
# It checks that:
#   • The input CSV file exists in its expected absolute location and
#     contains exactly the expected lines (header + 11 data rows).
#   • The reports directory exists and is currently empty.
#   • No output file critical_summary.log exists yet.
#
# Any deviation from these expectations will raise a clear, descriptive
# assertion error so that the student immediately knows what is missing
# or different.

import os
import stat
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "projects", "qa")
CSV_PATH = os.path.join(BASE_DIR, "test_scenarios", "scenarios.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SUMMARY_PATH = os.path.join(REPORTS_DIR, "critical_summary.log")


@pytest.fixture(scope="module")
def csv_lines():
    """Read all lines from the CSV file and return them stripped of their trailing newlines."""
    assert os.path.isfile(CSV_PATH), (
        f"Expected CSV file not found at {CSV_PATH}. "
        "Ensure the file exists before running the task."
    )

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n\r") for ln in f.readlines()]
    return lines


def test_csv_contents_exact(csv_lines):
    """The CSV file must contain exactly the lines specified in the task description."""
    expected_lines = [
        "id,title,severity,status,owner",
        '1,"Login with invalid password",low,closed,alice',
        '2,"Login with valid password",medium,closed,bob',
        '15,"Password reset email not sent",high,open,carol',
        '23,"Profile picture upload fails",medium,open,alice',
        '42,"Database deadlock during signup",critical,open,dave',
        '55,"Race condition on logout",critical,closed,emma',
        '71,"Session not terminated on password change",high,open,bob',
        '85,"Crash on importing malformed CSV",critical,reopened,carol',
        '104,"System reboot on malformed packet",critical,open,emma',
        '175,"Two-factor code not accepted",high,open,dave',
        '200,"Memory leak in report generator",critical,in-progress,frank',
    ]

    assert csv_lines == expected_lines, (
        "The content of scenarios.csv is not exactly as expected.\n"
        "Differences:\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n\n"
        f"Found ({len(csv_lines)} lines):\n{csv_lines}"
    )


def test_reports_directory_exists_and_empty():
    """The reports directory must exist and be empty before the task begins."""
    assert os.path.isdir(REPORTS_DIR), (
        f"Reports directory {REPORTS_DIR} does not exist. "
        "It should be present (and empty) before the task."
    )

    # List any non-hidden entries inside the reports directory
    entries = [
        name
        for name in os.listdir(REPORTS_DIR)
        if not name.startswith(".")
    ]

    assert entries == [], (
        f"Reports directory {REPORTS_DIR} is expected to be empty, "
        f"but contains: {entries}"
    )


def test_summary_log_does_not_exist_yet():
    """critical_summary.log should not exist before the student creates it."""
    assert not os.path.exists(SUMMARY_PATH), (
        f"Output file {SUMMARY_PATH} already exists, "
        "but it should be created by the student as part of the task."
    )


def test_csv_is_world_readable(csv_lines):
    """The CSV file should be world-readable so that all tooling can access it."""
    mode = os.stat(CSV_PATH).st_mode
    # Check the "other" read bit.
    assert mode & stat.S_IROTH, (
        f"CSV file {CSV_PATH} is not world-readable (mode={oct(mode)}). "
        "Run chmod 644 or more permissive."
    )