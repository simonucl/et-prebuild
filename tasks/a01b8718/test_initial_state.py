# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state **before**
# the student runs their solution script.  It checks that:
#   1. The expected log directory and the two log files are present.
#   2. Those log files contain the specific sample lines described in
#      the task description (so later tests can rely on them).
#   3. No deployment-report artefacts exist yet.
#
# IMPORTANT: If any of these tests fail the student must first bring the
# filesystem back to the required starting point before attempting the task.

import os
import re
import pytest
from pathlib import Path

HOME = Path("/home/user")
LOG_DIR = HOME / "app" / "logs"
DEPLOY_DIR = HOME / "deployment_reports"
SUMMARY_FILE = DEPLOY_DIR / "failure_summary_latest.txt"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _read_file(path: Path) -> list[str]:
    """Return the file content as a list of raw lines (with trailing newlines
    stripped).  Fail gracefully if the file is missing or unreadable."""
    if not path.exists():
        pytest.fail(f"Required log file is missing: {path}")
    try:
        with path.open(encoding="utf-8") as fh:
            return [ln.rstrip("\n") for ln in fh.readlines()]
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def _line_matches(raw_line: str, expected_parts: tuple[str, str, str, str]) -> bool:
    """
    Check that `raw_line` matches the (DATE|TIME, SERVICE, LEVEL, CODE) tuple.

    The log format can contain variable horizontal spacing, so the match is
    performed via a tolerant regular expression:
      ^YYYY-MM-DD HH:MM:SS,mmm  <spaces>-
          <spaces>SERVICE<spaces>-<spaces>LEVEL<spaces>-<spaces>CODE\b
    The message text is *not* validated here; we only need enough certainty
    that the specific row is present.
    """
    date_time, service, level, code = expected_parts

    # Build a tolerant regex for the given parts.
    pattern = (
        rf"^{re.escape(date_time)}"          # exact timestamp (with millis)
        rf"\s+-\s+"                         # first " - " separator (tolerate spaces)
        rf"{re.escape(service)}\s*-\s+"     # service then " - "
        rf"{re.escape(level)}\s*-\s+"       # level then " - "
        rf"{re.escape(code)}\b"             # error / info / warn code
    )
    return re.search(pattern, raw_line) is not None


# ---------------------------------------------------------------------------
# Ground-truth expectations for each file
# ---------------------------------------------------------------------------
EXPECTED_LOG_CONTENT = {
    "app-2023-08-10.log": [
        ("2023-08-10 08:53:02,018", "api-service",     "INFO", "I200"),
        ("2023-08-10 09:01:44,776", "api-service",     "WARN", "W301"),
        ("2023-08-10 09:42:11,667", "scheduler",       "INFO", "I210"),
    ],
    "app-2023-08-11.log": [
        ("2023-08-11 09:15:23,456", "api-service",     "INFO",  "I201"),
        ("2023-08-11 10:02:11,102", "billing-service", "ERROR", "E451"),
        ("2023-08-11 11:47:05,332", "api-service",     "ERROR", "E401"),
        ("2023-08-11 14:30:00,908", "scheduler",       "INFO",  "I215"),
    ],
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_log_directory_exists():
    assert LOG_DIR.is_dir(), (
        f"Log directory {LOG_DIR} is missing. "
        "The initial setup must contain /home/user/app/logs/ with the two "
        "pre-existing log files."
    )


@pytest.mark.parametrize("filename", list(EXPECTED_LOG_CONTENT))
def test_log_file_presence(filename):
    path = LOG_DIR / filename
    assert path.is_file(), (
        f"Required log file {path} is missing. "
        "Make sure the unmodified logs from yesterday are present before "
        "running the exercise."
    )


@pytest.mark.parametrize(
    ("filename", "expected_rows"),
    EXPECTED_LOG_CONTENT.items()
)
def test_log_file_contains_expected_rows(filename, expected_rows):
    """
    Confirm that each expected (timestamp, service, level, code) line is
    present in the corresponding log file.  This ensures later grading can
    rely on the specific ERROR lines being available for extraction.
    """
    path = LOG_DIR / filename
    raw_lines = _read_file(path)

    for parts in expected_rows:
        if not any(_line_matches(line, parts) for line in raw_lines):
            date_time, service, level, code = parts
            pytest.fail(
                f"The log file {path} is missing the expected entry:\n"
                f"  {date_time} … {service} … {level} … {code}\n"
                "Verify that the source log has not been altered."
            )


def test_no_deployment_report_yet():
    """
    Prior to running the student's solution, the deployment report directory
    *may* exist from a previous run, but the summary file must not.  We only
    guard against the presence of the summary artefact because its existence
    would indicate the task has already been performed.
    """
    assert not SUMMARY_FILE.exists(), (
        f"The summary file {SUMMARY_FILE} already exists.  "
        "Testing must start from a clean state where this file is absent."
    )