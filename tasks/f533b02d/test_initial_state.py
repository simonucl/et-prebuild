# test_initial_state.py
"""
Pytest suite to validate the **initial** operating-system state
_before_ the student carries out the file-creation exercise.

The task requirements (see assignment text) state that *after* the
student’s work is complete the following should exist:

    /home/user/fw_config                     (directory)
    /home/user/fw_config/block_ssh.rule      (file)
    /home/user/fw_config/block_ssh.log       (file)

Because this test-suite is executed **prior** to any student action,
it asserts that none of the above paths exist yet.  If any of them
*do* exist, the initial environment is considered invalid and the
tests will fail with a clear, actionable message.
"""

import os
import stat
import pytest

HOME_DIR = "/home/user"
FW_DIR = os.path.join(HOME_DIR, "fw_config")
RULE_FILE = os.path.join(FW_DIR, "block_ssh.rule")
LOG_FILE = os.path.join(FW_DIR, "block_ssh.log")


def _path_type(path: str):
    """
    Helper that returns a human-readable string describing what a path
    currently is, to aid in assertion error messages.
    """
    if os.path.islink(path):
        return "a symlink"
    if os.path.isdir(path):
        return "a directory"
    if os.path.isfile(path):
        return "a regular file"
    if os.path.exists(path):
        # Exists but is neither file nor dir (e.g. socket, device node)
        mode = os.stat(path, follow_symlinks=False).st_mode
        return f"special file (mode: {stat.S_IFMT(mode):#o})"
    return "non-existent"


@pytest.mark.parametrize(
    "path, should_exist",
    [
        (FW_DIR, False),
        (RULE_FILE, False),
        (LOG_FILE, False),
    ],
)
def test_paths_absent_initially(path: str, should_exist: bool):
    """
    Ensure that the directory and files expected *after* the exercise
    do **not** exist yet.  A pre-existing path would indicate that the
    testing environment is polluted or that the student’s solution was
    run prematurely.
    """
    exists = os.path.exists(path)
    assert exists is should_exist, (
        f"Initial-state violation: expected {path!r} to be "
        f'{"present" if should_exist else "absent"}, '
        f"but it is {_path_type(path)}."
    )