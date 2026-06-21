# test_initial_state.py
#
# This pytest suite validates that the workspace is **clean** before the
# student executes the command that will create the “vulnscan_env” virtual
# environment.  Nothing related to the venv should exist yet.  If any of the
# artefacts are already present, the test will fail with a clear message.
#
# Checked paths (all must be absent *before* the student acts):
#   1. /home/user/vulnscan_env                   (directory)
#   2. /home/user/vulnscan_env/pyvenv.cfg        (file)
#   3. /home/user/vulnscan_env/bin/python        (file/executable)
#
# Only stdlib and pytest are used, per the instructions.

import os
import stat
import pytest

HOME = "/home/user"
VENV_DIR = os.path.join(HOME, "vulnscan_env")
POSSIBLE_PATHS = [
    VENV_DIR,
    os.path.join(VENV_DIR, "pyvenv.cfg"),
    os.path.join(VENV_DIR, "bin", "python"),
]


@pytest.mark.parametrize("path", POSSIBLE_PATHS)
def test_venv_artifacts_do_not_exist_yet(path):
    """
    Ensure no part of the virtual environment already exists.

    Why:
        The exercise requires the student to *create* the virtual
        environment; the filesystem must therefore be clean beforehand.
    """
    assert not os.path.exists(
        path
    ), (
        f"Found unexpected path '{path}'.\n"
        "The workspace should be empty before the student runs the venv "
        "creation command, but this path already exists.  "
        "Remove it so the task can be performed and graded correctly."
    )


def test_python_binary_is_not_preexisting_executable():
    """
    Double-check that an executable is not sitting at the expected venv
    interpreter path.  Even if the file exists, it must not be executable;
    otherwise the environment is considered pre-populated.
    """
    python_path = os.path.join(VENV_DIR, "bin", "python")
    if os.path.exists(python_path):
        mode = os.stat(python_path).st_mode
        is_exec = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        assert (
            not is_exec
        ), (
            f"'{python_path}' already exists and is executable.  "
            "The virtual environment must be created by the student; "
            "remove this interpreter first."
        )