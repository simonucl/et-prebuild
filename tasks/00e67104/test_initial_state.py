# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student’s solution is run.
#
# Rules checked:
#   1. /home/user/build/logs/ directory exists.
#   2. /home/user/build/reports/ directory exists and is empty.
#   3. /home/user/build/logs/mobile_build.log exists and contains exactly
#      the 23 expected lines (each terminated by '\n').
#
# No checks are performed on any output artefacts that are supposed to be
# created by the student’s solution.

import os
import stat
import pytest

HOME = "/home/user"
LOGS_DIR = os.path.join(HOME, "build", "logs")
REPORTS_DIR = os.path.join(HOME, "build", "reports")
LOG_FILE = os.path.join(LOGS_DIR, "mobile_build.log")


EXPECTED_LOG_LINES = [
    "INFO: Build started\n",
    "WARNING: Unused resource\n",
    "INFO: Checking dependencies\n",
    "WARNING: Deprecated API usage\n",
    "INFO: Running Lint\n",
    "WARNING: Unused resource\n",
    "ERROR: Missing keystore\n",
    "WARNING: Missing translation\n",
    "INFO: Compiling sources\n",
    "WARNING: Deprecated API usage\n",
    "INFO: Packaging APK\n",
    "WARNING: Unused resource\n",
    "ERROR: Build failed\n",
    "WARNING: Large APK size\n",
    "INFO: Build environment: Android-30\n",
    "WARNING: Missing translation\n",
    "INFO: Retrying build steps\n",
    "WARNING: Deprecated API usage\n",
    "INFO: Re-running unit tests\n",
    "INFO: Build completed with warnings\n",
    "WARNING: Unused resource\n",
    "INFO: Archiving artifacts\n",
    "INFO: Pipeline finished\n",
]


def _assert_mode(path: str, expected_octal: int):
    """
    Helper: ensure the permission bits of `path` match `expected_octal`
    (e.g. 0o755).  Produces a clear error message on mismatch.
    """
    actual_mode = stat.S_IMODE(os.stat(path).st_mode)
    assert actual_mode == expected_octal, (
        f"Path {path!r} exists but has mode {oct(actual_mode)}, "
        f"expected {oct(expected_octal)}"
    )


def test_logs_directory_exists():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory {LOGS_DIR!r} is missing or not a directory."
    )
    _assert_mode(LOGS_DIR, 0o755)


def test_reports_directory_exists_and_empty():
    # Directory existence & permissions
    assert os.path.isdir(REPORTS_DIR), (
        f"Required directory {REPORTS_DIR!r} is missing or not a directory."
    )
    _assert_mode(REPORTS_DIR, 0o755)

    # Must be empty before the student's script runs
    contents = os.listdir(REPORTS_DIR)
    assert contents == [], (
        f"Directory {REPORTS_DIR!r} should be empty before execution, "
        f"but contains: {contents}"
    )


def test_mobile_build_log_exists_and_content():
    # File presence & permissions
    assert os.path.isfile(LOG_FILE), (
        f"Required log file {LOG_FILE!r} is missing."
    )
    _assert_mode(LOG_FILE, 0o644)

    # Read and validate contents
    with open(LOG_FILE, encoding="utf-8") as fh:
        file_lines = fh.readlines()

    # Check line count first for quick feedback
    expected_count = len(EXPECTED_LOG_LINES)
    actual_count = len(file_lines)
    assert actual_count == expected_count, (
        f"{LOG_FILE!r} should contain exactly {expected_count} lines, "
        f"found {actual_count}."
    )

    # Check each line verbatim (including newline endings)
    mismatches = [
        (idx + 1, exp.rstrip("\n"), got.rstrip("\n"))
        for idx, (exp, got) in enumerate(zip(EXPECTED_LOG_LINES, file_lines))
        if exp != got
    ]

    assert not mismatches, (
        f"Content mismatch in {LOG_FILE!r}.\n"
        + "\n".join(
            f"Line {lineno}: expected {exp!r}, got {got!r}"
            for lineno, exp, got in mismatches
        )
    )