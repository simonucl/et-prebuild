# test_initial_state.py
#
# This pytest module verifies the workstation *before* the student carries out
# the “translation diagnostics” task.  At this point, neither the diagnostics
# directory nor the diagnostics file should yet exist.  If either one is
# already present, the pre-exercise state is wrong and the test will fail with
# a clear, actionable message.

import os
import stat
import pytest

HOME = "/home/user"
DIAG_DIR = os.path.join(HOME, "diagnostics")
DIAG_FILE = os.path.join(DIAG_DIR, "translation_preupdate_diag.txt")


def _is_regular_file(path: str) -> bool:
    """
    Return True if *path* exists and is a regular file.
    """
    try:
        mode = os.stat(path).st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode)


def _is_directory(path: str) -> bool:
    """
    Return True if *path* exists and is a directory.
    """
    try:
        mode = os.stat(path).st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISDIR(mode)


def test_diagnostics_file_absent():
    """
    The pre-task state must *not* already contain the diagnostics file.
    If it exists (regular file or otherwise), the exercise has already
    been completed or the environment is dirty, so we fail early.
    """
    assert not os.path.exists(DIAG_FILE), (
        f"The diagnostics file {DIAG_FILE!r} already exists. "
        "The workstation should be in a clean, pre-update state."
    )


def test_diagnostics_directory_clean_state():
    """
    The diagnostics directory may or may not exist prior to the exercise.
    If it exists, it must *not* already contain the diagnostics file.
    We also ensure that if the path exists, it is a directory (not a file).
    """
    if os.path.exists(DIAG_DIR):
        assert _is_directory(DIAG_DIR), (
            f"The path {DIAG_DIR!r} exists but is not a directory."
        )
        assert not _is_regular_file(DIAG_FILE), (
            f"The diagnostics directory {DIAG_DIR!r} already contains "
            f"{DIAG_FILE!r}.  The student has nothing to create."
        )