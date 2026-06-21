# test_initial_state.py
#
# This pytest suite verifies that the filesystem is still in its **initial**
# (pre-task) state.  Nothing related to the “secure_project” hierarchy should
# exist yet.  If any of the paths already exist, the student would not be
# starting from a clean slate and the test must fail with a clear, actionable
# message.
#
# Stdlib only + pytest, no external dependencies.
import os
import stat
import pytest

HOME = "/home/user"
SECURE_PROJECT_ROOT = os.path.join(HOME, "secure_project")

EXPECTED_DIRS = [
    SECURE_PROJECT_ROOT,
    os.path.join(SECURE_PROJECT_ROOT, "bin"),
    os.path.join(SECURE_PROJECT_ROOT, "data"),
    os.path.join(SECURE_PROJECT_ROOT, "logs"),
]

ACCESS_LOG = os.path.join(SECURE_PROJECT_ROOT, "logs", "access.log")


def _path_state(path):
    """
    Helper that returns a tuple describing the current state of *path*.

    Returns
    -------
    exists : bool
    is_file : bool
    is_dir : bool
    perm_octal : str | None
        Octal permission string (e.g. '755') if the path exists; None otherwise.
    """
    exists = os.path.exists(path)
    is_file = os.path.isfile(path)
    is_dir = os.path.isdir(path)
    perm = None
    if exists:
        # stat.S_IMODE extracts the permission bits; format as octal without `0o`
        perm = format(stat.S_IMODE(os.stat(path).st_mode), "03o")
    return exists, is_file, is_dir, perm


@pytest.mark.parametrize("path", EXPECTED_DIRS)
def test_expected_directories_do_not_exist_yet(path):
    """
    None of the directories that will later be created by the student should
    exist before they begin.  If any are present, the environment is already
    “contaminated” and the exercise cannot be graded reliably.
    """
    exists, is_file, is_dir, perm = _path_state(path)
    assert not exists, (
        f"Pre-check failed: '{path}' already exists (dir={is_dir}, file={is_file}, "
        f"perm={perm}). The filesystem must start clean so the student can create it."
    )


def test_access_log_does_not_exist_yet():
    """
    The access.log file must also be absent at the start of the exercise.
    """
    exists, is_file, is_dir, perm = _path_state(ACCESS_LOG)
    assert not exists, (
        f"Pre-check failed: '{ACCESS_LOG}' already exists "
        f"(dir={is_dir}, file={is_file}, perm={perm})."
    )