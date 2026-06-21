# test_initial_state.py
#
# This pytest suite verifies that the filesystem state required for the
# “status-summary” exercise is present *before* the student runs any command.
# It checks for:
#   1. Presence of essential directories.
#   2. Presence of the integration log file.
#   3. Correct contents of the log file (line counts & HTTP status
#      class distributions).
#
# IMPORTANT:  In compliance with the grading rules, this test suite
# does *not* look for the eventual output file
# /home/user/api_test/analysis/status_summary.txt.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
API_TEST_DIR = HOME / "api_test"
LOGS_DIR = API_TEST_DIR / "logs"
ANALYSIS_DIR = API_TEST_DIR / "analysis"
LOG_FILE = LOGS_DIR / "integration.log"

# Expected statistics extracted from the truth-value description.
EXPECTED_TOTAL = 8
EXPECTED_2XX = 5
EXPECTED_4XX = 2
EXPECTED_5XX = 1


@pytest.mark.parametrize(
    "path,description",
    [
        (API_TEST_DIR, "base project directory /home/user/api_test"),
        (LOGS_DIR, "logs directory /home/user/api_test/logs"),
        (ANALYSIS_DIR, "analysis directory /home/user/api_test/analysis"),
    ],
)
def test_required_directories_exist(path: Path, description: str) -> None:
    """
    Ensure that all mandatory directories exist.
    """
    assert path.is_dir(), f"Missing required directory: {description}"


def test_analysis_directory_is_writable() -> None:
    """
    Confirm that the analysis directory is writable so the student’s command
    can create status_summary.txt there.
    """
    # Using os.access instead of attempting to write a file so we remain non-destructive.
    assert os.access(ANALYSIS_DIR, os.W_OK), (
        "Directory /home/user/api_test/analysis exists but is not writable."
    )


def test_integration_log_exists() -> None:
    """
    Verify that the integration log file is present.
    """
    assert LOG_FILE.is_file(), (
        "Expected log file /home/user/api_test/logs/integration.log is missing."
    )


def test_integration_log_contents() -> None:
    """
    Parse the log file and validate that its statistics match the expected
    truth values. This ensures the student has the correct starting data.
    """
    with LOG_FILE.open(encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    total = len(lines)
    count_2xx = 0
    count_4xx = 0
    count_5xx = 0

    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            pytest.fail(f"Line {idx} in integration.log is blank; log should not contain empty lines.")

        # Assume the HTTP status code is the last whitespace-separated token.
        status_token = line.split()[-1]
        if not status_token.isdigit():
            pytest.fail(
                f"Line {idx} in integration.log does not end with a numeric status code: {line!r}"
            )

        status_code = int(status_token)
        if 200 <= status_code <= 299:
            count_2xx += 1
        elif 400 <= status_code <= 499:
            count_4xx += 1
        elif 500 <= status_code <= 599:
            count_5xx += 1
        # Other ranges (e.g., 100 or 300) are ignored for this exercise.

    assert total == EXPECTED_TOTAL, (
        f"integration.log should contain {EXPECTED_TOTAL} lines, found {total}."
    )
    assert count_2xx == EXPECTED_2XX, (
        f"Expected {EXPECTED_2XX} successful (2xx) responses, found {count_2xx}."
    )
    assert count_4xx == EXPECTED_4XX, (
        f"Expected {EXPECTED_4XX} client error (4xx) responses, found {count_4xx}."
    )
    assert count_5xx == EXPECTED_5XX, (
        f"Expected {EXPECTED_5XX} server error (5xx) responses, found {count_5xx}."
    )