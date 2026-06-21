# test_initial_state.py
#
# This pytest suite validates that the filesystem and process
# state are “clean” **before** the learner begins the exercise.
# Nothing that the assignment asks the learner to create should
# exist yet, and none of the target environment variables should
# be set.  If any of these assertions fail, the learning
# environment is in an unexpected state and must be reset **before**
# the learner starts working.

import os
import pytest
from pathlib import Path

# Absolute base path for the workspace that the student will create.
BASE_DIR = Path("/home/user/devsecops_policy_demo")

# All files / directories that must NOT exist at the outset.
EXPECTED_ABSENT_PATHS = [
    BASE_DIR,                                 # the workspace directory
    BASE_DIR / ".env.template",
    BASE_DIR / ".env.secure",
    BASE_DIR / "load_env.sh",
    BASE_DIR / ".gitignore",
    BASE_DIR / "env_after_source.log",
    BASE_DIR / "logs",                        # logs directory
    BASE_DIR / "logs" / "execution.log",
]

# Environment variables that should not yet be exported.
ENV_VARS_TO_CHECK = [
    "DB_USER",
    "DB_PASSWORD",
    "API_TOKEN",
    "LOG_LEVEL",
]


@pytest.mark.parametrize("path_obj", EXPECTED_ABSENT_PATHS)
def test_paths_do_not_exist(path_obj):
    """
    Ensure that none of the directories/files the student is
    supposed to create are already present.  A pre-existing file
    would give the learner an unfair starting point or cause the
    exercise to behave unpredictably.
    """
    assert not path_obj.exists(), (
        f"Unexpected artefact found before the exercise started: {path_obj}\n"
        "The workspace must be completely clean so the learner can "
        "create it from scratch.  Delete the path and reset the state."
    )


@pytest.mark.parametrize("var_name", ENV_VARS_TO_CHECK)
def test_env_vars_not_exported(var_name):
    """
    Confirm that none of the required environment variables are
    already present in the current shell.  They are supposed to be
    populated only after the student sources the load_env.sh script.
    """
    assert var_name not in os.environ, (
        f"Environment variable {var_name} is unexpectedly set to "
        f"'{os.environ.get(var_name)}' before the exercise begins.\n"
        "Unset it so the learner starts from a blank slate."
    )