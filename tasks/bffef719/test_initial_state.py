# test_initial_state.py
"""
Pytest suite that validates the initial state of the filesystem before the
student performs any action.

This file checks only the *input* artefacts that must already be present.
It purposely does NOT check for any output files or directories, per the
specification.
"""

from pathlib import Path
import os
import pytest

HOME = Path("/home/user")
BUILD_DIR = HOME / "build_logs"
LOG_FILE = BUILD_DIR / "ci_build.log"

# --------------------------------------------------------------------------- #
# Helper: the exact expected contents of /home/user/build_logs/ci_build.log
# Every line ends with a single UNIX newline.
# --------------------------------------------------------------------------- #
EXPECTED_LOG_CONTENT = (
    "[2023-09-12 10:15:01] [INFO] Starting build step 1\n"
    "[2023-09-12 10:15:05] [ERROR] Failed to fetch dependencies\n"
    "[2023-09-12 10:16:12] [WARN] Deprecated API usage\n"
    "[2023-09-12 10:17:30] [INFO] Running unit tests\n"
    "[2023-09-12 10:17:45] [ERROR] Unit test failures detected\n"
    "[2023-09-12 10:18:02] [INFO] Build completed\n"
    "[2023-09-12 10:18:06] [ERROR] Post-build hook failed\n"
)


@pytest.fixture(scope="module")
def log_text():
    """Read and return the contents of the CI build log."""
    if not LOG_FILE.exists():
        pytest.skip(f"Required log file {LOG_FILE} is missing; test cannot proceed.")
    return LOG_FILE.read_text(encoding="utf-8")


def test_build_logs_directory_exists():
    assert BUILD_DIR.is_dir(), (
        f"The directory {BUILD_DIR} does not exist. "
        "It must be present before the task starts."
    )


def test_ci_build_log_exists():
    assert LOG_FILE.is_file(), (
        f"The build log {LOG_FILE} is missing. "
        "The task requires this file to already exist."
    )


def test_ci_build_log_contents_exact(log_text):
    assert log_text == EXPECTED_LOG_CONTENT, (
        f"The contents of {LOG_FILE} are not as expected.\n"
        "Expected:\n"
        "--------------------------------\n"
        f"{EXPECTED_LOG_CONTENT}"
        "--------------------------------\n"
        "Found:\n"
        "--------------------------------\n"
        f"{log_text}"
        "--------------------------------\n"
        "Please ensure the initial log file has exactly the required lines, "
        "each terminated by a single UNIX newline."
    )