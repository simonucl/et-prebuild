# test_initial_state.py
"""
Pytest suite to assert that the machine is in a clean state
 BEFORE the student starts working on the “api-test” task.

The checks deliberately confirm the *absence* of every file /
 directory / venv that the student will later be asked to create.
If any of these artefacts already exist, the test suite fails with
a clear error message so the grader knows the environment is
contaminated.
"""

from pathlib import Path

# Base paths
HOME_DIR = Path("/home/user")
PROJECT_DIR = HOME_DIR / "api-test"
VENV_DIR = PROJECT_DIR / "env"
ACTIVATE_SCRIPT = VENV_DIR / "bin" / "activate"
PYTHON_BIN = VENV_DIR / "bin" / "python"
REQUIREMENTS_FILE = PROJECT_DIR / "requirements.txt"
INSTALL_LOG = PROJECT_DIR / "install.log"


def _assert_not_exists(path: Path):
    """
    Helper that fails with a readable error if the given path exists.
    """
    assert not path.exists(), (
        f"Initial-state error: {path} already exists, but it should be "
        f"ABSENT before the student starts the task."
    )


def test_project_directory_absent():
    """
    The directory /home/user/api-test must NOT exist yet.
    """
    _assert_not_exists(PROJECT_DIR)


def test_virtualenv_absent():
    """
    The virtual-environment directory and its key executables
    must NOT exist before the task begins.
    """
    _assert_not_exists(VENV_DIR)
    _assert_not_exists(ACTIVATE_SCRIPT)
    _assert_not_exists(PYTHON_BIN)


def test_requirements_file_absent():
    """
    requirements.txt should not be present in the initial state.
    """
    _assert_not_exists(REQUIREMENTS_FILE)


def test_install_log_absent():
    """
    install.log should not be present in the initial state.
    """
    _assert_not_exists(INSTALL_LOG)