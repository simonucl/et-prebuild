# test_initial_state.py
#
# Pytest suite that validates the _initial_ operating-system / filesystem
# state for the “build-logs” exercise _before_ the student performs any work.
#
# WHAT IS TESTED
# 1. The logs directory /home/user/builds/logs/ exists.
# 2. The three expected *.log files exist at their full, absolute paths.
# 3. Each log file contains the exact, ground-truth line-counts for
#    total, INFO, WARN and ERROR lines.
# 4. Across all log files, the chronologically latest ERROR entry is
#    exactly the one specified in the task description.
#
# IMPORTANT
# * No assertions are made about /home/user/builds/reports/ or its content,
#   because the student has not created those yet and the grading rubric
#   explicitly forbids testing the output files/directories at this stage.
#
# Only the Python standard library and pytest are used.

import datetime as _dt
import pathlib as _pl
import re as _re

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the ground-truth initial state
# --------------------------------------------------------------------------- #

LOG_DIR = _pl.Path("/home/user/builds/logs")

EXPECTED_FILES = {
    "build_2024-06-01.log": dict(total=7, info=5, warn=1, error=1),
    "build_2024-06-02.log": dict(total=6, info=5, warn=1, error=0),
    "build_2024-06-03.log": dict(total=7, info=4, warn=1, error=2),
}

LATEST_ERROR = dict(
    timestamp="2024-06-03 08:00:25",
    file="build_2024-06-03.log",
    message="Failed to compile module C: unresolved reference",
)

# Regex for parsing one log line.
# Example line: "[2024-06-03 08:00:25] ERROR Something bad happened"
_LINE_RE = _re.compile(
    r"""
    ^\[(?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]  # timestamp in brackets
    \s+
    (?P<level>INFO|WARN|ERROR)                         # log level
    \s+
    (?P<msg>.+)$                                       # message
    """,
    _re.VERBOSE,
)


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _scan_file(path: _pl.Path):
    """
    Scan a single .log file and return a dictionary with the following keys:
        total, info, warn, error, error_entries (list of (ts_str, msg) tuples)
    """
    counts = dict(total=0, info=0, warn=0, error=0)
    error_entries = []

    with path.open("rt", encoding="utf-8") as fh:
        for line in fh:
            counts["total"] += 1
            m = _LINE_RE.match(line.rstrip("\n"))
            if not m:
                # A line that doesn't follow the expected pattern is still a
                # line, but does not affect INFO/WARN/ERROR counts.
                continue

            level = m.group("level")
            if level == "INFO":
                counts["info"] += 1
            elif level == "WARN":
                counts["warn"] += 1
            elif level == "ERROR":
                counts["error"] += 1
                error_entries.append((m.group("ts"), m.group("msg")))

    counts["error_entries"] = error_entries
    return counts


def _latest_error_across_logs():
    """
    Return a tuple (ts_str, filename, message) representing the chronologically
    latest ERROR across all expected log files.
    """
    latest_dt = None
    latest_data = None

    for fname in EXPECTED_FILES:
        path = LOG_DIR / fname
        data = _scan_file(path)
        for ts_str, msg in data["error_entries"]:
            ts_dt = _dt.datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            if latest_dt is None or ts_dt > latest_dt:
                latest_dt = ts_dt
                latest_data = (ts_str, fname, msg)

    return latest_data


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    """The directory /home/user/builds/logs/ must exist and be a directory."""
    assert LOG_DIR.exists(), (
        f"Expected directory {LOG_DIR} does not exist. "
        "The exercise requires the logs to be pre-populated here."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES.keys()))
def test_each_log_file_exists(filename):
    """Each expected .log file must exist at its full path."""
    full_path = LOG_DIR / filename
    assert full_path.exists(), (
        f"Missing required log file: {full_path}\n"
        "The initial state must contain this file."
    )
    assert full_path.is_file(), f"{full_path} exists but is not a regular file."


@pytest.mark.parametrize("filename,expected", sorted(EXPECTED_FILES.items()))
def test_log_file_counts(filename, expected):
    """
    The total, INFO, WARN and ERROR line counts for every log file must match
    the ground-truth values given in the task description.
    """
    full_path = LOG_DIR / filename
    observed = _scan_file(full_path)

    for key in ("total", "info", "warn", "error"):
        assert (
            observed[key] == expected[key]
        ), (
            f"Count mismatch in {full_path} for '{key}': "
            f"expected {expected[key]}, found {observed[key]}"
        )


def test_latest_error_details():
    """
    Across all log files, the chronologically latest ERROR line must match
    the specification in the task description.
    """
    latest = _latest_error_across_logs()
    assert latest is not None, "No ERROR entries were found in any log file."

    ts_str, fname, msg = latest

    assert (
        ts_str == LATEST_ERROR["timestamp"]
    ), f"Latest ERROR timestamp mismatch: expected {LATEST_ERROR['timestamp']}, found {ts_str}"

    assert (
        fname == LATEST_ERROR["file"]
    ), f"Latest ERROR file mismatch: expected {LATEST_ERROR['file']}, found {fname}"

    assert (
        msg == LATEST_ERROR["message"]
    ), f"Latest ERROR message mismatch: expected '{LATEST_ERROR['message']}', found '{msg}'"