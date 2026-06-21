# test_initial_state.py
#
# This pytest module verifies **the pristine, pre-exercise state**
# of the filesystem for the “QA environment” task.  NOTHING that the
# student is asked to create should exist yet.  If any of the checked
# paths are found, the tests will fail with a clear, actionable message.
#
# Only Python’s standard library and pytest are used, per instructions.

import os
import stat
import subprocess
import sys

import pytest

HOME = "/home/user"
QA_ROOT = os.path.join(HOME, "qa_env")

# Every path that *must not* exist before the student starts working.
ABSENT_DIRS = [
    QA_ROOT,
    os.path.join(QA_ROOT, "configs"),
    os.path.join(QA_ROOT, "logs"),
    os.path.join(QA_ROOT, "venv"),
]

ABSENT_FILES = [
    os.path.join(QA_ROOT, "configs", "app_config.ini"),
    os.path.join(QA_ROOT, "env.sh"),
    os.path.join(QA_ROOT, "requirements.txt"),
    os.path.join(QA_ROOT, "logs", "setup_audit.log"),
    os.path.join(QA_ROOT, ".setup_complete"),
]


@pytest.mark.parametrize("path", ABSENT_DIRS + ABSENT_FILES)
def test_paths_do_not_yet_exist(path):
    """
    Verifies that none of the directories / files that the student
    will be asked to create are present beforehand.
    """
    assert not os.path.exists(
        path
    ), f"Path unexpectedly exists before setup: {path!r}. Start from a clean slate."


def test_virtualenv_not_present():
    """
    Extra sanity-check: if a directory happens to be named qa_env/venv,
    confirm it is *not* a functional virtual-environment yet.
    """
    venv_python = os.path.join(QA_ROOT, "venv", "bin", "python")
    if os.path.exists(venv_python):
        # The venv directory is there; that is already a failure.
        pytest.fail(
            f"Virtual-environment already present at {venv_python!r}. "
            "The student must create it themselves."
        )


def test_no_leaked_environment_variables(monkeypatch):
    """
    The setup script env.sh will eventually export QA_ENV_ROOT.
    Make sure it is *not* already defined in the current process
    environment.
    """
    assert "QA_ENV_ROOT" not in os.environ, (
        "Environment variable QA_ENV_ROOT is already set; "
        "the environment should be pristine before the exercise starts."
    )