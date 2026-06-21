# test_initial_state.py
#
# This test-suite verifies that the execution environment is sane *before*
# the student attempts the task.  We purposefully avoid checking for the
# presence or absence of any of the files / directories that the student
# has been asked to create; instead we make sure that the basics the
# student relies on are in place.

import os
import errno
from pathlib import Path
import pytest


HOME = Path("/home/user")


def test_home_directory_exists():
    """
    The working directory for the student must exist.

    We deliberately *do not* check for any sub-directories or files that the
    student is asked to create in the assignment; that is handled by the
    post-exercise tests.
    """
    assert HOME.is_dir(), (
        f"Expected {HOME} to exist as a directory, "
        "but it was not found."
    )


def test_home_directory_is_writable(tmp_path):
    """
    The student must be able to write in their home directory.

    We attempt to create and delete a temporary file inside /home/user.
    """
    test_file = HOME / ".write_test_tmp"
    try:
        # Touch the file.  If this fails, the directory is not writable.
        with open(test_file, "w"):
            pass
        assert test_file.exists(), (
            f"Unable to create files inside {HOME}; "
            "please ensure it is writable."
        )
    finally:
        # Best-effort clean-up: ignore errors if the file cannot be removed.
        try:
            test_file.unlink(missing_ok=True)
        except OSError as exc:  # pragma: no cover  (cleanup, non-critical)
            if exc.errno not in (errno.ENOENT, errno.EPERM):
                raise


def test_bash_is_available_and_executable():
    """
    The assignment requires a shebang that points to /bin/bash.
    Confirm that /bin/bash exists and is executable.
    """
    bash_path = Path("/bin/bash")
    assert bash_path.exists(), "/bin/bash is required but was not found."
    assert os.access(bash_path, os.X_OK), "/bin/bash exists but is not executable."