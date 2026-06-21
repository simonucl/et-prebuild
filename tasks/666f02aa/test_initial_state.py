# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state that must exist **before** the student performs any work.
#
# Requirements verified:
#   • The log source tree exists and is readable.
#   • /home/user/projects/inventory/logs/app.log exists, is non-empty, and
#     appears to follow the documented log format.
#   • The reports directory is present and currently empty of the expected
#     output file.
#   • The log file definitely contains at least one record that the assignment
#     is supposed to extract (i.e. a 5xx for /api/v1/orders on 2023-10-22).
#
# Only the Python standard library and pytest are used.

import re
from pathlib import Path

import pytest

LOGS_DIR = Path("/home/user/projects/inventory/logs")
APP_LOG = LOGS_DIR / "app.log"
REPORTS_DIR = Path("/home/user/reports")
EXPECTED_OUTPUT = REPORTS_DIR / "orders_5xx_20231022.log"

LINE_PATTERN = re.compile(
    # ISO-8601 date, space(s), IPv4, space(s), METHOD, space(s),
    # URL path, space(s), 3-digit status, space(s), latency like "120ms"
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\s+"
    r"(?:\d{1,3}\.){3}\d{1,3}\s+"
    r"[A-Z]+\s+"
    r"/\S+\s+"
    r"\d{3}\s+"
    r"\d+ms\n?$"
)


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} does not exist. "
        "The project tree is missing."
    )


def test_app_log_exists_and_readable():
    assert APP_LOG.is_file(), f"Required log file {APP_LOG} does not exist."
    assert APP_LOG.stat().st_size > 0, f"Log file {APP_LOG} is empty."
    # Attempt to open for reading to verify permissions.
    try:
        with APP_LOG.open("r", encoding="utf-8") as fh:
            fh.readline()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to open {APP_LOG} for reading: {exc}")


def test_reports_directory_exists():
    assert REPORTS_DIR.is_dir(), (
        f"Reports directory {REPORTS_DIR} is missing. "
        "It must exist before the task begins."
    )


def test_expected_output_file_not_present_yet():
    assert not EXPECTED_OUTPUT.exists(), (
        f"{EXPECTED_OUTPUT} already exists but should not be present "
        "before the student has run their solution."
    )


def test_some_lines_match_documented_format():
    """
    Scan a small sample of the file to ensure the documented log format
    is actually in use.  We don't read the whole file to keep the test
    lightweight.
    """
    sample_size = 50  # read first 50 lines (or entire file if shorter)
    bad_lines = []

    with APP_LOG.open("r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, 1):
            if idx > sample_size:
                break
            if not LINE_PATTERN.match(line):
                bad_lines.append((idx, line.rstrip("\n")))

    assert not bad_lines, (
        "One or more lines in the initial sample do not match the expected "
        "log format. Offending lines:\n" +
        "\n".join(f"  Line {ln}: {text}" for ln, text in bad_lines)
    )


def test_file_contains_at_least_one_relevant_5xx_order():
    """
    Confirm that the input data set actually contains *something* the
    student is supposed to extract, so the assignment is meaningful.
    """
    relevant_count = 0
    date_prefix = "2023-10-22"
    target_path = "/api/v1/orders"

    with APP_LOG.open("r", encoding="utf-8") as fh:
        for line in fh:
            # Quick substring checks before doing heavier work
            if date_prefix not in line or target_path not in line:
                continue

            parts = line.strip().split()
            if len(parts) < 6:
                continue  # malformed, skip

            date_part, _, _, path_part, status_part = (
                parts[0],
                parts[1],
                parts[2],
                parts[3],
                parts[4],
            )

            if not date_part.startswith(date_prefix):
                continue
            if path_part != target_path:
                continue

            try:
                status_code = int(status_part)
            except ValueError:
                continue

            if 500 <= status_code <= 599:
                relevant_count += 1
                break  # One is enough for the pre-state test

    assert relevant_count > 0, (
        "The source log file does not contain any 5xx records for "
        f"{target_path} on {date_prefix}. Either the test data is wrong or "
        "the file path is incorrect."
    )