# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the correct *initial* state _before_ the student begins work.
#
# What we check:
#   • The three raw authentication log files exist exactly where the
#     task description says they are.
#   • Each file is non-empty and each line follows the declared
#     key-value layout:
#         YYYY-MM-DDThh:mm:ssZ user=<username> action=<action> status=<status> ip=<ipv4>
#   • At least one line with “status=failed” exists across the files
#     (otherwise later subtasks would be impossible).
#   • Timestamps inside each individual file are in non-decreasing
#     chronological order.
#   • The output directory (/home/user/audit) must NOT exist yet,
#     guaranteeing a clean workspace for the student.
#
# Stdlib only + pytest.

import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME_DIR = Path("/home/user")
LOG_DIR = HOME_DIR / "data" / "logs"
RAW_LOG_FILES = [
    LOG_DIR / "auth_2023-05-01.log",
    LOG_DIR / "auth_2023-05-02.log",
    LOG_DIR / "auth_2023-05-03.log",
]
OUTPUT_DIR = HOME_DIR / "audit"

# Regular expression for one correctly-formatted line.
LINE_RE = re.compile(
    r"""
    ^                                   # start of line
    (?P<ts>\d{4}-\d{2}-\d{2}T           #   date part
          \d{2}:\d{2}:\d{2}Z)           #   time part + 'Z'
    [ ]user=(?P<user>[^\s]+)
    [ ]action=(?P<action>[^\s]+)
    [ ]status=(?P<status>[^\s]+)
    [ ]ip=(?P<ip>(?:\d{1,3}\.){3}\d{1,3})
    $                                   # end of line (no trailing spaces)
    """,
    re.VERBOSE,
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _parse_ts(ts_str: str) -> datetime:
    """Return a timezone-aware datetime object (UTC)."""
    # All timestamps are UTC and end with 'Z'
    return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_output_directory_does_not_exist_yet():
    """
    The /home/user/audit directory must *not* exist before the student starts.
    """
    assert not OUTPUT_DIR.exists(), (
        "Output directory %s already exists; the working directory should be "
        "created by the student during task execution." % OUTPUT_DIR
    )


@pytest.mark.parametrize("file_path", RAW_LOG_FILES)
def test_raw_log_file_exists(file_path: Path):
    """
    Verify that every expected raw log file is present and is a regular file.
    """
    assert file_path.is_file(), f"Required raw log file missing: {file_path}"


@pytest.mark.parametrize("file_path", RAW_LOG_FILES)
def test_raw_log_file_non_empty(file_path: Path):
    """
    Each raw log file must contain at least one line.
    """
    content = file_path.read_text(encoding="utf-8").splitlines()
    assert content, f"Raw log file {file_path} is empty."


@pytest.mark.parametrize("file_path", RAW_LOG_FILES)
def test_raw_log_file_line_format_and_order(file_path: Path):
    """
    1. Every line in the file must strictly match the specified key-value format.
    2. Timestamps inside the file must be in non-decreasing chronological order.
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    prev_ts: datetime | None = None

    for line_no, line in enumerate(lines, 1):
        m = LINE_RE.match(line)
        assert m, (
            f"Line {line_no} in {file_path} does not match the required format:\n"
            f"    {line}"
        )

        # Check chronological order inside this file
        ts = _parse_ts(m.group("ts"))
        if prev_ts is not None:
            assert ts >= prev_ts, (
                f"Timestamps in {file_path} are not in chronological order "
                f"(line {line_no}: {ts.isoformat()} < {prev_ts.isoformat()})."
            )
        prev_ts = ts


def test_at_least_one_failed_event_exists_across_all_logs():
    """
    Down-stream tasks depend on the existence of at least one failed login.
    Ensure there is at least one “status=failed” line across all inputs.
    """
    failed_found = False
    offending_files: list[str] = []

    for file_path in RAW_LOG_FILES:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            m = LINE_RE.match(line)
            # Skip malformed lines (they're checked elsewhere).
            if not m:
                continue
            if m.group("status") == "failed":
                failed_found = True
                break
        else:
            offending_files.append(str(file_path))
        if failed_found:
            break

    assert failed_found, (
        "No lines with 'status=failed' were found in any input log file. "
        "At least one failed login must be present to satisfy the task "
        "requirements.\nFiles checked with no failures: " + ", ".join(offending_files)
    )