# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem **before**
# the student performs any actions for the deployment task.  A failure here
# means the environment is not in the expected clean slate and the exercise
# cannot be graded reliably.

import os
import stat
import pytest

SOURCE_DIR = "/home/user/source"
SOURCE_JAR = "/home/user/source/app.jar"
BUILD_DIR = "/home/user/build"


def test_source_directory_exists():
    """/home/user/source must exist and be a directory."""
    assert os.path.isdir(
        SOURCE_DIR
    ), f"Expected source directory {SOURCE_DIR!r} to exist before the task starts."


def test_source_jar_exists_with_expected_contents():
    """
    /home/user/source/app.jar must exist and contain the ASCII text
    'dummy-artifact' with no trailing newline.
    """
    assert os.path.isfile(
        SOURCE_JAR
    ), f"Expected JAR file {SOURCE_JAR!r} to exist before the task starts."

    with open(SOURCE_JAR, "rb") as f:
        data = f.read()

    expected = b"dummy-artifact"
    assert (
        data == expected
    ), (
        f"Expected {SOURCE_JAR!r} to contain the exact bytes {expected!r}; "
        f"got {data!r}."
    )

    # Confirm the file is a regular file (not, e.g., a symlink or directory)
    mode = os.stat(SOURCE_JAR).st_mode
    assert stat.S_ISREG(mode), f"{SOURCE_JAR!r} must be a regular file."


def test_build_directory_absent():
    """/home/user/build must not exist at the start of the exercise."""
    assert not os.path.exists(
        BUILD_DIR
    ), f"Build directory {BUILD_DIR!r} should NOT exist before the task starts."