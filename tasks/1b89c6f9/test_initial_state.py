# test_initial_state.py
"""
Pytest suite that verifies the initial filesystem state for the
“quick, one–off security-style scan” exercise.

This file only checks the _pre-task_ conditions.  It intentionally
does NOT look for the student’s output file
(/home/user/security_scan_report.txt); the grading harness will
validate that separately after the student’s work is complete.

Constraints:
* stdlib + pytest only
* Explicit, full paths are used
"""

from pathlib import Path

LOG_DIR = Path("/home/user/app/logs")
LOG_FILE = LOG_DIR / "latest.log"


def test_log_directory_exists():
    assert LOG_DIR.exists(), (
        f"Required directory does not exist: {LOG_DIR}"
    )
    assert LOG_DIR.is_dir(), (
        f"Expected {LOG_DIR} to be a directory, but it is not."
    )


def test_latest_log_file_exists_and_is_file():
    assert LOG_FILE.exists(), (
        f"Required log file is missing: {LOG_FILE}"
    )
    assert LOG_FILE.is_file(), (
        f"Expected {LOG_FILE} to be a regular file, but it is not."
    )


def test_latest_log_contains_expected_traceback_count():
    """
    The exercise description (and hidden ground-truth) state that
    the log file initially contains exactly three lines with the
    uppercase substring 'TRACEBACK'.  Confirm that so students who
    rely on this fact can succeed.
    """
    content = LOG_FILE.read_text(encoding="utf-8").splitlines()

    traceback_lines = [ln for ln in content if "TRACEBACK" in ln]
    count = len(traceback_lines)

    assert count == 3, (
        f"Expected exactly 3 lines containing 'TRACEBACK' in "
        f"{LOG_FILE}, but found {count}.\n"
        f"Lines found:\n" + "\n".join(traceback_lines)
    )