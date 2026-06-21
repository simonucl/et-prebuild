# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state expected by the
# exercise is present **before** the student runs any solution code.
#
# It checks only the required source material under /home/user/build_logs/ and
# deliberately ignores the yet-to-be-created output artefacts under
# /home/user/artifact_reports/.

import os
from pathlib import Path
import pytest

BUILD_LOG_DIR = Path("/home/user/build_logs")

# --------------------------------------------------------------------------- #
# Expected build-log contents (verbatim, including blank spaces).
# A final newline is expected at the end of each file, matching typical
# POSIX tools’ behaviour.
# --------------------------------------------------------------------------- #
EXPECTED_CONTENT = {
    "appserver_build.log": (
        "2023-07-19 14:20:55 [INFO ] Starting build for appserver\n"
        "2023-07-19 14:20:56 [WARN ] Deprecated API usage detected\n"
        "2023-07-19 14:20:57 [INFO ] Compiling modules...\n"
        "2023-07-19 14:20:58 [ERROR] Failed to copy artifact artifact-xyz.jar\n"
        "2023-07-19 14:21:10 Build step completed\n"
        "2023-07-19 14:21:15 [INFO ] Running unit tests...\n"
        "2023-07-19 14:21:20 [ERROR] Test suite failed for module security\n"
        "2023-07-19 14:21:45  Tests run: 230, Failures: 3, Errors: 0, Skipped: 1\n"
        "2023-07-19 14:22:12 Build step failed with code E5678\n"
        "2023-07-19 14:22:20 [INFO ] Build finished with status FAILED\n"
    ),
    "db_build.log": (
        "2023-07-19 14:00:01 [INFO ] Starting build for database layer\n"
        "2023-07-19 14:00:05 [WARN ] Outdated driver version detected\n"
        "2023-07-19 14:00:07 [INFO ] Executing migrations...\n"
        "2023-07-19 14:00:09 Script completed successfully\n"
        "2023-07-19 14:00:10 [ERROR] Migration 20230719_add_index.sql failed\n"
        "2023-07-19 14:00:11 Error code E3141 encountered during migration\n"
        "2023-07-19 14:00:15 [INFO ] Build finished with status FAILED\n"
    ),
    "ui_build.log": (
        "2023-07-19 13:40:10 [INFO ] Starting build for UI\n"
        "2023-07-19 13:40:12 [INFO ] Installing dependencies...\n"
        "2023-07-19 13:40:18 [WARN ] Package \"left-pad\" is deprecated\n"
        "2023-07-19 13:40:28 [INFO ] Running lint...\n"
        "2023-07-19 13:40:30  Lint failed at component Navbar with E0987\n"
        "2023-07-19 13:40:33 [INFO ] Running unit tests...\n"
        "2023-07-19 13:40:45 [ERROR] 12 tests failed\n"
        "2023-07-19 13:40:55 [INFO ] Build finished with status FAILED\n"
    ),
}


def _normalise_newlines(text: str) -> str:
    """
    Convert CRLF to LF and ensure exactly one newline at EOF (to make comparison
    robust across editors).
    """
    text = text.replace("\r\n", "\n")
    # Guarantee a single trailing newline for comparison
    if not text.endswith("\n"):
        text += "\n"
    return text


def test_build_logs_directory_exists():
    assert BUILD_LOG_DIR.is_dir(), (
        f"Required directory {BUILD_LOG_DIR} is missing. "
        "All pre-existing build logs must be placed there."
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_CONTENT))
def test_each_expected_log_file_exists(filename):
    file_path = BUILD_LOG_DIR / filename
    assert file_path.is_file(), (
        f"Expected log file {file_path} is missing."
    )


def test_no_missing_expected_files():
    existing_logs = {p.name for p in BUILD_LOG_DIR.glob("*.log")}
    expected_logs = set(EXPECTED_CONTENT)
    missing = expected_logs - existing_logs
    assert not missing, (
        f"The following expected log files are missing from {BUILD_LOG_DIR}: "
        f"{', '.join(sorted(missing))}"
    )


@pytest.mark.parametrize("filename,expected_raw", EXPECTED_CONTENT.items())
def test_log_file_contents_match_spec(filename, expected_raw):
    """
    Ensure that every build log file exactly matches the exercise specification.
    This guards against silent corruption or accidental edits.
    """
    file_path = BUILD_LOG_DIR / filename
    actual = file_path.read_text(encoding="utf-8")
    assert _normalise_newlines(actual) == _normalise_newlines(expected_raw), (
        f"Content mismatch in {file_path}.\n"
        "The file must contain exactly the lines specified in the assignment."
    )


def test_no_unexpected_log_files():
    """
    There should be *only* the three log files referenced by the task inside
    /home/user/build_logs/.  Any extra *.log files may cause the student's
    parsing logic to pick up unintended data.
    """
    unexpected = {
        p.name for p in BUILD_LOG_DIR.glob("*.log")
        if p.name not in EXPECTED_CONTENT
    }
    assert not unexpected, (
        "Unexpected .log files found in /home/user/build_logs/: "
        f"{', '.join(sorted(unexpected))}. "
        "Remove or move them out of the directory before running the exercise."
    )