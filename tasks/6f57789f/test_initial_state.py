# test_initial_state.py
#
# This pytest suite verifies that the starting operating-system / filesystem
# state is exactly as expected *before* the student carries out any actions for
# the assignment “SQLite meta-information & summary report”.
#
# Expectations _before_ work starts:
#   1. The directory  /home/user/project             MUST exist.
#   2. The file       /home/user/project/meta.db     MUST **not** exist.
#   3. The file       /home/user/project/category_counts.log MUST **not** exist.
#
# Any deviation from these rules will make the test suite fail with a clear
# message so that issues can be corrected early.

import os
import stat
import pytest

PROJECT_DIR = "/home/user/project"
META_DB = os.path.join(PROJECT_DIR, "meta.db")
SUMMARY_LOG = os.path.join(PROJECT_DIR, "category_counts.log")


def _path_type(path: str) -> str:
    """
    Helper that returns a human-readable description of what the path points to.

    Possible return values:
        • 'file'       – regular file
        • 'dir'        – directory
        • 'symlink'    – symbolic link
        • 'other'      – anything else (FIFO, socket, device, etc.)
        • 'missing'    – path does not exist
    """
    if not os.path.exists(path) and not os.path.islink(path):
        return "missing"
    mode = os.lstat(path).st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


@pytest.mark.order(1)
def test_project_directory_exists_and_is_directory():
    """
    The /home/user/project directory must be present and must be a real
    directory (not a symlink, not a file).
    """
    path_type = _path_type(PROJECT_DIR)
    assert path_type == "dir", (
        f"Expected {PROJECT_DIR} to be a directory, "
        f"but found it to be {path_type!r}."
    )


@pytest.mark.order(2)
@pytest.mark.parametrize("artifact", [META_DB, SUMMARY_LOG])
def test_target_artifacts_do_not_yet_exist(artifact):
    """
    Neither the SQLite database file nor the summary log file should exist
    before the student begins the task.
    """
    path_type = _path_type(artifact)
    assert path_type == "missing", (
        f"Pre-existing artifact found at {artifact}. "
        f"The path currently points to a {path_type}. "
        "The environment must start clean so the student can create the file "
        "as part of the exercise."
    )