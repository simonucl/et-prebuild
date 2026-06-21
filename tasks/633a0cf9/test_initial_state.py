# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state before the student starts the exercise.

The tests intentionally confirm that none of the artefacts that the
student is asked to create already exist.  If any of them are found, the
suite fails with a clear, actionable message.

Only modules from the Python standard library are used.
"""

import os
import stat
import pytest

HOME = "/home/user"
DEPLOY_ROOT = os.path.join(HOME, "deployments")

DIRS_EXPECTED_LATER = [
    DEPLOY_ROOT,
    os.path.join(DEPLOY_ROOT, "releases"),
    os.path.join(DEPLOY_ROOT, "logs"),
]

FILES_EXPECTED_LATER = [
    os.path.join(DEPLOY_ROOT, "RELEASE_GROUP"),
    os.path.join(DEPLOY_ROOT, "RELEASE_USERS"),
    os.path.join(DEPLOY_ROOT, "deployment_audit.log"),
]


@pytest.mark.parametrize("path", DIRS_EXPECTED_LATER)
def test_directories_do_not_yet_exist(path):
    """
    No directory that the learner is supposed to create should be present
    beforehand.  If any are found, fail early so the learner starts from a
    clean slate.
    """
    assert not os.path.exists(
        path
    ), (
        f"The directory {path!r} already exists. "
        "The workspace must start clean so the learner can create it."
    )


@pytest.mark.parametrize("path", FILES_EXPECTED_LATER)
def test_files_do_not_yet_exist(path):
    """
    No file that the learner is supposed to create should be present
    beforehand.  This prevents false positives in the grader later on.
    """
    assert not os.path.exists(
        path
    ), (
        f"The file {path!r} already exists. "
        "The learner must be able to create it from scratch."
    )