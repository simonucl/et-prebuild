# test_initial_state.py
#
# This pytest suite validates that the machine is in a *clean* state
# before the student performs any work for the “Build Artifacts
# Repository” task.
#
# We assert that nothing from the expected final outcome is already
# present, so the student starts from a known baseline.
#
# What we deliberately *do NOT* want to find *yet*:
#   1. /home/user/artifacts directory
#   2. /home/user/artifacts/index.html file
#   3. A process listening on TCP port 8123
#   4. /home/user/webserver_launch.log file
#
# If any of these already exist, the environment is “dirty” and the
# subsequent grading of the student’s work would be unreliable.

import os
import pathlib
import socket
import errno
import pytest
import subprocess
import sys
import shlex
import time


ARTIFACT_DIR = pathlib.Path("/home/user/artifacts")
INDEX_HTML   = ARTIFACT_DIR / "index.html"
LOG_FILE     = pathlib.Path("/home/user/webserver_launch.log")
PORT         = 8123
LOCALHOST    = "127.0.0.1"


def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Return True if a TCP connection to (host, port) can be established.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (ConnectionRefusedError, OSError):
            return False


def test_artifact_directory_absent():
    """
    The /home/user/artifacts directory should NOT exist yet.
    """
    assert not ARTIFACT_DIR.exists(), (
        f"Precondition failed: {ARTIFACT_DIR} already exists. "
        "The environment should start clean so the student can create it."
    )


def test_index_html_absent():
    """
    The landing page should NOT exist before the student creates it.
    """
    assert not INDEX_HTML.exists(), (
        f"Precondition failed: {INDEX_HTML} already exists. "
        "The student must create this file during the task."
    )


def test_port_8123_not_listening():
    """
    Nothing should be listening on TCP port 8123 yet.
    We detect this by attempting to open a socket to 127.0.0.1:8123.
    """
    is_open = _is_port_open(LOCALHOST, PORT)
    assert not is_open, (
        f"Precondition failed: Something is already listening on port {PORT}. "
        "The student needs this port to be free to start their web server."
    )


def test_log_file_absent():
    """
    The webserver_launch.log file should NOT exist before the student runs
    their commands.  An existing file could cause grading ambiguities when
    we later validate the last two lines.
    """
    assert not LOG_FILE.exists(), (
        f"Precondition failed: {LOG_FILE} already exists. "
        "The log file must be created by the student's script, not beforehand."
    )