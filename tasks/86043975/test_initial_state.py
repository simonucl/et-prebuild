# test_initial_state.py
#
# This pytest suite validates the *initial* condition of the system
# before the student runs any command.  It checks that:
#
# 1. The project directory `/home/user/web_project` already exists.
# 2. No virtual-environment related artefacts are present yet.
# 3. No confirmation file `.venv_created` exists.
# 4. A usable `python3` interpreter is discoverable in $PATH.
#
# If any of these assertions fail, the filesystem is in an unexpected
# state and the student’s one-liner cannot be reliably graded.

import os
import shutil
import subprocess
import sys

PROJECT_DIR = "/home/user/web_project"
VENV_DIR = os.path.join(PROJECT_DIR, "venv")
PYVENV_CFG = os.path.join(VENV_DIR, "pyvenv.cfg")
ACTIVATE_SH = os.path.join(VENV_DIR, "bin", "activate")
CONFIRMATION_FILE = os.path.join(PROJECT_DIR, ".venv_created")


def test_project_directory_exists():
    """The cloned repository directory must already be present."""
    assert os.path.isdir(
        PROJECT_DIR
    ), f"Expected project directory {PROJECT_DIR!r} to exist."


def test_no_virtualenv_directory_yet():
    """
    The venv directory must *not* exist before the student runs their
    command.  Its presence would indicate that the virtual environment
    has already been created, invalidating the exercise.
    """
    assert not os.path.exists(
        VENV_DIR
    ), f"The virtual-environment directory {VENV_DIR!r} should NOT exist yet."


def test_no_virtualenv_files_yet():
    """Neither pyvenv.cfg nor activation script should be present yet."""
    for path in (PYVENV_CFG, ACTIVATE_SH):
        assert not os.path.exists(
            path
        ), f"Virtual-environment artefact {path!r} found but should not exist yet."


def test_no_confirmation_file_yet():
    """The '.venv_created' marker file must not exist at the start."""
    assert not os.path.exists(
        CONFIRMATION_FILE
    ), f"Confirmation file {CONFIRMATION_FILE!r} should not be present yet."


def test_python3_is_available():
    """Ensure that a Python 3 interpreter is discoverable in $PATH."""
    python_path = shutil.which("python3")
    assert (
        python_path
        and os.path.isfile(python_path)
        and os.access(python_path, os.X_OK)
    ), "python3 interpreter not found in $PATH; it is required for `python3 -m venv` to succeed."