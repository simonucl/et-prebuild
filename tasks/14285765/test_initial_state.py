# test_initial_state.py
#
# This pytest file validates that the operating-system state required
# *before* the student’s solution runs is present and correct.
#
# It checks ONLY the prerequisite inputs—never any output that the
# student is expected to create.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
APP_DIR = HOME / "app"
LOG_DIR = APP_DIR / "logs"
VERSION_FILE = APP_DIR / "VERSION"

EXPECTED_VERSION = "v2.5.1-beta"
EXPECTED_TOTAL_LOG_FILES = 3
EXPECTED_ERROR_LINES = 2
EXPECTED_DEBUG_LINES = 2
EXPECTED_LATEST_LOG_TS = "2023-04-01T12:10:03Z"


def read_text(path: pathlib.Path) -> str:
    """Utility: read file as UTF-8 text."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Required file is missing: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def test_version_file_exists_and_contents():
    assert VERSION_FILE.is_file(), (
        f"VERSION file not found at expected path: {VERSION_FILE}"
    )
    content = read_text(VERSION_FILE).rstrip("\n")
    assert content == EXPECTED_VERSION, (
        f"VERSION file content mismatch.\n"
        f"Expected: {EXPECTED_VERSION!r}\n"
        f"Found:    {content!r}"
    )


def test_log_directory_and_file_count():
    assert LOG_DIR.is_dir(), f"Logs directory missing: {LOG_DIR}"
    log_files = sorted(LOG_DIR.glob("*.log"))
    assert len(log_files) == EXPECTED_TOTAL_LOG_FILES, (
        f"Expected {EXPECTED_TOTAL_LOG_FILES} '*.log' files in {LOG_DIR}, "
        f"found {len(log_files)} ({[p.name for p in log_files]})"
    )


def _count_string_occurrences(log_files, literal):
    """Count lines containing the literal string in the given files."""
    total = 0
    for path in log_files:
        for line in read_text(path).splitlines():
            if literal in line:
                total += 1
    return total


def test_error_and_debug_line_counts():
    log_files = sorted(LOG_DIR.glob("*.log"))
    error_lines = _count_string_occurrences(log_files, "ERROR")
    debug_lines = _count_string_occurrences(log_files, "DEBUG")

    assert error_lines == EXPECTED_ERROR_LINES, (
        f"ERROR line count mismatch.\n"
        f"Expected: {EXPECTED_ERROR_LINES}\n"
        f"Found:    {error_lines}"
    )
    assert debug_lines == EXPECTED_DEBUG_LINES, (
        f"DEBUG line count mismatch.\n"
        f"Expected: {EXPECTED_DEBUG_LINES}\n"
        f"Found:    {debug_lines}"
    )


def test_latest_log_timestamp():
    log_files = sorted(LOG_DIR.glob("*.log"))
    assert log_files, f"No log files found in {LOG_DIR}"

    # Pure ASCII lexicographic order; the last element of `sorted` suffices
    latest_file = log_files[-1]

    last_line = read_text(latest_file).splitlines()[-1]
    # The timestamp is the first field on the line, separated by whitespace.
    timestamp = last_line.split(maxsplit=1)[0]

    assert timestamp == EXPECTED_LATEST_LOG_TS, (
        f"Latest log timestamp mismatch.\n"
        f"Expected: {EXPECTED_LATEST_LOG_TS}\n"
        f"Found:    {timestamp}\n"
        f"In file:  {latest_file}"
    )