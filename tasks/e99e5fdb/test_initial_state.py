# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# filesystem **before** the student completes the assignment.
#
# The repository directory /home/user/infra must already exist, but it should
# be completely empty: specifically, there must be NO “Makefile” and NO
# “automation_setup.log” yet.  These files will be created by the student as
# part of the exercise.

import os
import stat
import pytest

REPO_DIR = "/home/user/infra"
MAKEFILE_PATH = os.path.join(REPO_DIR, "Makefile")
LOG_PATH = os.path.join(REPO_DIR, "automation_setup.log")


def _fmt_mode(path: str) -> str:
    """Return the octal file mode (e.g. '0o644') for clearer failure output."""
    try:
        return oct(os.stat(path).st_mode & 0o777)
    except FileNotFoundError:
        return "N/A (file not found)"


@pytest.mark.order(1)
def test_repo_directory_exists_and_is_directory():
    assert os.path.exists(REPO_DIR), (
        "The repository directory {0!r} does not exist. "
        "It should be present before starting the task.".format(REPO_DIR)
    )
    assert os.path.isdir(REPO_DIR), (
        "{0!r} exists but is not a directory. "
        "It must be a directory that will contain the student’s files.".format(REPO_DIR)
    )


@pytest.mark.order(2)
def test_makefile_does_not_exist_yet():
    assert not os.path.exists(MAKEFILE_PATH), (
        "Unexpected Makefile found at {0!r} (mode: {1}).\n"
        "The repository is supposed to be empty at the beginning; "
        "the student will create this file.".format(MAKEFILE_PATH, _fmt_mode(MAKEFILE_PATH))
    )


@pytest.mark.order(3)
def test_logfile_does_not_exist_yet():
    assert not os.path.exists(LOG_PATH), (
        "Unexpected automation_setup.log found at {0!r} (mode: {1}).\n"
        "The repository is supposed to be empty at the beginning; "
        "the student will create this file.".format(LOG_PATH, _fmt_mode(LOG_PATH))
    )