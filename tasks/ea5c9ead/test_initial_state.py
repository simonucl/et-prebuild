# test_initial_state.py
#
# Pytest suite to validate the machine’s state *before* the student
# starts the “backup-service” health-check task.
#
# What we expect at this point:
#   • The mock server script exists at /home/user/mock_backup_api.py.
#   • Nothing is yet listening on TCP port 9090.
#   • Neither the results directory nor the two result files exist.
#
# Any deviation from these expectations will fail with an
# explanatory message so the student immediately knows
# what prerequisite is missing or unexpectedly present.

import os
import socket
import pathlib
import pytest

SERVER_SCRIPT = "/home/user/mock_backup_api.py"
PORT = 9090
LOG_FILE = "/home/user/backup_test/backup_api_test.log"
SUMMARY_FILE = "/home/user/backup_test/summary.txt"
RESULT_DIR = "/home/user/backup_test"


def _is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    """
    Returns True if a TCP connection to (host, port) succeeds,
    False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)  # short, we only need a quick yes/no
        return sock.connect_ex((host, port)) == 0


def test_server_script_present():
    """
    Ensure the mock server source file required for the exercise
    is present and is a regular file.
    """
    assert os.path.isfile(SERVER_SCRIPT), (
        f"Required server script not found at {SERVER_SCRIPT}. "
        "The student cannot start the service without this file."
    )


def test_port_9090_not_listening_yet():
    """
    The specification requires the student to start the service
    themselves.  Therefore, nothing should be bound to 0.0.0.0:9090
    (we check via localhost) at the beginning of the exercise.
    """
    assert not _is_port_open(PORT), (
        f"TCP port {PORT} is already in use. "
        "The backup-service should not be running before the student starts it."
    )


def test_result_directory_not_yet_created():
    """
    The directory /home/user/backup_test should not exist before the
    student creates it.  If it exists already, something is wrong or
    left over from a previous run.
    """
    assert not pathlib.Path(RESULT_DIR).exists(), (
        f"Result directory {RESULT_DIR} unexpectedly exists. "
        "It must be created by the student as part of the task."
    )


@pytest.mark.parametrize(
    "path", [LOG_FILE, SUMMARY_FILE],
    ids=["log file", "summary file"]
)
def test_output_files_absent(path):
    """
    Neither backup_api_test.log nor summary.txt should exist yet.
    """
    assert not os.path.exists(path), (
        f"Output file {path} already exists. "
        "These files must be created only after the student performs the task."
    )