# test_initial_state.py
#
# This test-suite verifies that the filesystem is in a **clean initial state**
# before the student carries out any of the required actions.
#
# EXPECTED INITIAL CONDITIONS
#   • None of the target files or directories for the task must exist yet.
#   • If they do already exist (from a previous run, for example) the learner
#     needs to remove or rename them before proceeding so that the exercise
#     starts from a predictable baseline.
#
# The tests below will fail with a clear, actionable message if any artefact
# that the forthcoming instructions are meant to create is already present.

import os
from pathlib import Path

import pytest


# Absolute paths that must NOT exist before the student runs the task
ABSENT_PATHS = [
    Path("/home/user/.ssh/staging_id_rsa"),
    Path("/home/user/.ssh/staging_id_rsa.pub"),
    Path("/home/user/deployment/authorized_keys_staging"),
    Path("/home/user/deployment/staging_key_fingerprint.log"),
]


@pytest.mark.parametrize("path", ABSENT_PATHS, ids=[str(p) for p in ABSENT_PATHS])
def test_path_does_not_exist(path: Path):
    """
    Assert that each artefact the learner is supposed to create does NOT exist
    yet.  This guarantees a predictable, clean starting point.
    """
    assert not path.exists(), (
        f"The path {path} already exists. "
        "Please remove or rename it before starting the task so that you "
        "can create it from scratch as instructed."
    )