# test_initial_state.py
#
# This pytest suite validates that the workspace is in the correct
# initial state *before* the student script is executed.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
BUILD_LOGS_DIR = HOME / "build_logs"

# ---------------------------------------------------------------------------
# 1. Generic directory-level checks
# ---------------------------------------------------------------------------

def test_build_logs_directory_exists():
    """
    The directory /home/user/build_logs must exist and be a directory.
    """
    assert BUILD_LOGS_DIR.exists(), f"Directory {BUILD_LOGS_DIR} is missing."
    assert BUILD_LOGS_DIR.is_dir(), f"{BUILD_LOGS_DIR} exists but is not a directory."


# ---------------------------------------------------------------------------
# 2. Expected / unexpected files
# ---------------------------------------------------------------------------

EXPECTED_LOG_FILES = {
    "branch_main.log",
    "branch_release.log",
    "branch_featureA.log",
}

@pytest.mark.parametrize("filename", sorted(EXPECTED_LOG_FILES))
def test_expected_log_file_present(filename):
    """
    Each expected branch_*.log file must be present.
    """
    path = BUILD_LOGS_DIR / filename
    assert path.exists(), f"Expected log file {path} is missing."
    assert path.is_file(), f"Expected log file {path} exists but is not a regular file."


def test_no_extra_branch_logs():
    """
    No unexpected files that match the pattern branch_*.log should be present.
    """
    pattern_files = {p.name for p in BUILD_LOGS_DIR.glob("branch_*.log")}
    extra_files = pattern_files - EXPECTED_LOG_FILES
    missing_files = EXPECTED_LOG_FILES - pattern_files

    assert not missing_files, (
        "The following expected files are missing: "
        f"{', '.join(sorted(missing_files))}"
    )
    assert not extra_files, (
        "Found unexpected branch log files in build_logs directory: "
        f"{', '.join(sorted(extra_files))}"
    )


def test_error_summary_csv_absent():
    """
    error_summary.csv must *not* exist yet.
    """
    summary_path = BUILD_LOGS_DIR / "error_summary.csv"
    assert not summary_path.exists(), (
        f"{summary_path} should not exist before the student's script runs."
    )

# ---------------------------------------------------------------------------
# 3. Exact content verification for each log file
# ---------------------------------------------------------------------------

EXPECTED_CONTENTS = {
    "branch_main.log": [
        "BuildStart: 2023-08-15 14:23:11",
        "[INFO] Checking dependencies",
        "[ERROR:] Missing library xyz",
        "[INFO] Build aborted",
    ],
    "branch_release.log": [
        "BuildStart: 2023-08-16 09:04:51",
        "[INFO] Preparing build",
        "[INFO] Compiling...",
        "[FAILURE:] Unit tests failed",
        "[ERROR:] Code signing failed",
        "[INFO] Build failed",
    ],
    "branch_featureA.log": [
        "BuildStart: 2023-08-17 11:39:05",
        "[INFO] Setup...",
        "[INFO] Build succeeded",
        "[INFO] Cleaning up",
    ],
}

@pytest.mark.parametrize("filename, expected_lines",
    [(fn, EXPECTED_CONTENTS[fn]) for fn in sorted(EXPECTED_CONTENTS)]
)
def test_log_file_contents(filename, expected_lines):
    """
    Each log file must contain the exact expected lines (in order, with LF newlines).
    """
    path = BUILD_LOGS_DIR / filename
    assert path.exists(), f"Cannot read {path}; file is missing."

    with path.open("r", encoding="utf-8") as fp:
        actual_lines = [line.rstrip("\n") for line in fp.readlines()]

    assert actual_lines == expected_lines, (
        f"Content mismatch in {path}.\n"
        f"Expected:\n{expected_lines!r}\n\nGot:\n{actual_lines!r}"
    )