# test_initial_state.py
#
# This pytest suite verifies that the operating-system state **before**
# the student starts matches the assumptions laid out in the assignment.
# It checks only the *pre-existing* items and purposefully avoids any
# reference to the files/directories that are supposed to be created
# later (as required by the grading rubric).

import os
from pathlib import Path
import stat
import pytest

WORKSPACE = Path("/home/user/workspace")

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _is_regular_file(path: Path) -> bool:
    """
    Return True if `path` exists and is a regular file (not a directory,
    symlink, socket, etc.).
    """
    try:
        mode = path.stat().st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode)


# ----------------------------------------------------------------------
# Parametrised tests for the four initial files the student should
# start with.
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "relative_name",
    [
        "intro.md",
        "api.md",
        "style.md",
        "guide.txt",
    ],
)
def test_initial_files_exist_and_are_regular(relative_name):
    """
    Verify that each required starter file exists at the expected absolute
    path and is a regular file.
    """
    full_path = WORKSPACE / relative_name
    assert full_path.exists(), (
        f"Expected starter file {full_path} is missing. "
        "Verify that the project was set up correctly."
    )
    assert _is_regular_file(full_path), (
        f"{full_path} exists but is not a regular file."
    )


def test_no_subdirectories_yet():
    """
    The assignment does not guarantee the absence or presence of any
    particular sub-directories *except* the initial /home/user/workspace
    itself.  This test simply confirms that that directory exists and is
    indeed a directory, guarding against gross misconfiguration such as
    /home/user/workspace being a file or missing entirely.
    """
    assert WORKSPACE.exists(), "/home/user/workspace is missing."
    assert WORKSPACE.is_dir(), "/home/user/workspace exists but is not a directory."