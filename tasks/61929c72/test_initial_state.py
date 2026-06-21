# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem / OS state
# is exactly what the student is told to start with for the “alert-digest”
# exercise.  It intentionally does **not** look for any artefacts that
# will be produced by the solution – it only inspects items that must be
# present *before* the student begins working.

import re
import os
import stat
import tempfile
from pathlib import Path
from datetime import datetime
import pytest

# ----------------------------------------------------------------------
# Constant paths
# ----------------------------------------------------------------------

HOME = Path("/home/user")
LOG_DIR = HOME / "research_logs"
ANALYSIS_DIR = HOME / "analysis"

EXP_A = LOG_DIR / "experiment_A.log"
EXP_B = LOG_DIR / "experiment_B.log"
CTRL  = LOG_DIR / "experiment_control.log"

# Expected counts derived from the task description
EXPECTED_WARN_ERROR_COUNT = 6
EXPECTED_CHECKSUM_COUNT   = 3

# Expected ordered digest lines (for extra safety we recompute them from
# the source logs, but the list is here so that test failures can show
# exactly what went wrong).
EXPECTED_DIGEST_LINES = [
    "[2023-04-12 10:01:01] INFO  Monitor: checksum validated",
    "[2023-04-12 10:05:11] WARN  DataLoad: Incomplete record encountered",
    "[2023-04-12 10:12:21] WARN  DataLoad: Missing value filled",
    "[2023-04-12 10:17:45] ERROR DataLoad: Null pointer exception",
    "[2023-04-12 10:31:18] INFO  Monitor: checksum validated",
    "[2023-04-12 10:55:09] ERROR DataLoad: Index out of range",
    "[2023-04-12 11:45:12] WARN  DataLoad: Timeout on socket 3",
    "[2023-04-12 11:46:45] INFO  Monitor: checksum validated",
    "[2023-04-12 11:59:59] WARN  DataLoad: Disk read latency high",
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

TIMESTAMP_RE = re.compile(
    r"""
    ^\[
        (?P<date>\d{4}-\d{2}-\d{2})\s+
        (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})
    \]\s+
    (?P<level>INFO|WARN|ERROR)\s+
    (?P<module>\w+):
    """,
    re.VERBOSE,
)

def parse_timestamp(line: str) -> datetime | None:
    """Extract a datetime object from a log line; return None on mismatch."""
    m = TIMESTAMP_RE.match(line)
    if not m:
        return None
    return datetime.strptime(
        f"{m.group('date')} {m.group('hour')}:{m.group('minute')}:{m.group('second')}",
        "%Y-%m-%d %H:%M:%S",
    )

def matches_filters(line: str) -> bool:
    """
    Return True if `line` satisfies:
      * module == DataLoad
      * level  == WARN or ERROR
      * timestamp between 2023-04-12 10:00:00 and 11:59:59 inclusive
    """
    m = TIMESTAMP_RE.match(line)
    if not m:
        return False

    if m.group("module") != "DataLoad":
        return False

    if m.group("level") not in {"WARN", "ERROR"}:
        return False

    dt = parse_timestamp(line)
    if dt is None:
        return False

    start = datetime(2023, 4, 12, 10, 0, 0)
    end   = datetime(2023, 4, 12, 11, 59, 59)
    return start <= dt <= end

def checksum_line(line: str) -> bool:
    """Return True if the line contains the exact substring 'checksum validated'."""
    return "checksum validated" in line

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_directories_exist_and_writable():
    # All required directories must already exist.
    for path in (LOG_DIR, ANALYSIS_DIR):
        assert path.exists(), f"Required directory {path} is missing."
        assert path.is_dir(), f"{path} exists but is not a directory."

    # The analysis directory must be writable by the current user.
    testfile = None
    try:
        with tempfile.NamedTemporaryFile(dir=ANALYSIS_DIR, delete=False) as tf:
            testfile = Path(tf.name)
            tf.write(b"probe")
        assert testfile.exists(), f"Cannot create files in {ANALYSIS_DIR} – directory not writable."
    finally:
        # Clean up the probe file (ignore any errors).
        if testfile and testfile.exists():
            testfile.unlink(missing_ok=True)

@pytest.mark.parametrize(
    "filepath",
    [EXP_A, EXP_B, CTRL],
)
def test_log_files_exist(filepath: Path):
    assert filepath.exists(), f"Expected log file {filepath} is missing."
    assert filepath.is_file(), f"{filepath} exists but is not a regular file."
    # Sanity check: file must not be empty.
    assert filepath.stat().st_size > 0, f"Log file {filepath} is empty."

def test_filtered_line_counts_and_order():
    """Validate that the source logs contain exactly the lines described."""
    warn_error_lines = []
    for path in (EXP_A, EXP_B):
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if matches_filters(line):
                    warn_error_lines.append(line)

    checksum_lines = []
    with CTRL.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if checksum_line(line):
                checksum_lines.append(line)

    assert len(warn_error_lines) == EXPECTED_WARN_ERROR_COUNT, (
        f"Expected {EXPECTED_WARN_ERROR_COUNT} WARN/ERROR DataLoad lines across "
        f"{EXP_A.name} and {EXP_B.name}, but found {len(warn_error_lines)}.\n"
        f"Lines found:\n" + "\n".join(warn_error_lines)
    )

    assert len(checksum_lines) == EXPECTED_CHECKSUM_COUNT, (
        f"Expected {EXPECTED_CHECKSUM_COUNT} checksum lines in {CTRL.name}, "
        f"but found {len(checksum_lines)}.\nLines found:\n" + "\n".join(checksum_lines)
    )

    # Merge and sort chronologically to ensure the ordering is exactly as
    # the task description states.
    combined = warn_error_lines + checksum_lines
    combined_sorted = sorted(
        combined,
        key=lambda ln: parse_timestamp(ln) or datetime.min,
    )

    assert combined_sorted == EXPECTED_DIGEST_LINES, (
        "The chronological ordering or the content of the initial log lines "
        "does not match the exercise description.\n"
        "Expected:\n" + "\n".join(EXPECTED_DIGEST_LINES) + "\n\n"
        "Found:\n" + "\n".join(combined_sorted)
    )