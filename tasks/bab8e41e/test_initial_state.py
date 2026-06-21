# test_initial_state.py
#
# This pytest suite validates that the freshly-provisioned Linux
# workstation is still in its pristine state *before* the student
# begins the bootstrap task.  We intentionally avoid inspecting
# any of the files or directories that the student is expected to
# create later (per the grading rules).  The only thing we check
# is the user’s existing ~/.bashrc, which must exist and must **not**
# yet contain the ANDROID_HOME export line that the assignment
# instructs the student to add.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
BASHRC_PATH = HOME / ".bashrc"
EXPORT_LINE = "export ANDROID_HOME=/home/user/android-sdk"


def test_bashrc_file_exists():
    """
    The ~/.bashrc file must already be present on the fresh system.
    If it's missing, the environment is not in the expected pristine
    state for the exercise.
    """
    assert BASHRC_PATH.exists(), (
        f"Expected {BASHRC_PATH} to exist on the clean system, "
        "but it was not found."
    )
    assert BASHRC_PATH.is_file(), f"{BASHRC_PATH} exists but is not a regular file."


def test_android_home_not_yet_exported():
    """
    Verify that the target export line has *not* yet been added to ~/.bashrc.
    The student will append this line in the course of completing the task,
    so its presence beforehand would constitute an invalid initial state.
    """
    with BASHRC_PATH.open("r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]

    assert EXPORT_LINE not in lines, (
        "The line that exports ANDROID_HOME is already present in ~/.bashrc. "
        "The initial environment must not contain this line—students are "
        "responsible for appending it during the task."
    )