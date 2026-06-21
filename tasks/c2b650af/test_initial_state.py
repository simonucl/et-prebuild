# test_initial_state.py
"""
Pytest suite to verify that the system is in a pristine state **before**
the student begins work on the “debug-workbench” task.

The tests assert that *none* of the files or directories which are supposed
to be created by the student already exist.  If anything is found, the test
suite fails with a clear, actionable message.

Only the Python standard library and pytest are used.
"""

import os
import stat
import pytest

# Root of the workbench that the student will create
ROOT_DIR = "/home/user/devops_debug"

# All artifacts that must *not* be present yet
MUST_NOT_EXIST = [
    ROOT_DIR,
    os.path.join(ROOT_DIR, "logs"),
    os.path.join(ROOT_DIR, "logs", "app1.log"),
    os.path.join(ROOT_DIR, "logs", "app2.log"),
    os.path.join(ROOT_DIR, "logs", "error_combined.log"),
    os.path.join(ROOT_DIR, "scripts"),
    os.path.join(ROOT_DIR, "scripts", "extract_errors.sh"),
    os.path.join(ROOT_DIR, "error_summary.csv"),
    os.path.join(ROOT_DIR, "logs_archive.tar.gz"),
]

@pytest.mark.parametrize("path", MUST_NOT_EXIST)
def test_artifact_is_absent(path):
    """
    Ensure that no part of the target workbench already exists.

    If any of these paths are found, the environment is not clean and the
    student would start with an unfair advantage (or face unexpected errors).
    """
    assert not os.path.exists(path), (
        f"Pre-existing path detected: {path!r}\n"
        "The working environment must be completely clean before the student "
        "starts.  Remove this file/directory or use a fresh workspace."
    )