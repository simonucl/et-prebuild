# test_initial_state.py
#
# This pytest suite verifies that the workspace is still in its **initial**
# (pristine) state before the student starts solving the exercise.
#
# Expected initial state:
#   • /home/user/alert_project/          MUST NOT exist
#   • /home/user/alert_project/venv/     MUST NOT exist
#   • /home/user/alert_project/setup/    MUST NOT exist
#   • /home/user/alert_project/setup/install_log.txt MUST NOT exist
#
# Rationale:
# The student is asked to create all of the above as part of the assignment,
# so they must be absent at the very beginning.  If any of them are already
# present, the grader would be unable to tell whether the student created
# them or they pre-existed, leading to false positives.  These tests make sure
# the filesystem really starts empty with regard to the project.

from pathlib import Path

import pytest


# Base directory that the student will have to create.
PROJECT_ROOT = Path("/home/user/alert_project")


@pytest.mark.parametrize(
    "path, should_exist",
    [
        (PROJECT_ROOT, False),
        (PROJECT_ROOT / "venv", False),
        (PROJECT_ROOT / "setup", False),
        (PROJECT_ROOT / "setup" / "install_log.txt", False),
    ],
    ids=[
        "project root should NOT exist",
        "virtualenv directory should NOT exist",
        "setup directory should NOT exist",
        "install_log.txt should NOT exist",
    ],
)
def test_precondition_paths_do_not_exist(path: Path, should_exist: bool):
    """
    Ensure that none of the artefacts the student is responsible for
    creating are present *before* the exercise starts.
    """
    if should_exist:
        assert path.exists(), (
            f"Precondition failed: Expected {path} to exist, "
            "but it is missing.  The template environment is broken."
        )
    else:
        assert not path.exists(), (
            f"Precondition failed: {path} already exists, "
            "but it must be absent at the start so the student can create it."
        )