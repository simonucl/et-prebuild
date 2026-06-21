# test_initial_state.py
#
# Pytest suite to verify the *initial* state of the operating system / file
# system before the student performs any actions for the “artifact-manager”
# task.  In the final solution a single file, /home/user/artifact_dns_check.log,
# must be created with exact contents.  At this point (prior to the student’s
# work) that file must **not** exist.  If it is already present, the test
# should fail with a clear, explanatory message so that the student knows the
# starting environment is incorrect.

import os
import stat
import pytest

HOME_DIR = "/home/user"
LOG_FILE = os.path.join(HOME_DIR, "artifact_dns_check.log")


def _human_mode(bits: int) -> str:
    """
    Helper to return file mode in human-readable octal form, e.g. '0644'.
    """
    return oct(bits & 0o777)[2:].rjust(4, "0")


def test_home_directory_exists():
    """
    Sanity-check that the user’s home directory exists and is a directory.
    This guards against mis-configured environments which would render the
    remainder of the exercise impossible.
    """
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected home directory {HOME_DIR!r} to exist and be a directory."


def test_artifact_log_absent_initially():
    """
    The required log file must NOT exist before the student has carried out
    the assignment.  Its presence would indicate that the environment is in
    an unexpected state (e.g. a previous run polluted the workspace).
    """
    if os.path.exists(LOG_FILE):
        # Gather a bit more context to help the student clean up if needed.
        st = os.stat(LOG_FILE)
        perms = _human_mode(st.st_mode)
        msg_lines = [
            f"Unexpected pre-existing file {LOG_FILE!r}.",
            "The initial state should not include this file.",
            f"Current size: {st.st_size} bytes",
            f"Permissions: {perms}",
            "Please remove or rename the file before starting the task.",
        ]
        pytest.fail("\n".join(msg_lines))