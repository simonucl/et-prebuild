# test_initial_state.py
"""
Pytest suite to verify that the system is in a clean state *before*
the student starts working on the “reproducible Python build artifact” task.

The suite ENSURES that none of the required deliverables (virtual‐environment,
artifacts directory, nor artifact files) already exist.

If any of these pre-existing items are found, the test suite fails with a
helpful message so the student can clean up the workspace before proceeding.

Only the Python stdlib and pytest are used, per specification.
"""

import os
from pathlib import Path

HOME = Path("/home/user")

# Paths that must NOT exist yet
BUILD_ENV_DIR      = HOME / "build_env"
ACTIVATE_SCRIPT    = BUILD_ENV_DIR / "bin" / "activate"
ARTIFACTS_DIR      = HOME / "artifacts"
REQUIREMENTS_FILE  = ARTIFACTS_DIR / "requirements.txt"
SUMMARY_LOG_FILE   = ARTIFACTS_DIR / "build_summary.log"


def _assert_absent(path: Path):
    """
    Helper that asserts a path does NOT exist on the filesystem.
    Produces a clear failure message if the path is unexpectedly present.
    """
    assert not path.exists(), (
        f"Precondition failure: {path} already exists but it must NOT exist "
        "before the student begins the task. "
        "Please remove or rename it and start with a clean workspace."
    )


def test_build_env_directory_absent():
    """/home/user/build_env must NOT exist yet."""
    _assert_absent(BUILD_ENV_DIR)


def test_activate_script_absent():
    """/home/user/build_env/bin/activate must NOT exist yet."""
    _assert_absent(ACTIVATE_SCRIPT)


def test_artifacts_directory_absent():
    """/home/user/artifacts must NOT exist yet."""
    _assert_absent(ARTIFACTS_DIR)


def test_requirements_file_absent():
    """/home/user/artifacts/requirements.txt must NOT exist yet."""
    _assert_absent(REQUIREMENTS_FILE)


def test_summary_log_file_absent():
    """/home/user/artifacts/build_summary.log must NOT exist yet."""
    _assert_absent(SUMMARY_LOG_FILE)