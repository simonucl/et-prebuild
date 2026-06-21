# test_initial_state.py
#
# This pytest file verifies that the operating-system / filesystem is in the
# expected *clean* state **before** the student starts working on the task.
#
# Nothing that the student is supposed to create should exist yet:
#   • /home/user/perf_env/ (the virtual-environment directory)
#   • /home/user/project/requirements.txt
#   • /home/user/package_audit.log
#
# If any of these are already present, the test suite will fail with a clear
# explanation so the learner knows the environment is not pristine.

from pathlib import Path
import os
import pytest

HOME = Path("/home/user")
VENV_DIR = HOME / "perf_env"
REQUIREMENTS_TXT = HOME / "project" / "requirements.txt"
AUDIT_LOG = HOME / "package_audit.log"


def _assert_absent(path: Path):
    """
    Helper that asserts a path does NOT exist.  Produces a descriptive failure
    message if the file or directory is unexpectedly present.
    """
    assert not path.exists(), (
        f"\n'{path}' already exists but it should NOT be present at the start "
        f"of the exercise.\nPlease remove it and ensure you perform all steps "
        f"from scratch."
    )


def test_virtual_env_absent():
    """
    The virtual-environment directory /home/user/perf_env must NOT exist yet.
    """
    _assert_absent(VENV_DIR)
    # Additionally ensure typical venv sub-files are not present (defensive).
    _assert_absent(VENV_DIR / "bin" / "activate")
    _assert_absent(VENV_DIR / "bin" / "python")


@pytest.mark.parametrize("path", [REQUIREMENTS_TXT, AUDIT_LOG])
def test_task_files_absent(path: Path):
    """
    Neither requirements.txt nor package_audit.log should exist at this point.
    """
    _assert_absent(path)


def test_not_inside_any_virtualenv():
    """
    The shell that runs the tests should not already be inside *any* Python
    virtual environment (the VIRTUAL_ENV env-var should be unset).
    """
    assert "VIRTUAL_ENV" not in os.environ, (
        "Your shell is already inside a virtual environment "
        f"({os.environ.get('VIRTUAL_ENV')}).\n"
        "Deactivate it before starting the exercise so that the grader can "
        "see you create the correct venv from scratch."
    )