# test_initial_state.py
#
# This pytest suite verifies that the filesystem is in a clean state
# BEFORE the student starts working.  Nothing related to the task
# (directory /home/user/iot_deployment or the files inside it) should
# exist yet.  If any of these artefacts are already present, the tests
# will fail with a clear explanation so the learner can clean up and
# start from a known baseline.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
IOT_DIR = HOME / "iot_deployment"
FILES = [
    IOT_DIR / "deploy.sh",
    IOT_DIR / "config.json",
    IOT_DIR / "permission_audit.log",
]


def test_home_directory_exists():
    """
    Basic sanity-check that the home directory itself exists;
    the assignment depends on this path.
    """
    assert HOME.is_dir(), f"Expected home directory {HOME} to exist."


def test_iot_deployment_directory_absent():
    """
    The iot_deployment directory must NOT exist before the student
    runs any commands.  Starting with a clean slate prevents accidental
    reuse of stale artefacts from previous attempts.
    """
    assert not IOT_DIR.exists(), (
        f"Directory {IOT_DIR} already exists. "
        "Please remove it before starting the task to ensure a clean state."
    )


@pytest.mark.parametrize("filepath", FILES)
def test_task_files_absent(filepath: Path):
    """
    None of the task files should be present at this stage.
    """
    assert not filepath.exists(), (
        f"Found unexpected file at {filepath}. "
        "Make sure to start the assignment without pre-existing artefacts."
    )