# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating system
# before the student attempts the provisioning-marker exercise.
#
# The exercise will eventually ask the student to create the file
#   /home/user/provisioned.flag
# with very specific contents.  Because that file is considered **output** of
# the task, this test suite deliberately avoids mentioning it at all.
#
# Instead, we verify that the execution environment is sane and ready
# for the student:
#   • /home/user must exist and be a writable directory.
#   • Common GNU / POSIX utilities the student is expected to use
#     (echo, printf, cat, wc, stat) must be present in $PATH.
#
# These checks protect against grader mis-configuration and give students
# clear, actionable feedback if the base image is broken.

import os
import stat as statmod
import sys
import shutil
from pathlib import Path

import pytest


HOME = Path("/home/user")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _check_executable(tool: str) -> None:
    """
    Assert that a given executable is resolvable by shutil.which() and
    the path actually points to an executable file.
    """
    path = shutil.which(tool)
    assert path is not None, (
        f"The required tool '{tool}' is not available in $PATH.\n"
        "Make sure core utilities are installed and PATH is correctly set."
    )
    # Double-check that the located file really is executable to avoid
    # corner-cases where an alias or broken symlink might be returned.
    st_mode = os.stat(path).st_mode
    is_exec = bool(st_mode & (statmod.S_IXUSR | statmod.S_IXGRP | statmod.S_IXOTH))
    assert is_exec, (
        f"Located '{tool}' at '{path}', but it is not marked as executable."
    )


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_home_directory_exists_and_is_directory():
    """
    The base image must provide /home/user as a real directory.
    """
    assert HOME.exists(), (
        f"The expected home directory '{HOME}' does NOT exist.\n"
        "The environment seems mis-configured; please ensure the user home\n"
        "is created before running the exercise."
    )
    assert HOME.is_dir(), (
        f"'{HOME}' exists but is NOT a directory. "
        "Something is seriously wrong with the filesystem layout."
    )


def test_home_directory_is_writable(tmp_path):
    """
    /home/user must be writable so the student can create the marker file.
    We attempt to create and delete a temporary file inside that directory.
    """
    test_file = HOME / ".write_test_pytest"
    try:
        with open(test_file, "w") as fh:
            fh.write("ok")
        assert test_file.exists(), (
            f"Failed to create files inside '{HOME}'. "
            "Directory is not writable for the current user."
        )
    finally:
        try:
            test_file.unlink(missing_ok=True)
        except Exception as exc:  # pragma: no cover
            # Even if cleanup fails, we still want a clean error message.
            pytest.fail(f"Could not clean up temporary file '{test_file}': {exc}")


@pytest.mark.parametrize(
    "tool",
    [
        "echo",   # POSIX-shell builtin or /bin/echo
        "printf", # POSIX tool used for precise output
        "cat",    # Required by the grading rubric
        "wc",     # Required for line count verification
        "stat",   # Required for file size verification
    ],
)
def test_required_command_line_tools_are_available(tool):
    """
    Ensure every command that the grader says it will invoke is available
    and executable in the current $PATH.
    """
    _check_executable(tool)