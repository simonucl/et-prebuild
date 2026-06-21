# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student carries out the three-step deployment task.
#
# These tests purposefully check that NOTHING related to the task
# is yet present.  They will fail if any of the required artefacts
# already exist, thereby guaranteeing that the environment starts in
# a clean slate.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
DEPLOY_DIR = HOME / "deployment"
CONF_FILE = DEPLOY_DIR / "service_release.conf"
LOG_FILE = DEPLOY_DIR / "release_manifest.log"


def _pretty(path: Path) -> str:
    """Return a nicely formatted absolute path for messages."""
    return str(path.resolve())


def test_deployment_directory_absent():
    """
    The /home/user/deployment directory must NOT exist before the
    student runs their commands.
    """
    assert not DEPLOY_DIR.exists(), (
        f"Initial state invalid: directory {_pretty(DEPLOY_DIR)} already exists. "
        "The deployment directory should be created by the student, "
        "not be present beforehand."
    )


@pytest.mark.parametrize(
    "artifact",
    [
        CONF_FILE,
        LOG_FILE,
    ],
)
def test_deployment_files_absent(artifact: Path):
    """
    Neither service_release.conf nor release_manifest.log should exist
    before the student performs the task.
    """
    assert not artifact.exists(), (
        f"Initial state invalid: file {_pretty(artifact)} already exists. "
        "All deployment artefacts must be created by the student."
    )