# test_initial_state.py
"""
Pytest suite that validates the operating-system / filesystem **before**
the student runs any solution code.

It checks the following pre-conditions:

1. The directory /home/user/builds exists.
2. The file /home/user/builds/jenkins_build.log exists and is a regular file.
3. The log file is valid UTF-8 and contains exactly three occurrences of the
   literal string 'BUILD SUCCESS'.
4. The directory /home/user/builds/analysis must **not** exist yet.

These checks guarantee that the environment starts in the expected state
so that subsequent grading logic can rely on a consistent baseline.
"""

from pathlib import Path
import pytest

BUILD_DIR = Path("/home/user/builds")
LOG_FILE = BUILD_DIR / "jenkins_build.log"
ANALYSIS_DIR = BUILD_DIR / "analysis"


def test_build_directory_exists():
    """
    /home/user/builds must already exist and be a directory.
    """
    assert BUILD_DIR.exists(), (
        f"Expected directory {BUILD_DIR} to exist, but it is missing."
    )
    assert BUILD_DIR.is_dir(), (
        f"Expected {BUILD_DIR} to be a directory, but it is not."
    )


def test_log_file_present():
    """
    /home/user/builds/jenkins_build.log must exist and be a regular file.
    """
    assert LOG_FILE.exists(), (
        f"Expected log file {LOG_FILE} to exist, but it is missing."
    )
    assert LOG_FILE.is_file(), (
        f"Expected {LOG_FILE} to be a regular file, but it is not."
    )


def test_log_file_utf8_and_exact_count():
    """
    The log file must be valid UTF-8 and contain exactly three occurrences
    of the literal string 'BUILD SUCCESS'.
    """
    try:
        content = LOG_FILE.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(
            f"Log file {LOG_FILE} is not valid UTF-8: {exc}"
        )

    count = content.count("BUILD SUCCESS")
    assert count == 3, (
        f"Expected exactly 3 occurrences of 'BUILD SUCCESS' in "
        f"{LOG_FILE}, but found {count}."
    )


def test_analysis_directory_absent():
    """
    /home/user/builds/analysis must NOT exist before the student runs the solution.
    """
    assert not ANALYSIS_DIR.exists(), (
        f"Directory {ANALYSIS_DIR} should not exist before running the task; "
        "it must be created by the student's command."
    )