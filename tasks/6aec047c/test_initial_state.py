# test_initial_state.py
#
# This pytest file validates that the workspace is completely clean
# before the student starts working on the “loop-back connectivity”
# automation project.  Nothing related to the project should exist
# yet under /home/user/netdiag.

import os
import pytest
from pathlib import Path

# Absolute paths that must NOT exist at the beginning of the exercise.
NETDIAG_DIR = Path("/home/user/netdiag")
MAKEFILE_PATH = NETDIAG_DIR / "Makefile"
LOG_DIR = NETDIAG_DIR / "logs"
LOG_FILE = LOG_DIR / "loopback.log"


@pytest.mark.parametrize(
    "path_obj, kind",
    [
        (NETDIAG_DIR, "directory"),
        (MAKEFILE_PATH, "file"),
        (LOG_DIR, "directory"),
        (LOG_FILE, "file"),
    ],
)
def test_project_artifacts_do_not_exist_yet(path_obj: Path, kind: str):
    """
    Ensure no part of the /home/user/netdiag project hierarchy exists
    before the student starts the task.  A pre-existing artefact would
    mean the environment is not clean and would invalidate the exercise.
    """
    assert not path_obj.exists(), (
        f"Initial-state validation failed: The {kind} {path_obj} "
        "should NOT exist before the task is attempted.  "
        "Please remove it so the student starts from a clean slate."
    )