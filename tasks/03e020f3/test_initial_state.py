# test_initial_state.py
#
# This pytest file validates the **initial** state of the operating system
# *before* the student performs any actions described in the exercise.
#
# The exercise eventually expects the following structure to be created:
#
#   /home/user/policy-as-code-demo/
#       ├── policy.yaml
#       └── compliance.log
#
# Because these resources must be created by the student, they must **not**
# exist at the beginning of the exercise.  These tests therefore assert the
# *absence* of that directory and its expected files.  If any of them already
# exist, the learner is starting from an incorrect state and should move or
# remove the items before proceeding.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME_DIR = "/home/user"
POLICY_DIR = os.path.join(HOME_DIR, "policy-as-code-demo")
POLICY_FILE = os.path.join(POLICY_DIR, "policy.yaml")
LOG_FILE = os.path.join(POLICY_DIR, "compliance.log")


def _exists_and_is_regular_file(path: str) -> bool:
    """
    Helper that returns True only if `path` exists **and** is a regular file.
    """
    try:
        mode = os.stat(path).st_mode
        return stat.S_ISREG(mode)
    except FileNotFoundError:
        return False


def test_home_directory_exists():
    """
    Sanity-check that the canonical /home/user directory exists.
    This is the only item that *should* be present at the start.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected the home directory '{HOME_DIR}' to exist. "
        "The testing environment appears to be mis-configured."
    )


def test_policy_directory_absent():
    """
    The directory that the learner will create **must not** already exist.
    """
    assert not os.path.exists(POLICY_DIR), (
        f"The directory '{POLICY_DIR}' already exists, but it should not be "
        "present at the start of the exercise.  Please remove or rename it "
        "before beginning."
    )


@pytest.mark.parametrize(
    "file_path, description",
    [
        (POLICY_FILE, "policy.yaml"),
        (LOG_FILE, "compliance.log"),
    ],
)
def test_expected_files_absent(file_path: str, description: str):
    """
    None of the target files should exist yet.  If they do, the student no
    longer has a clean slate.
    """
    assert not _exists_and_is_regular_file(file_path), (
        f"The file '{file_path}' ({description}) already exists, but it should "
        "be created by the learner as part of the exercise.  Remove or rename "
        "it before proceeding."
    )