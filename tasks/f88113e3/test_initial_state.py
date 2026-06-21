# test_initial_state.py
#
# This pytest suite verifies that the environment is a clean slate before the
# learner starts working on the “mock-API” exercise.  It intentionally checks
# that none of the files / directories / network listeners that the task will
# later create are present yet.  If any of them already exist the test(s) will
# fail with a clear, actionable message.

import os
import socket
import errno
import subprocess
import sys
import textwrap

import pytest

# --------------------------------------------------------------------------- #
# Constants – the artefacts that must *not* exist at the outset
# --------------------------------------------------------------------------- #
SERVICE_DIR = "/home/user/mock_service"
V1_DIR      = f"{SERVICE_DIR}/v1"
V2_DIR      = f"{SERVICE_DIR}/v2"

PODS_JSON   = f"{V1_DIR}/pods.json"
STATUS_TXT  = f"{V1_DIR}/status.txt"
HEALTH_JSON = f"{V2_DIR}/health.json"

RESULTS_DIR = "/home/user/api_test_results"
REPORT_LOG  = f"{RESULTS_DIR}/curl_report.log"

ALL_DIRECTORIES = [SERVICE_DIR, V1_DIR, V2_DIR, RESULTS_DIR]
ALL_FILES       = [PODS_JSON, STATUS_TXT, HEALTH_JSON, REPORT_LOG]

SERVER_PORT = 8787
SERVER_HOST = "127.0.0.1"   #  localhost


# --------------------------------------------------------------------------- #
# Helper(s)
# --------------------------------------------------------------------------- #
def _port_is_listening(host: str, port: int) -> bool:
    """
    Return True iff we can establish a TCP connection to ``host:port``.
    Uses only the Python stdlib.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        try:
            sock.connect((host, port))
        except socket.error as e:
            if e.errno in {errno.ECONNREFUSED, errno.ETIMEDOUT}:
                return False
            # Any *other* error (including success) means something unexpected
            return False
        # connect() succeeded – someone is listening
        return True


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("path", ALL_DIRECTORIES)
def test_directories_do_not_exist(path):
    """
    None of the target directories should exist before the learner runs their
    solution.  If they do, we risk masking logic errors or stale state.
    """
    assert not os.path.isdir(path), textwrap.dedent(
        f"""
        The directory {path!r} already exists, but the exercise requires the
        learner to create it.  Please remove it so the workspace starts clean.
        """
    ).strip()


@pytest.mark.parametrize("path", ALL_FILES)
def test_files_do_not_exist(path):
    """
    The resource / log files must *not* be present yet.
    """
    assert not os.path.isfile(path), textwrap.dedent(
        f"""
        The file {path!r} already exists, but the exercise expects it to be
        created by the learner.  Remove the file to start from a clean state.
        """
    ).strip()


def test_port_8787_not_listening():
    """
    Port 8787 should be free (no process listening) so that the learner can
    start their one-shot HTTP server without collisions.
    """
    is_open = _port_is_listening(SERVER_HOST, SERVER_PORT)
    assert not is_open, textwrap.dedent(
        f"""
        TCP port {SERVER_PORT} appears to be in use on {SERVER_HOST}.  The task
        requires the learner to start an HTTP server on that port; having it
        already bound will cause their attempt to fail.
        """
    ).strip()


def test_no_http_server_process_running():
    """
    A very lightweight sanity check that no stray “python -m http.server” or
    similar process is running.  We only use tools guaranteed to exist in a
    POSIX-ish environment: `ps` and stdlib parsing.
    """
    # `ps -eo pid,command` gives us PID and the full command line
    try:
        proc = subprocess.run(
            ["ps", "-eo", "pid,command"],
            check=True,
            stdout=subprocess.PIPE,
            text=True
        )
    except FileNotFoundError:
        # Extremely minimal environments could lack `ps`; if so we skip.
        pytest.skip("`ps` command not available; skipping process check.")
        return

    http_processes = [
        line for line in proc.stdout.splitlines()
        if "http.server" in line or "SimpleHTTPServer" in line
    ]

    assert not http_processes, textwrap.dedent(
        """
        Detected an already-running HTTP server process (e.g. started with
        `python -m http.server`).  Please stop it so that the learner can start
        their own instance as part of the exercise.
        """
    ).strip()