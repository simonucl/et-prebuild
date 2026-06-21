# test_initial_state.py
#
# This pytest suite verifies that the operating-system state is **clean**
# before the student attempts the credential-rotation exercise.  In
# particular, it asserts that neither the target directory nor the log
# file already exist.

import os
import stat
import pytest

HOME = "/home/user"
TARGET_DIR = os.path.join(HOME, "credential_rotation")
TARGET_LOG = os.path.join(TARGET_DIR, "benchmark.log")


def _human_path(path: str) -> str:
    """
    Return a human-readable representation of a filesystem path,
    quoting it so that any surrounding whitespace is obvious in the
    assertion messages.
    """
    return f"'{path}'"


def test_home_directory_exists():
    """Sanity check: the base home directory itself must exist."""
    assert os.path.isdir(HOME), (
        f"Expected the home directory {_human_path(HOME)} to exist "
        "before starting the exercise."
    )


@pytest.mark.parametrize("path", [TARGET_DIR, TARGET_LOG])
def test_target_paths_absent(path):
    """
    Ensure that neither the directory nor the log file from the task
    exist yet.  The student is expected to create them as part of the
    assignment.
    """
    assert not os.path.exists(path), (
        f"The path {_human_path(path)} already exists. "
        "The initial state should be clean: you must create this "
        "directory / file yourself as part of the task."
    )


def test_no_partial_artifacts_inside_home():
    """
    Guard against partially completed work: if the parent directory
    exists, ensure it is completely empty.  This catches the case where
    the student accidentally created the directory but not the file, or
    vice-versa.
    """
    if os.path.isdir(TARGET_DIR):
        # Directory exists when it should not; provide a detailed diff.
        contents = os.listdir(TARGET_DIR)
        pytest.fail(
            f"The directory {_human_path(TARGET_DIR)} already exists and "
            f"contains: {contents!r}.  Remove it so the grader starts from "
            "a known clean state."
        )
    elif os.path.isfile(TARGET_DIR):
        # A non-directory file is blocking the desired directory path.
        mode = os.stat(TARGET_DIR).st_mode
        type_desc = (
            "regular file" if stat.S_ISREG(mode) else "special file/device"
        )
        pytest.fail(
            f"A {type_desc} already exists at {_human_path(TARGET_DIR)}. "
            "Please remove or rename it so the exercise can create the "
            "required directory."
        )