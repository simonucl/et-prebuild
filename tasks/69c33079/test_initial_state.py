# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student executes the automation task.  All artefacts the
# student is supposed to create (directory, virtual-environment, log file)
# MUST be absent at this point.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")
PROJECT_DIR = HOME / "python_automation"
VENV_DIR = PROJECT_DIR / "venv_automation"
VENV_PYTHON = VENV_DIR / "bin" / "python"
LOG_FILE = PROJECT_DIR / "venv_setup.log"


def _describe_missing(path: Path) -> str:
    """Return a human-readable description for assertion messages."""
    return f"'{path}' should NOT exist yet, but it does."


def _describe_present(path: Path) -> str:
    """Return a human-readable description for assertion messages."""
    return f"Expected '{path}' to exist, but it is missing."


def test_home_directory_exists():
    """Sanity-check: /home/user must exist on the test system."""
    assert HOME.exists(), _describe_present(HOME)
    assert HOME.is_dir(), f"'{HOME}' exists but is not a directory."


@pytest.mark.parametrize(
    "path",
    [
        PROJECT_DIR,
        VENV_DIR,
        VENV_PYTHON,
        LOG_FILE,
    ],
)
def test_project_artifacts_absent(path: Path):
    """
    The project directory, virtual-environment, interpreter, and log file
    must NOT exist before the student performs the task.
    """
    assert not path.exists(), _describe_missing(path)