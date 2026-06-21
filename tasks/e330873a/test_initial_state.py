# test_initial_state.py
#
# This pytest suite verifies the **initial** state of the filesystem
# before the student’s solution is executed.  It checks:
#   1. Presence and permissions of required directories.
#   2. Presence, permissions, line-ending style and exact contents of
#      /home/user/logs/app.log.
#   3. That /home/user/output/ exists **and is empty**.
#
# If any check fails the assertion message explains precisely what is
# missing or incorrect.
#
# NOTE:  Absolutely no checks are performed for the files that the
#        student is expected to create later; only the initial state
#        is validated.

import os
import stat
import json
import pytest
from pathlib import Path

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
OUTPUT_DIR = HOME / "output"
APP_LOG = LOGS_DIR / "app.log"

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def _mode(path: Path) -> int:
    """Return the permission bits of a path, e.g. 0o755."""
    return stat.S_IMODE(path.stat().st_mode)

def _read_lines_no_cr(path: Path):
    """Return list of lines (without LF) and assert file is LF-only."""
    raw = path.read_bytes()
    assert b"\r" not in raw, f"{path} must use LF line endings only (found CR)."
    # Splitlines(keepends=False) drops line endings cleanly.
    return raw.decode("utf-8").splitlines()

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_directories_exist_and_permissions():
    # logs dir
    assert LOGS_DIR.is_dir(), f"Missing directory: {LOGS_DIR}"
    assert _mode(LOGS_DIR) == 0o755, (
        f"{LOGS_DIR} permissions expected 755, got {oct(_mode(LOGS_DIR))}"
    )

    # output dir
    assert OUTPUT_DIR.is_dir(), f"Missing directory: {OUTPUT_DIR}"
    assert _mode(OUTPUT_DIR) == 0o755, (
        f"{OUTPUT_DIR} permissions expected 755, got {oct(_mode(OUTPUT_DIR))}"
    )

def test_output_directory_is_empty():
    contents = list(OUTPUT_DIR.iterdir())
    assert contents == [], (
        f"{OUTPUT_DIR} must be empty before the task starts; found: "
        + ", ".join(str(p.name) for p in contents)
    )

def test_app_log_exists_and_permissions():
    assert APP_LOG.is_file(), f"Missing log file: {APP_LOG}"
    assert _mode(APP_LOG) == 0o644, (
        f"{APP_LOG} permissions expected 644, got {oct(_mode(APP_LOG))}"
    )

def test_app_log_content_exact():
    expected_lines = [
        '{"timestamp":"2023-10-01T12:00:00Z","level":"INFO","message":"Service started"}',
        '{"timestamp":"2023-10-01T12:05:00Z","level":"ERROR","message":"Failed to connect to DB","error_code":"ERR001"}',
        '{"timestamp":"2023-10-01T12:06:00Z","level":"ERROR","message":"Null pointer exception","error_code":"ERR002"}',
        '{"timestamp":"2023-10-01T12:07:00Z","level":"ERROR","message":"Invalid input data"}',
        '{"timestamp":"2023-10-01T12:08:00Z","level":"WARN","message":"High memory usage"}',
    ]

    lines = _read_lines_no_cr(APP_LOG)
    assert lines == expected_lines, (
        f"{APP_LOG} contents do not match the expected initial log lines.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n\nFound ({len(lines)} lines):\n"
        + "\n".join(lines)
    )

def test_app_log_contains_valid_json():
    """
    The file must contain exactly five single-line JSON objects that parse
    without error.  This is a sanity check on structure, not schema.
    """
    lines = _read_lines_no_cr(APP_LOG)
    assert len(lines) == 5, "app.log must have exactly 5 lines."

    for idx, line in enumerate(lines, start=1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            pytest.fail(f"Line {idx} in {APP_LOG} is not valid JSON: {e}")