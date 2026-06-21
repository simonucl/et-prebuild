# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem is in a clean
# state *before* the learner executes the task.  In particular, the benchmark
# timestamp file that the learner must create **must not exist yet**.
#
#   Expected post-task artefact:
#       /home/user/profile/logs/epoch_utc_time.log
#       (with the single line "1970-01-01 00:00:00 UTC\n")
#
# For the initial state we therefore assert that this file is **absent** so the
# learner can create it deterministically.  A clear failure message is provided
# if anything is already in place, indicating that the environment is dirty.

import os
import stat
import pytest


TARGET_DIR = "/home/user/profile/logs"
TARGET_FILE = os.path.join(TARGET_DIR, "epoch_utc_time.log")


def _is_regular_file(path: str) -> bool:
    """
    Return ``True`` if *path* exists and is a regular (non-symlink) file.
    """
    try:
        mode = os.lstat(path).st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode)


def test_target_file_must_not_exist_before_task(tmp_path_factory):
    """
    The reference timestamp file should NOT exist before the learner runs the
    required one-liner.  If the file is present (regardless of its contents)
    the environment is considered dirty and the test fails with a clear hint.
    """
    assert not os.path.exists(
        TARGET_FILE
    ), (
        "The file {file!r} already exists, but the learner is expected to "
        "create it.  Please reset the environment so the file is absent."
    ).format(file=TARGET_FILE)


def test_target_path_must_not_be_symlink():
    """
    Even if the target path exists, it must not be a symlink that could trick
    later checks.  We explicitly verify that the path is absent or at least
    not a symlink.
    """
    if os.path.lexists(TARGET_FILE):  # lexists() returns True for broken links
        assert not os.path.islink(
            TARGET_FILE
        ), (
            f"{TARGET_FILE!r} is a symbolic link.  The learner must create a "
            "regular file; please remove the symlink so the environment is "
            "clean."
        )


def test_target_directory_state_is_clean():
    """
    The parent directory may or may not exist—both scenarios are allowed.
    If it does exist, ensure it is a directory (not a file/symlink) and that
    no premature timestamp file sneaked in.
    """
    if os.path.lexists(TARGET_DIR):
        assert os.path.isdir(
            TARGET_DIR
        ), (
            f"{TARGET_DIR!r} exists but is not a directory.  Remove or rename "
            "it so the learner can create the required directory structure."
        )

        # If the directory exists, double-check the unwanted file is not inside.
        assert not _is_regular_file(
            TARGET_FILE
        ), (
            "Found an unexpected file at {file!r}.  The learner is supposed to "
            "create this file; please remove it before running the exercise."
        )