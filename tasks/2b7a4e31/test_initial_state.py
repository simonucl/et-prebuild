# test_initial_state.py
#
# Pytest suite that asserts the workspace is clean *before* the student
# performs any action.  Nothing that the assignment asks the student to
# create should exist at this point.

import subprocess
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants for the resources that should **NOT** exist at the outset.
# --------------------------------------------------------------------------- #
VENV_DIR = Path("/home/user/venvs/research_env")
VENV_PYTHON = VENV_DIR / "bin" / "python"
VENV_PIP = VENV_DIR / "bin" / "pip"
CSV_MANIFEST = Path("/home/user/research/installed_packages.csv")


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
def _path_exists(path: Path) -> bool:
    """Return True if the given path exists in the filesystem."""
    return path.exists()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_virtualenv_directory_absent():
    """
    The assignment requires the student to *create* the virtual-environment
    directory.  It must therefore be absent at the start.
    """
    assert not _path_exists(
        VENV_DIR
    ), (
        f"Pre-existing virtual-environment directory found at {VENV_DIR!s}. "
        "The workspace should start clean so the student can create it."
    )


def test_virtualenv_python_absent():
    """
    The `bin/python` executable inside the virtual-environment must not exist
    yet.  Its presence would indicate the env was already created.
    """
    assert not _path_exists(
        VENV_PYTHON
    ), (
        f"Unexpected file {VENV_PYTHON!s} detected. "
        "A fresh workspace must not contain the virtual-env's Python."
    )


def test_virtualenv_pip_absent():
    """
    Similarly, the `bin/pip` executable must not exist before the student
    builds the environment.
    """
    assert not _path_exists(
        VENV_PIP
    ), (
        f"Unexpected file {VENV_PIP!s} detected. "
        "A fresh workspace must not contain the virtual-env's pip."
    )


def test_manifest_csv_absent():
    """
    The CSV manifest file should be produced by the student.  It must not
    exist beforehand.
    """
    assert not _path_exists(
        CSV_MANIFEST
    ), (
        f"Pre-existing manifest file found at {CSV_MANIFEST!s}. "
        "The student must generate this file during the task."
    )