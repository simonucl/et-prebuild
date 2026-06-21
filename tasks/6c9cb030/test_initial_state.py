# test_initial_state.py
#
# Pytest suite that validates the *initial* machine state
# BEFORE the student sets up the regression-run environment.
#
# These tests must pass on a clean system where:
#   • The virtual environment /home/user/qa_env has NOT been created yet.
#   • The log file   /home/user/qa_env_setup.log does NOT exist yet.
#
# If either resource is already present, the tests will fail with a
# descriptive message so the learner knows something is amiss.

import os
import stat
import pytest

HOME = "/home/user"
VENV_DIR = os.path.join(HOME, "qa_env")
LOG_FILE = os.path.join(HOME, "qa_env_setup.log")


def _path_info(path: str) -> str:
    """
    Helper: return a human-readable description of a path’s type so the
    assertion message is clearer (e.g. 'file', 'directory', 'symlink').
    """
    if not os.path.exists(path):
        return "does not exist"

    mode = os.lstat(path).st_mode
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "special filesystem entry"


@pytest.mark.order(1)
def test_virtualenv_directory_absent_initially():
    """
    The virtual environment must NOT exist **before** the student follows
    the instructions.  If it is already present, something is pre-baked
    in the image and the learner will not get meaningful feedback.
    """
    assert not os.path.exists(VENV_DIR), (
        f"Pre-condition failure: Expected virtualenv directory '{VENV_DIR}' "
        f"to be absent, but it is a {_path_info(VENV_DIR)}."
    )


@pytest.mark.order(2)
def test_log_file_absent_initially():
    """
    The setup log file must NOT exist until the student creates it.
    """
    assert not os.path.exists(LOG_FILE), (
        f"Pre-condition failure: Expected log file '{LOG_FILE}' to be absent, "
        f"but it is a {_path_info(LOG_FILE)}."
    )