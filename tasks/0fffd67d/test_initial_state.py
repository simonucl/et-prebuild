# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the operating system
# before the learner begins the “data-preparation virtual-environment” task.
#
# These tests must pass **before** any work is performed.  They purposely
# check that the artefacts which the learner is about to create are
# currently absent, guaranteeing a clean, predictable starting point.

import pathlib

# Fixed, absolute locations used throughout the exercise
PROJECT_DIR = pathlib.Path("/home/user/projects/data_prep")
VENV_DIR    = PROJECT_DIR / "ml_env"
LOG_FILE    = PROJECT_DIR / "env_packages.log"


def test_virtual_environment_absent():
    """
    The virtual-environment directory must not pre-exist.
    A pre-existing directory could contain unexpected state that
    invalidates the exercise.
    """
    assert not VENV_DIR.exists(), (
        f"Pre-check failed: the directory '{VENV_DIR}' already exists. "
        "Start with a clean slate—remove it before beginning the task."
    )


def test_log_file_absent():
    """
    The package-freeze log must not pre-exist.
    Its presence would indicate that the task has already been started
    or completed, defeating the purpose of this initial-state check.
    """
    assert not LOG_FILE.exists(), (
        f"Pre-check failed: the log file '{LOG_FILE}' already exists. "
        "Remove or rename it before beginning the task."
    )