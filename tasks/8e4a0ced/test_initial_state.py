# test_initial_state.py
# -------------------------------------------------
# Pytest suite that validates the *initial* state of
# the operating system / filesystem before the
# learner begins the exercise described in the task
# prompt.
#
# The exercise requires the learner to create:
#   /home/user/iot_edge/api_test/
#       ├── server.py
#       └── api_responses.log
#
# At this “zero-state” moment, none of those paths
# or files should exist, and nothing should already
# be listening on TCP port 9000.
#
# If any of the assertions below fail, it means the
# playground was pre-populated (or polluted) with
# artefacts that the learner is supposed to create
# themselves, which would break the pedagogical
# flow of the assignment.
#
# Only Python’s standard library and pytest are used
# in accordance with the grading-infrastructure
# restrictions.

import os
import socket
from pathlib import Path

import pytest


API_TEST_DIR = Path("/home/user/iot_edge/api_test")
SERVER_PY = API_TEST_DIR / "server.py"
LOG_FILE = API_TEST_DIR / "api_responses.log"
PORT = 9000
HOST = "127.0.0.1"


def _port_is_open(host: str, port: int) -> bool:
    """Return True if something is listening on the given TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)  # short timeout; we only care about connect/no-connect
        try:
            sock.connect((host, port))
            return True
        except (ConnectionRefusedError, OSError):
            # ConnectionRefused → nothing is listening
            # OSError covers 'No route to host' etc.
            return False


def test_home_user_exists():
    assert Path("/home/user").exists(), (
        "Expected base directory /home/user to exist; the exercise assumes this "
        "is the student’s home directory."
    )


def test_api_test_directory_does_not_exist_yet():
    assert not API_TEST_DIR.exists(), (
        "/home/user/iot_edge/api_test/ already exists, but it should NOT be present "
        "before the student starts the task."
    )


@pytest.mark.parametrize(
    "path_to_check, description",
    [
        (SERVER_PY, "server.py (mock API implementation)"),
        (LOG_FILE, "api_responses.log (curl output log)"),
    ],
)
def test_solution_files_do_not_exist_yet(path_to_check: Path, description: str):
    assert not path_to_check.exists(), (
        f"{description} found at {path_to_check}. The workspace should start EMPTY so "
        "the student can create this file themselves."
    )


def test_nothing_listening_on_port_9000():
    assert not _port_is_open(HOST, PORT), (
        "TCP port 9000 is already in use. The learner’s mock server must be able to "
        "bind to this port; please ensure nothing is listening on 127.0.0.1:9000 at "
        "the start of the exercise."
    )