# test_initial_state.py
#
# This test-suite verifies that the *pre-exercise* environment is in place
# for the “Symbolic-link housekeeping for an API integration sandbox”
# challenge.  It purposefully avoids touching (or even referencing) any of
# the objects that the student is expected to create or modify, in compliance
# with the grading‐harness guidelines.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
APIS_DIR = HOME / "apis"
TARGET_VERSION = APIS_DIR / "v1.2.3"


@pytest.fixture(scope="module")
def apis_dir():
    """
    Return the /home/user/apis directory Path object and fail early if it
    does not exist.  Factoring this into a fixture keeps the error message
    clean and avoids cascading failures in subsequent tests.
    """
    if not APIS_DIR.exists():
        pytest.fail(
            f"Required directory {APIS_DIR} is missing. "
            "Create it (and its versioned sub-directories) before proceeding."
        )
    if not APIS_DIR.is_dir():
        pytest.fail(
            f"{APIS_DIR} exists but is *not* a directory. "
            "Remove or rename the conflicting file and create a directory in its place."
        )
    return APIS_DIR


def test_target_version_directory_exists(apis_dir):
    """
    Ensure that the directory the symbolic link must eventually point to—
    /home/user/apis/v1.2.3—already exists and is indeed a directory.
    """
    if not TARGET_VERSION.exists():
        pytest.fail(
            f"Expected version directory {TARGET_VERSION} does not exist. "
            "Create it so the symbolic link can resolve correctly."
        )

    if not TARGET_VERSION.is_dir():
        pytest.fail(
            f"{TARGET_VERSION} exists but is not a directory. "
            "Remove or rename the conflicting item and create a directory with this name."
        )