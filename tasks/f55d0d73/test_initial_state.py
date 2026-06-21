# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system /
# filesystem *before* the student carries out any actions for the
# "Provisioning Utility" exercise.  In short, we make sure the workspace under
# /home/user is clean so that the subsequent grading of the student's work is
# reliable.
#
# The tests deliberately FAIL when any artefact that the student is supposed to
# create later is already present.

import os
import stat
import pytest

USER_HOME = "/home/user"
DOCS_DIR = os.path.join(USER_HOME, "docs")
PROVISIONING_MD = os.path.join(DOCS_DIR, "provisioning.md")
LINT_SCRIPT = os.path.join(DOCS_DIR, "md_lint.sh")
LINT_LOG = os.path.join(DOCS_DIR, "md_lint.log")


def _assert_absent(path: str) -> None:
    """
    Helper that fails the test if the given path exists.

    Parameters
    ----------
    path : str
        Absolute path that must NOT exist yet.
    """
    assert not os.path.exists(
        path
    ), f"Unexpected pre-existing artefact at '{path}'. " \
       "The workspace must start empty for a fair evaluation."


def test_user_home_directory_exists():
    """
    Sanity-check that /home/user itself is available and is a directory.
    """
    assert os.path.isdir(
        USER_HOME
    ), f"Required base directory '{USER_HOME}' is missing. "\
       "The exercise cannot proceed."


def test_docs_directory_absent():
    """
    The /home/user/docs directory must NOT exist before the student starts the assignment.
    """
    _assert_absent(DOCS_DIR)


@pytest.mark.parametrize("filepath", [PROVISIONING_MD, LINT_SCRIPT, LINT_LOG])
def test_expected_files_absent(filepath):
    """
    None of the artefacts that the student will create should exist yet.
    """
    _assert_absent(filepath)