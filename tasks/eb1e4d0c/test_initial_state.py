# test_initial_state.py
"""
Pytest suite to verify that the operating-system state is *clean* before the
student creates the requested virtual-environment and log file.

The assignment later demands the following artefacts:

1. Directory  /home/user/mobile-pipeline-env/
   └── bin/
       ├── activate
       └── python  (executable)

2. File       /home/user/mobile-pipeline-env-setup.log
   (exactly three non-empty lines, newline-terminated after each line)

Because this test suite is executed **before** the student’s work, it must
confirm that none of the artefacts are present yet.  If any of them already
exist, the initial state is invalid and the student will not get a fair test.
"""

import os
from pathlib import Path

ENV_DIR = Path("/home/user/mobile-pipeline-env")
BIN_DIR = ENV_DIR / "bin"
ACTIVATE_FILE = BIN_DIR / "activate"
PYTHON_FILE = BIN_DIR / "python"
LOG_FILE = Path("/home/user/mobile-pipeline-env-setup.log")


def _raise_if_path_exists(path: Path, what: str):
    assert not path.exists(), (
        f"Initial-state check failed: '{path}' already exists, but it should "
        f"NOT be present before the student starts. "
        f"Please remove the pre-existing {what} so the assignment begins with "
        f"a clean slate."
    )


def test_virtual_environment_directory_absent():
    """The virtual-environment directory must not exist yet."""
    _raise_if_path_exists(ENV_DIR, "directory")


def test_bin_subdirectory_absent():
    """The 'bin' subdirectory inside the virtual environment must not exist."""
    _raise_if_path_exists(BIN_DIR, "directory")


def test_activate_script_absent():
    """The activate script must not exist before the student creates the venv."""
    _raise_if_path_exists(ACTIVATE_FILE, "file")


def test_python_executable_absent():
    """The python executable must not exist before the student creates the venv."""
    _raise_if_path_exists(PYTHON_FILE, "file")


def test_setup_log_absent():
    """The setup log file must not be present at the start."""
    _raise_if_path_exists(LOG_FILE, "file")