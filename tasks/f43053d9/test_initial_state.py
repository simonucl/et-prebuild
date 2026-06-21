# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state for the
# “error-code summary” exercise *before* the student performs any action.
#
# Truth (what must already be on disk):
#   • /home/user/ci_pipeline/logs/build_2024-05-01.log      → must exist,
#     be readable and contain the 9 lines shown in the task description.
#
#   • /home/user/ci_pipeline/logs/                          → must exist.
#
#   • /home/user/ci_pipeline/reports/                       → must *not* exist
#     yet (the student is responsible for creating it).
#
#   • /home/user/ci_pipeline/reports/error_code_summary_2024-05-01.txt
#     → must *not* exist yet.
#
# Everything else is out of scope for this pre-flight check.
#
# Only the standard library and pytest are used.

import os
import re
from pathlib import Path

import pytest

LOG_DIR = Path("/home/user/ci_pipeline/logs")
LOG_FILE = LOG_DIR / "build_2024-05-01.log"
REPORTS_DIR = Path("/home/user/ci_pipeline/reports")
SUMMARY_FILE = REPORTS_DIR / "error_code_summary_2024-05-01.txt"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
ISO_ERROR_RE = re.compile(
    rb"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z] ERROR (E\d{3}): .+"
)


# --------------------------------------------------------------------------- #
# Tests for artefacts that *must* already be present
# --------------------------------------------------------------------------- #
def test_log_directory_exists():
    """The directory that houses the raw log must already exist."""
    assert LOG_DIR.is_dir(), (
        f"Expected directory {LOG_DIR} to exist, "
        "but it is missing."
    )


def test_log_file_exists_and_readable():
    """The raw log file must be present and readable."""
    assert LOG_FILE.is_file(), (
        f"Expected log file {LOG_FILE} to exist, "
        "but it is missing."
    )
    try:
        LOG_FILE.read_bytes()
    except Exception as exc:  # pragma: no cover  (guards against permission issues)
        pytest.fail(f"Log file {LOG_FILE} exists but cannot be read: {exc}")


def test_log_file_has_expected_content():
    """
    Validate that the log file has exactly 9 lines and that every line
    matches the strict pattern:

        [ISO-8601] ERROR E###: <free-text>
    """
    content = LOG_FILE.read_bytes().splitlines()
    expected_line_count = 9
    assert len(content) == expected_line_count, (
        f"{LOG_FILE} should contain {expected_line_count} lines, "
        f"found {len(content)}."
    )

    unmatched = [
        (idx + 1, line.decode(errors='replace'))
        for idx, line in enumerate(content)
        if not ISO_ERROR_RE.fullmatch(line)
    ]
    assert not unmatched, (
        f"The following lines in {LOG_FILE} do not match the required "
        f"pattern '[ISO-8601] ERROR E###: …':\n"
        + "\n".join(f"  line {lineno}: {text}" for lineno, text in unmatched)
    )

    # Optional strict check of expected error-code distribution.
    from collections import Counter

    codes = [
        ISO_ERROR_RE.fullmatch(line).group(1).decode()
        for line in content
    ]
    expected_counts = {"E202": 4, "E101": 3, "E303": 1, "E404": 1}
    assert Counter(codes) == expected_counts, (
        "The error-code distribution in the log file does not match the "
        "expected fixture.\n"
        f"Expected: {expected_counts}\n"
        f" Found:   {Counter(codes)}"
    )


# --------------------------------------------------------------------------- #
# Tests for artefacts that *must not* yet exist
# --------------------------------------------------------------------------- #
def test_reports_directory_absent():
    """
    The reports directory should *not* exist before the student runs their
    solution script – they are required to create it.
    """
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR} should NOT exist yet; "
        "it will be created by the student's solution."
    )


def test_summary_file_absent():
    """The summary file must not pre-exist."""
    assert not SUMMARY_FILE.exists(), (
        f"File {SUMMARY_FILE} should NOT exist yet; "
        "it will be produced by the student's solution."
    )