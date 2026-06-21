# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state *before* the student performs any action for the deployment task.
#
# The tests purposefully confirm that none of the deliverables required
# by the assignment are present yet and that the target TCP port is free.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import socket
import errno
import subprocess
import sys
import os
import pytest

# Absolute paths used throughout the assignment
BASE_RELEASES_DIR = Path("/home/user/releases")
RELEASE_DIR       = BASE_RELEASES_DIR / "release-1.0.0"
INDEX_HTML        = RELEASE_DIR / "index.html"
SERVER_LOG        = BASE_RELEASES_DIR / "server.log"
VERIFY_LOG        = BASE_RELEASES_DIR / "deployment_verification.log"

@pytest.fixture(scope="module")
def base_dir_exists():
    """
    Ensure the base directory /home/user/releases is present.
    Returns the Path object for downstream tests.
    """
    assert BASE_RELEASES_DIR.exists(), (
        f"Expected base directory '{BASE_RELEASES_DIR}' to exist "
        "so the student has a place to create releases."
    )
    assert BASE_RELEASES_DIR.is_dir(), (
        f"'{BASE_RELEASES_DIR}' exists but is not a directory."
    )
    return BASE_RELEASES_DIR


def test_release_directory_absent(base_dir_exists):
    """The release directory must NOT exist before the student starts."""
    assert not RELEASE_DIR.exists(), (
        f"Found unexpected directory '{RELEASE_DIR}'. "
        "The workspace should be clean before the student begins."
    )


@pytest.mark.parametrize(
    "path_obj,description",
    [
        (INDEX_HTML, "index.html file"),
        (SERVER_LOG, "server.log file"),
        (VERIFY_LOG, "deployment_verification.log file"),
    ],
)
def test_deliverable_files_absent(path_obj: Path, description: str):
    """None of the deliverable files should exist initially."""
    assert not path_obj.exists(), (
        f"Unexpected {description} found at '{path_obj}'. "
        "The student has not yet produced any deliverables."
    )


def test_port_8000_is_free():
    """
    Port 8000 on localhost must be available—no process should be
    listening on it yet.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(1.0)
        result = sock.connect_ex(("127.0.0.1", 8000))
        assert result != 0, (
            "TCP port 8000 is already in use on 127.0.0.1. "
            "The initial state should have this port free."
        )
    finally:
        sock.close()


def test_no_python_http_server_process_running():
    """
    Ensure there is no python -m http.server process already running.
    Parsing `ps` output keeps us within stdlib (via subprocess).
    """
    try:
        # `ps -f -u <uid>` lists processes for the current user in full format
        uid = os.getuid()
        ps_output = subprocess.check_output(
            ["ps", "-f", "-u", str(uid)], text=True, stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If ps is unavailable, fall back to simply passing the test after
        # checking that port 8000 is free (already done in previous test).
        pytest.skip("Unable to inspect process list with 'ps'; skipped.")
        return

    for line in ps_output.strip().splitlines():
        if "python" in line and "http.server" in line:
            pytest.fail(
                "Detected a running Python http.server process before the "
                "assignment has started:\n" + line
            )