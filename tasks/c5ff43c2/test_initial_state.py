# test_initial_state.py
#
# This pytest suite validates the **initial** state of the execution
# environment before the student performs any action for the “emergency
# static site” exercise.
#
# IMPORTANT:  These tests intentionally avoid checking for the presence
#             (or absence) of any task-specific output such as:
#               • /home/user/maintenance
#               • /home/user/maintenance/index.html
#               • /home/user/webserver_launch.log
#
# They only ensure that the operating system and filesystem are in a sane
# and expected baseline state that will let the student complete the task
# without conflicts.

import os
import socket
import tempfile
import errno
import pytest


HOME_DIR = "/home/user"
TEST_PORT = 8080
LOCALHOST = "127.0.0.1"


def test_home_directory_exists():
    """
    The base home directory for the student account must exist and be a
    directory.  If it does not, the rest of the exercise is impossible.
    """
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected {HOME_DIR} to exist and be a directory, but it was not found."


def test_home_directory_is_writable():
    """
    The student must be able to create files under /home/user.
    Attempt to create then delete a temporary file in that directory.
    """
    try:
        with tempfile.NamedTemporaryFile(dir=HOME_DIR, delete=True) as tmp:
            tmp.write(b"write-test")
            tmp.flush()
    except PermissionError as exc:
        pytest.fail(f"{HOME_DIR} is not writable: {exc}")


def test_port_8080_is_free():
    """
    Ensure nothing is listening on TCP port 8080 before the student
    starts their lightweight webserver.  We try to bind to the port; if
    it is already in use, bind() will raise an error.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # SO_REUSEADDR guards against TIME_WAIT edge-cases without masking
        # genuine "already in use" errors.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LOCALHOST, TEST_PORT))
    except OSError as exc:
        if exc.errno in (errno.EADDRINUSE, errno.EACCES):
            pytest.fail(
                f"Port {TEST_PORT} on {LOCALHOST} is already in use; "
                "it must be free before starting the exercise."
            )
        # Re-raise any unexpected socket error.
        raise
    finally:
        s.close()