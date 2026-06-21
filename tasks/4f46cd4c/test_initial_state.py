# test_initial_state.py
#
# This pytest suite validates that the operating-system state
# is correct *before* the student performs any work.
#
# What we assert:
# 1. The source log file /home/user/app/logs/pipeline.log exists and is readable.
# 2. The log file contains the expected number of ERROR and WARNING lines
#    and the expected timestamp for the last ERROR.
# 3. The destination summary file (/home/user/app/reports/log_summary.txt)
#    does NOT exist yet (the student must create it).
# 4. The directories needed for the task already exist.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PIPELINE_LOG = HOME / "app" / "logs" / "pipeline.log"
SUMMARY_FILE = HOME / "app" / "reports" / "log_summary.txt"


@pytest.fixture(scope="module")
def log_contents():
    """Return the contents of the pipeline log as a list of lines."""
    if not PIPELINE_LOG.exists():
        pytest.skip(f"{PIPELINE_LOG} is missing; cannot run further tests.")
    try:
        return PIPELINE_LOG.read_text(encoding="utf-8").splitlines()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Failed to read {PIPELINE_LOG}: {exc}")


def test_directories_exist():
    """Ensure /home/user/app/logs and /home/user/app/reports both exist."""
    logs_dir = PIPELINE_LOG.parent
    reports_dir = SUMMARY_FILE.parent

    assert logs_dir.is_dir(), (
        f"Required directory {logs_dir} is missing. "
        "The pipeline log should be located here."
    )
    assert reports_dir.is_dir(), (
        f"Required directory {reports_dir} is missing. "
        "Create it so the summary file can be written."
    )


def test_pipeline_log_exists_and_nonempty(log_contents):
    """The source log file must be present and non-empty."""
    assert PIPELINE_LOG.is_file(), f"Expected log file {PIPELINE_LOG} was not found."
    assert log_contents, f"{PIPELINE_LOG} is empty; it must contain log entries."


def test_pipeline_log_expected_metrics(log_contents):
    """
    Validate that the pipeline log contains the expected ERROR/WARNING counts
    and the correct timestamp for the last ERROR line, matching the fixture
    supplied in the assignment.
    """
    error_lines = [ln for ln in log_contents if "ERROR" in ln]
    warning_lines = [ln for ln in log_contents if "WARNING" in ln]

    expected_error_count = 1
    expected_warning_count = 2
    expected_last_error_ts = "2023-09-01 10:00:02"

    assert len(error_lines) == expected_error_count, (
        f"Expected {expected_error_count} line(s) containing 'ERROR' in "
        f"{PIPELINE_LOG}, but found {len(error_lines)}."
    )
    assert len(warning_lines) == expected_warning_count, (
        f"Expected {expected_warning_count} line(s) containing 'WARNING' in "
        f"{PIPELINE_LOG}, but found {len(warning_lines)}."
    )

    # Extract timestamp portion: assume format "[YYYY-MM-DD HH:MM:SS] ..."
    def extract_ts(line: str) -> str:
        if not line.startswith("[") or "]" not in line:
            return ""
        return line.split("]")[0].lstrip("[")

    last_error_ts = extract_ts(error_lines[-1]) if error_lines else ""
    assert last_error_ts == expected_last_error_ts, (
        "Timestamp for last 'ERROR' line does not match expected.\n"
        f"Expected : {expected_last_error_ts}\n"
        f"Found    : {last_error_ts}"
    )


def test_summary_file_not_present_yet():
    """
    The student has not created the summary file yet; it must be absent so that
    their forthcoming work creates it afresh.
    """
    assert not SUMMARY_FILE.exists(), (
        f"{SUMMARY_FILE} already exists. "
        "Delete or rename it before running the assignment so the tests "
        "can verify your newly generated file later."
    )