# test_initial_state.py
#
# This pytest file validates the *initial* filesystem state that must exist
# BEFORE the student runs any commands for the “CI/CD log-trimming” task.
#
# Expectations for the pristine environment:
#
# 1. The directory /home/user/ci_logs/ **exists**.
# 2. Exactly three raw log files already live inside that directory
#    and their *entire* contents match the specification given in
#    the assignment:
#
#       ├── build_backend_20230912.log
#       ├── build_frontend_20230912.log
#       └── build_docs_20230912.log
#
# 3. The helper artifacts the student is supposed to create later
#    must *not* be present yet.  Concretely:
#
#       • /home/user/ci_logs/trimmed_logs/          (directory)
#       • /home/user/ci_logs/error_summary.tsv      (file)
#
# If any of these checks fail, the test suite provides an explicit,
# human-readable error message so that the learner knows exactly what
# is missing or incorrect.
#
# Only the Python standard library and pytest are used.
import os
from pathlib import Path

import pytest

CI_DIR = Path("/home/user/ci_logs")

# ---------------------------------------------------------------------------
# Expected raw log files and their exact, line-for-line contents
# ---------------------------------------------------------------------------
EXPECTED_LOGS = {
    "build_backend_20230912.log": [
        "[INFO] Starting backend build",
        "[INFO] Fetching dependencies",
        "[ERROR] Missing dependency: libfoo",
        "[INFO] Retrying...",
        "[ERROR] Missing dependency: libfoo",
        "[INFO] Build failed",
    ],
    "build_frontend_20230912.log": [
        "[INFO] Starting frontend build",
        "[INFO] Installing packages",
        "[INFO] Compiling TypeScript",
        "[ERROR] Can't resolve './App'",
        "[ERROR] Can't resolve './Header'",
        "[INFO] Build failed",
    ],
    "build_docs_20230912.log": [
        "[INFO] Starting docs build",
        "[INFO] Generating docs",
        "[INFO] Docs build completed successfully",
    ],
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def read_file_lines(path: Path):
    """Read a text file and return a list of lines **without** trailing newlines."""
    return path.read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_ci_logs_directory_exists():
    assert CI_DIR.is_dir(), (
        f"Directory {CI_DIR} is missing.\n"
        "The initial data should be seeded in this directory."
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_LOGS.items())
def test_raw_log_file_presence_and_content(filename, expected_lines):
    file_path = CI_DIR / filename
    assert file_path.is_file(), (
        f"Expected log file {file_path} is missing.\n"
        "Ensure the initial dataset is correctly provisioned."
    )

    actual_lines = read_file_lines(file_path)
    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected specification.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n"
        f"Found ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
        + "\n"
    )


def test_trimmed_logs_directory_absent_initially():
    trimmed_dir = CI_DIR / "trimmed_logs"
    assert not trimmed_dir.exists(), (
        f"Directory {trimmed_dir} should NOT exist before the student "
        "runs their log-trimming commands."
    )


def test_error_summary_file_absent_initially():
    summary_file = CI_DIR / "error_summary.tsv"
    assert not summary_file.exists(), (
        f"File {summary_file} should NOT exist before the student "
        "generates the summary."
    )