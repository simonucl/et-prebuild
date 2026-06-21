# test_initial_state.py
#
# This pytest file verifies that the operating‐system state *before* the
# student runs any commands is clean and ready for the exercise.
#
# It specifically asserts that the “answer” artefacts the grader will
# later look for are **not** already in place.  If any of those artefacts
# are found, the test fails with a clear message so that the exercise
# cannot be accidentally short-circuited.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
CI_DIR = HOME / "mobile_ci"
CI_LOG = CI_DIR / "ci_env_freeze.log"


@pytest.fixture(scope="module")
def ci_dir_exists():
    """
    Helper fixture: Returns True if /home/user/mobile_ci exists and is a
    directory, False otherwise.
    """
    return CI_DIR.is_dir()


def test_ci_log_does_not_exist(ci_dir_exists):
    """
    The freeze log MUST NOT exist yet.  The student’s task is to create
    it.  If it is already present, the initial state is incorrect.
    """
    assert not CI_LOG.exists(), (
        f"Precondition failed: {CI_LOG} already exists.  "
        "The environment must start WITHOUT this file so that the "
        "student’s command can create it."
    )


def test_ci_log_parent_dir_is_clean(ci_dir_exists):
    """
    If the parent directory exists, ensure it does NOT already contain
    a non-empty freeze log file.  Empty stub files are also disallowed
    because the grader expects the student to write fresh content.
    """
    if ci_dir_exists:
        # Directory exists — make sure any prospective log file is absent.
        assert not CI_LOG.exists(), (
            f"Precondition failed: {CI_LOG} already exists in an "
            "otherwise pre-created directory.  Remove it so the student "
            "can generate the correct file."
        )
    else:
        # It is perfectly fine (and even expected) that the directory
        # does not exist yet; no further assertions needed here.
        pass