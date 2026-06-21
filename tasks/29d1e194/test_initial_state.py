# test_initial_state.py
#
# This pytest suite validates the filesystem *before* the student performs the
# task.  It confirms that only the prerequisite objects exist (the Android SDK
# directory and the Gradle wrapper script) and that none of the artefacts the
# student is expected to create are present yet.
#
# PRE-EXISTING OBJECTS THAT **MUST** BE PRESENT:
#   • /home/user/build-tools/android-sdk-r30            (directory)
#   • /home/user/projects/sample-app/gradlew           (regular file)
#
# OBJECTS THAT **MUST NOT** BE PRESENT YET:
#   • /home/user/android-sdk   (symlink to be created by the student)
#   • /home/user/gradlew       (symlink to be created by the student)
#   • /home/user/link_update.log (verification log to be produced by the student)
#
# Any failure message should clearly tell the student what prerequisite is
# missing or what artefact already exists when it should not.

import os
import stat
import pytest

HOME = "/home/user"

# ---- Helper functions ----------------------------------------------------- #

def _assert_exists(path: str):
    assert os.path.exists(path), f"Expected '{path}' to exist but it does not."

def _assert_is_dir(path: str):
    _assert_exists(path)
    assert os.path.isdir(path), f"Expected '{path}' to be a directory."

def _assert_is_file(path: str):
    _assert_exists(path)
    assert os.path.isfile(path), f"Expected '{path}' to be a regular file."

def _assert_not_exists(path: str):
    assert not os.path.exists(path), (
        f"'{path}' already exists, but the task requires the student to create it."
    )

# ---- Tests for objects that MUST exist ----------------------------------- #

def test_android_sdk_directory_present():
    """
    The real Android SDK directory that links will point to must already exist.
    """
    sdk_dir = os.path.join(HOME, "build-tools", "android-sdk-r30")
    _assert_is_dir(sdk_dir)

def test_gradlew_file_present():
    """
    The definitive Gradle wrapper script that the symlink will point to must already exist.
    """
    gradlew_path = os.path.join(HOME, "projects", "sample-app", "gradlew")
    _assert_is_file(gradlew_path)

# ---- Tests for objects that MUST NOT exist (yet) ------------------------- #

@pytest.mark.parametrize(
    "path",
    [
        os.path.join(HOME, "android-sdk"),
        os.path.join(HOME, "gradlew"),
    ],
)
def test_symlinks_absent(path):
    """
    Neither of the required symbolic links should exist prior to the student's action.
    They will be created (or corrected) by the student script.
    """
    _assert_not_exists(path)

def test_verification_log_absent():
    """
    The verification log must *not* exist before the student finishes the task.
    """
    log_path = os.path.join(HOME, "link_update.log")
    _assert_not_exists(log_path)