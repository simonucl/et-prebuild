# test_initial_state.py
#
# This pytest suite verifies that the machine starts from a **clean** state
# before the student performs any work on the incident-diagnostics exercise.
#
# In particular, we confirm that neither the required virtual-environment
# directory nor the expected log file already exist.  If any of these items
# are present beforehand, the automated grader could give misleading results
# or mask an incorrect implementation by the student.
#
# NOTE: These checks purposefully ensure **absence** of artefacts; they do
# not validate their correctness (that will be done by a separate test
# suite after the student’s script runs).

import os
import stat
import pytest

HOME = "/home/user"
VENV_DIR = os.path.join(HOME, ".ops", "venvs", "incident2024")
PYTHON_BIN = os.path.join(VENV_DIR, "bin", "python")
LOG_FILE = os.path.join(HOME, "incident2024_setup.log")


@pytest.mark.describe("Initial filesystem state must be clean")
class TestInitialState:
    def test_virtualenv_directory_does_not_exist(self):
        """
        The virtual-environment directory should NOT exist at the start.
        """
        assert not os.path.exists(VENV_DIR), (
            f"Unexpected directory present: {VENV_DIR!r}. "
            "The environment must be created by the student’s solution, "
            "but it is already on disk."
        )

    def test_python_executable_does_not_exist(self):
        """
        The interpreter inside the yet-to-be-created venv must not exist.
        """
        assert not os.path.exists(PYTHON_BIN), (
            f"Unexpected file present: {PYTHON_BIN!r}. "
            "The student must create this virtual environment from scratch."
        )

    def test_log_file_does_not_exist(self):
        """
        The setup log file must not pre-exist; it will be generated
        by the student’s script.
        """
        assert not os.path.exists(LOG_FILE), (
            f"Unexpected file present: {LOG_FILE!r}. "
            "The log should be produced by the student’s solution, "
            "but it already exists."
        )