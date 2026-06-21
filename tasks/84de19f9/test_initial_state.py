# test_initial_state.py
#
# This pytest suite verifies that the workspace is **clean** before the
# student starts working.  None of the deployment-specific directories or
# files from the final specification should exist yet.  If any of them are
# already present, the environment is considered contaminated and the tests
# will fail with a clear, actionable message.
#
# Only stdlib + pytest are used, as required.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Canonical paths taken from the task description
# ---------------------------------------------------------------------------

HOME_DIR = Path("/home/user")

WORKSPACE_DIR      = HOME_DIR / "iot_deployment"
STAGING_DIR        = WORKSPACE_DIR / "staging"
PACKAGE_PLAN_CSV   = STAGING_DIR / "package_plan.csv"
INSTALL_LOG        = WORKSPACE_DIR / "install.log"
INSTALL_SORTED_LOG = WORKSPACE_DIR / "install_sorted.log"
SUMMARY_FILE       = WORKSPACE_DIR / "verification_summary.txt"

# All paths that **must not** be present yet.
PATHS_THAT_MUST_NOT_EXIST = [
    WORKSPACE_DIR,
    STAGING_DIR,
    PACKAGE_PLAN_CSV,
    INSTALL_LOG,
    INSTALL_SORTED_LOG,
    SUMMARY_FILE,
]

# ---------------------------------------------------------------------------
# Helper fixtures / functions
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def home_dir_exists():
    """
    Sanity check: /home/user must exist on the execution environment.
    """
    assert HOME_DIR.exists(), (
        f"Expected home directory {HOME_DIR} to exist, "
        "but it does not.  The execution environment is broken."
    )
    assert HOME_DIR.is_dir(), (
        f"{HOME_DIR} exists but is not a directory.  "
        "Please fix the test runner environment."
    )
    return True


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path_obj", PATHS_THAT_MUST_NOT_EXIST)
def test_workspace_is_clean(path_obj: Path, home_dir_exists):
    """
    Ensure that none of the workspace directories or files already exist.
    A clean start is required so the student's script can create everything
    deterministically.
    """
    assert not path_obj.exists(), (
        f"The path {path_obj} already exists, but the initial state is "
        "supposed to be clean.  Please remove it before running the "
        "student's solution."
    )