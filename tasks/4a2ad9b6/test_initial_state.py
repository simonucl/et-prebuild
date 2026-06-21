# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# state **before** the student runs any of their automation.
#
# The tasks the student will later perform are expected to create:
#   1. /home/user/mock_metadata_server/
#      ├── instance.json
#      ├── network.json
#      └── storage.json
#   2. /home/user/provisioning_logs/latest_metadata_snapshot.log
#   3. A HTTP server bound to 127.0.0.1:9080 whose document root is the
#      directory in (1).
#
# None of these artefacts should exist **yet**.  These tests make sure the
# environment is clean so that any later grading reflects only the
# student’s work.

import os
import pathlib
import socket
import errno
import pytest

HOME = pathlib.Path("/home/user")
METADATA_DIR = HOME / "mock_metadata_server"
PROVISIONING_DIR = HOME / "provisioning_logs"
LOG_FILE = PROVISIONING_DIR / "latest_metadata_snapshot.log"
PORT = 9080
HOST = "127.0.0.1"


def _can_connect(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Try to establish a TCP connection to (host, port).
    Returns True on success, False if connection is refused / timed out.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, TimeoutError):
        return False
    except OSError as exc:  # e.g. "No route to host"
        if exc.errno in {errno.EHOSTUNREACH, errno.ECONNREFUSED, errno.ETIMEDOUT}:
            return False
        raise  # Unexpected error, re-raise for visibility


def test_metadata_directory_does_not_exist():
    """
    The metadata directory must NOT pre-exist.
    """
    assert not METADATA_DIR.exists(), (
        f"Precondition failure: {METADATA_DIR} should not exist yet. "
        "Please start with a clean workspace."
    )


@pytest.mark.parametrize("fname", ["instance.json", "network.json", "storage.json"])
def test_individual_json_files_do_not_exist(fname):
    """
    Even if someone prematurely created the directory, the JSON files must
    not be present.
    """
    json_path = METADATA_DIR / fname
    assert not json_path.exists(), (
        f"Precondition failure: unexpected file {json_path} is already present."
    )


def test_log_file_does_not_exist():
    """
    The snapshot log must not exist yet.
    """
    assert not LOG_FILE.exists(), (
        f"Precondition failure: {LOG_FILE} already exists."
    )


def test_port_9080_not_listening():
    """
    Ensure no service is already bound to 127.0.0.1:9080.  The student’s
    automation will start its own HTTP server here.
    """
    assert not _can_connect(HOST, PORT), (
        "Precondition failure: something is already listening on "
        f"{HOST}:{PORT}.  Make sure the port is free before you begin the task."
    )