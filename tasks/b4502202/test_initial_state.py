# test_initial_state.py
#
# These tests assert the expected *initial* state of the filesystem
# before the student runs any command.  They deliberately confirm that
# the virtual-environment directory and the status file do **not** yet
# exist, while ensuring the expected base directories are in place.
#
# If any test here fails it means the checker’s starting environment
# is wrong or the student has already performed actions that should
# happen only **after** the forthcoming command.

import os
from pathlib import Path

HOME = Path("/home/user")
DOCS_DIR = HOME / "docs"
VENV_DIR = DOCS_DIR / "venv"
STATUS_FILE = HOME / "docs" / "venv_status.log"


def test_home_directory_exists():
    """Ensure the base home directory is present."""
    assert HOME.is_dir(), f"Expected home directory {HOME} to exist."


def test_docs_directory_exists():
    """
    The exercise states that all project-related material is kept under
    /home/user/docs, so the directory should pre-exist.
    """
    assert DOCS_DIR.is_dir(), (
        f"Directory {DOCS_DIR} is missing.\n"
        "Create it before setting up the virtual environment."
    )


def test_venv_directory_absent():
    """
    The virtual-environment directory must NOT exist before the student runs
    the required shell command.  Its presence would indicate the task has
    already been performed or the starting state is polluted.
    """
    assert not VENV_DIR.exists(), (
        f"Found unexpected directory {VENV_DIR}.\n"
        "The virtual environment should be created by the student's command, "
        "so it must not be present at the beginning."
    )


def test_status_file_absent():
    """
    The status file must NOT exist yet.  It should be created *after*
    the virtual environment is set up.
    """
    assert not STATUS_FILE.exists(), (
        f"Found unexpected file {STATUS_FILE}.\n"
        "The status file should be generated only after the virtual "
        "environment is created."
    )