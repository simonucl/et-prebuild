# test_initial_state.py
"""
Pytest suite to assert the **initial** state of the operating system before the
student begins the exercise.

The checks here are deliberately limited to generic, baseline characteristics of
the environment.  They do ***not*** mention or touch any of the files or
directories the learner is expected to create (e.g. `/home/user/deployment_configs`,
`prod.env`, or the status log).  This keeps the initial-state verification
orthogonal to the actual assignment while still ensuring the runtime environment
is sane and writable.
"""

import os
import shutil
import stat
import pytest


HOME_DIR = "/home/user"


def test_home_directory_exists():
    """
    The canonical home directory for the learner must exist and be a directory.
    """
    assert os.path.exists(
        HOME_DIR
    ), f"Expected {HOME_DIR} to exist, but it does not."
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected {HOME_DIR} to be a directory, but it is not."


def test_home_directory_is_writable():
    """
    The learner needs write permissions inside their home directory.
    """
    assert os.access(
        HOME_DIR, os.W_OK
    ), f"{HOME_DIR} is not writable—cannot proceed with the exercise."


@pytest.mark.parametrize(
    "exe",
    ["mkdir", "echo", "cat"],
)
def test_basic_unix_tools_are_available(exe):
    """
    Validate that the essential UNIX utilities required to complete the task
    are present in the PATH.
    """
    path = shutil.which(exe)
    assert (
        path and os.path.isfile(path) and os.access(path, os.X_OK)
    ), f'Utility "{exe}" is required but was not found in PATH.'