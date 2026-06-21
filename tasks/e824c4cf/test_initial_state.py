# test_initial_state.py
#
# This test-suite verifies that the operating system is still in its
# pristine, pre-exercise state.  None of the artefacts that the student
# is asked to create should exist yet, and the related environment
# variables must be unset.  If any of these tests fail it means the
# initial environment is already “contaminated”, which would make it
# impossible to assess the student’s work reliably.

import os
import pathlib
import pytest


DEPLOYMENT_DIR = pathlib.Path("/home/user/deployment")
ENV_FILE = DEPLOYMENT_DIR / ".env"
SCRIPT_FILE = DEPLOYMENT_DIR / "load_env.sh"
LOG_FILE = DEPLOYMENT_DIR / "env_validation.log"
REQUIRED_VARS = ("AWS_REGION", "DB_HOST", "APP_MODE")


def _exists(p: pathlib.Path) -> bool:
    """Return True if the path exists (file, dir, symlink, etc.)."""
    return p.exists() or p.is_symlink()


def test_deployment_directory_absent():
    assert not _exists(DEPLOYMENT_DIR), (
        f"The directory {DEPLOYMENT_DIR} already exists. "
        "The exercise assumes the student starts from a clean slate, "
        "so this directory must NOT be present."
    )


@pytest.mark.parametrize("path_obj", [ENV_FILE, SCRIPT_FILE, LOG_FILE])
def test_no_target_files_exist(path_obj):
    assert not _exists(path_obj), (
        f"The path {path_obj} is present but should NOT exist before the "
        "student begins the task.  Remove it to restore the pristine state."
    )


@pytest.mark.parametrize("var_name", REQUIRED_VARS)
def test_related_environment_variables_unset(var_name):
    assert var_name not in os.environ, (
        f"The environment variable {var_name!r} is already defined.  "
        "It must be unset at the start of the exercise so the "
        "student can validate their script correctly."
    )