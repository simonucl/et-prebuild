# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the student’s solution runs.  The tests assert that:
#   • All expected *.log files already exist under /home/user/distributed-logs/
#   • Each file’s contents exactly match the specification given in the task
#   • No deployment artefacts (directory or release_blockers.log) exist yet
#
# The assertions use full, absolute paths and provide clear failure messages.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected initial state
# --------------------------------------------------------------------------- #

LOG_DIR = Path("/home/user/distributed-logs")

EXPECTED_LOG_CONTENT = {
    LOG_DIR / "frontend.log": [
        "[2023-07-01 10:00:00] Service frontend: HealthCheck: OK",
        "[2023-07-01 10:05:00] Service frontend: HealthCheck: OK",
        "[2023-07-01 10:10:00] Service frontend: HealthCheck: FAILED",
        "[2023-07-01 10:15:00] Service frontend: HealthCheck: OK",
    ],
    LOG_DIR / "backend.log": [
        "[2023-07-01 10:00:00] Service backend: HealthCheck: OK",
        "[2023-07-01 10:05:00] Service backend: HealthCheck: FAILED",
        "[2023-07-01 10:10:00] Service backend: HealthCheck: FAILED",
    ],
    LOG_DIR / "auth.log": [
        "[2023-07-01 10:00:00] Service auth: HealthCheck: OK",
        "[2023-07-01 10:05:00] Service auth: HealthCheck: OK",
    ],
    LOG_DIR / "payments.log": [
        "[2023-07-01 10:00:00] Service payments: HealthCheck: FAILED",
        "[2023-07-01 10:05:00] Service payments: HealthCheck: OK",
    ],
    LOG_DIR / "cache.log": [
        "[2023-07-01 10:00:00] Service cache: HealthCheck: OK",
        "[2023-07-01 10:05:00] Service cache: HealthCheck: OK",
    ],
}

DEPLOYMENT_DIR = Path("/home/user/deployment")
RELEASE_BLOCKERS_FILE = DEPLOYMENT_DIR / "release_blockers.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def read_file_lines(path: Path):
    """
    Read a text file and return a list of lines with trailing newlines stripped.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_log_directory_exists_and_is_dir():
    assert LOG_DIR.exists(), f"Expected directory {LOG_DIR} to exist."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


@pytest.mark.parametrize("log_path,expected_lines", EXPECTED_LOG_CONTENT.items())
def test_each_expected_log_file_exists(log_path: Path, expected_lines):
    assert log_path.exists(), f"Expected log file {log_path} to exist."
    assert log_path.is_file(), f"{log_path} exists but is not a regular file."

    actual_lines = read_file_lines(log_path)
    assert actual_lines == expected_lines, (
        f"Contents of {log_path} do not match the specification.\n"
        f"--- Expected ({len(expected_lines)} lines) ---\n"
        + "\n".join(expected_lines)
        + "\n--- Actual ({len_actual} lines) ---\n".format(len_actual=len(actual_lines))
        + "\n".join(actual_lines)
    )


def test_no_unexpected_deployment_artifacts_exist():
    """
    Before the student runs their solution, the deployment directory and
    release_blockers.log file should NOT exist.
    """
    assert not RELEASE_BLOCKERS_FILE.exists(), (
        f"Found {RELEASE_BLOCKERS_FILE} but it should not exist yet."
    )

    # The directory may or may not exist; if it exists already, it must be empty.
    if DEPLOYMENT_DIR.exists():
        assert DEPLOYMENT_DIR.is_dir(), (
            f"{DEPLOYMENT_DIR} exists but is not a directory."
        )
        # Accept an empty directory, but fail if it contains any files.
        contents = list(DEPLOYMENT_DIR.iterdir())
        assert not contents, (
            f"{DEPLOYMENT_DIR} should be empty at this point, "
            f"but found: {', '.join(str(p) for p in contents)}"
        )