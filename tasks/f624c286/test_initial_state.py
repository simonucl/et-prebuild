# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state
# *before* the student starts the repository API server or performs
# any HTTP interactions.
#
# Expectations:
# 1. The API implementation must be present at
#       /home/user/repo_api.py
# 2. The initial state file must exist at
#       /home/user/repo_state/artifacts.json
#    and contain exactly the two default artefacts.
# 3. Nothing must yet be listening on TCP port 9123.
# 4. The log file that the student will later create
#       /home/user/repo-tests/logs/api_test.log
#    must not exist at this point.

import json
import os
import socket
import errno
from pathlib import Path

import pytest

API_PATH = Path("/home/user/repo_api.py")
STATE_PATH = Path("/home/user/repo_state/artifacts.json")
LOG_FILE = Path("/home/user/repo-tests/logs/api_test.log")
PORT = 9123
HOST = "127.0.0.1"


def test_api_file_exists():
    """The main API implementation file must be present."""
    assert API_PATH.is_file(), (
        f"Expected API file not found at {API_PATH}. Make sure the repository "
        "contains repo_api.py in the correct location."
    )


def test_initial_state_file_exists_and_content():
    """The state JSON must exist and contain the default artefacts only."""
    assert STATE_PATH.is_file(), (
        f"Expected state file not found at {STATE_PATH}. "
        "The repository must ship with the initial state."
    )

    try:
        with STATE_PATH.open() as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        pytest.fail(f"State file {STATE_PATH} is not valid JSON: {exc}")

    expected = ["artifact-alpha", "artifact-beta"]
    assert isinstance(data, list), (
        f"State JSON must be a list, got {type(data).__name__} instead."
    )
    assert data == expected, (
        f"State JSON should initially contain {expected}, "
        f"but found {data}."
    )


def test_port_9123_not_listening_yet():
    """
    Nothing should be listening on 127.0.0.1:9123 before the student
    starts the service.  We attempt to connect; ECONNREFUSED (111) or
    a timeout is the expected result.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        err = sock.connect_ex((HOST, PORT))
        assert err in {errno.ECONNREFUSED, errno.ETIMEDOUT}, (
            f"Port {PORT} already appears to be in use. "
            "Make sure the repository API server is *not* running "
            "before beginning the assignment."
        )


def test_log_file_absent():
    """The log file must *not* exist yet."""
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should not exist before the exercise begins."
    )