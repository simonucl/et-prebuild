# test_initial_state.py
#
# Pytest suite that confirms the *initial* filesystem / OS state
# before the student performs any action for the “artifact–manager”
# exercise.  The assertions here encode the truth‐value handed down
# by the grader and MUST hold when the testing session starts.
#
# Only standard-library modules + pytest are used.

import os
import subprocess
import sys
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Static references                                                           #
# --------------------------------------------------------------------------- #
HOME = Path("/home/user")
REPO_DIR = HOME / "binary-repo"
TOOLS_DIR = HOME / "artifact-tools"
CLEANUP_SCRIPT = TOOLS_DIR / "cleanup_repo.sh"
LOG_FILE = TOOLS_DIR / "cleanup_repo.log"

INCOMPLETE_FILES = {
    "beta-2.2.3.tmp",
    "gamma-0.9.1.partial",
}
NORMAL_FILES = {
    "alpha-1.0.0.jar",
    "alpha-1.0.1.jar",
    "readme.txt",
}
ALL_EXPECTED_FILES = INCOMPLETE_FILES | NORMAL_FILES


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _current_user_crontab() -> str:
    """
    Return the current user's crontab (may be empty string).

    If the user has no crontab, `crontab -l` exits with non-zero status;
    in that case we treat the content as an empty string.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout
    # The typical message is “no crontab for <user>”, but that
    # implementation detail should not cause the test to fail.
    return ""


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_repository_directory_exists_and_is_directory():
    assert REPO_DIR.exists(), f"Expected directory {REPO_DIR} is missing."
    assert REPO_DIR.is_dir(), f"{REPO_DIR} exists but is not a directory."


def test_repository_contains_exact_expected_files():
    repo_files = {p.name for p in REPO_DIR.iterdir() if p.is_file()}
    missing = ALL_EXPECTED_FILES - repo_files
    assert not missing, (
        "The repository is missing the following expected file(s): "
        f"{', '.join(sorted(missing))}"
    )


def test_incomplete_files_present():
    """
    Ensure the pre-existing incomplete uploads (.tmp / .partial) are present.
    """
    for fname in INCOMPLETE_FILES:
        path = REPO_DIR / fname
        assert path.exists(), f"Expected incomplete file {path} is missing."
        assert path.is_file(), f"Expected file {path} is not a regular file."


def test_artifact_tools_directory_absent():
    assert not TOOLS_DIR.exists(), (
        f"Directory {TOOLS_DIR} should NOT exist before the student runs their "
        "solution."
    )


def test_cleanup_script_absent():
    assert not CLEANUP_SCRIPT.exists(), (
        f"File {CLEANUP_SCRIPT} should NOT exist prior to the student's work."
    )


def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should not pre-exist; the student's script must "
        "create it."
    )


def test_crontab_does_not_contain_cleanup_job():
    CRON_LINE = (
        "45 4 * * * /home/user/artifact-tools/cleanup_repo.sh >> "
        "/home/user/artifact-tools/cleanup_repo.log 2>&1"
    )
    crontab_contents = _current_user_crontab()
    assert CRON_LINE not in crontab_contents, (
        "The user crontab already contains the clean-up job, but it must NOT "
        "be present before the student configures it."
    )