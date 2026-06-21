# test_initial_state.py
#
# This pytest file validates the *initial* state of the operating-system /
# filesystem before the student launches the web-server.  It must **NOT**
# test the final desired outcome—only the prerequisites that the
# instructions rely on.

import os
import socket
from pathlib import Path

import pytest


DOCS_DIR = Path("/home/user/docs")
LOGS_DIR = Path("/home/user/logs")
LOG_FILE = LOGS_DIR / "docs_webserver.log"
PORT = 8765
INDEX_FILE = DOCS_DIR / "index.html"
EXPECTED_INDEX_LINE = "<h1>Technical Documentation Home</h1>"


def test_docs_directory_exists():
    """
    The documentation directory must exist before the user starts the task.
    """
    assert DOCS_DIR.is_dir(), (
        f"Expected directory {DOCS_DIR} to exist but it does not. "
        "Create the directory and put the HTML files there."
    )


def test_index_html_exists_and_contents():
    """
    /home/user/docs/index.html must be present and contain the expected single line.
    """
    assert INDEX_FILE.is_file(), f"Required file {INDEX_FILE} is missing."

    # Read the first non-empty line to compare against expectation
    with INDEX_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:  # first non-empty line
                assert (
                    stripped == EXPECTED_INDEX_LINE
                ), (
                    f"The first non-empty line of {INDEX_FILE} is:\n"
                    f"  {stripped!r}\n"
                    f"but expected exactly:\n"
                    f"  {EXPECTED_INDEX_LINE!r}"
                )
                break
        else:
            pytest.fail(f"{INDEX_FILE} exists but is completely empty.")


def test_logs_directory_exists_and_log_absent():
    """
    /home/user/logs must already exist and be writable, but the log file must
    not yet exist in the initial state.
    """
    assert LOGS_DIR.is_dir(), f"Expected directory {LOGS_DIR} to exist but it does not."
    assert os.access(LOGS_DIR, os.W_OK), f"Directory {LOGS_DIR} is not writable by the user."

    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should NOT exist before the web server is launched. "
        "Delete or move it before starting the task."
    )


def test_port_8765_is_free():
    """
    Port 8765 must not have a listener before the user starts the web server.

    We attempt to bind to the port; if binding succeeds, the port is free.
    The socket is immediately released afterwards so it does not interfere
    with the student's future process.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Allow immediate reuse in case previous tests ran very quickly.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", PORT))
    except OSError as exc:
        pytest.fail(
            f"Port {PORT} is already in use (cannot bind: {exc}). "
            "Ensure no process is listening on this port before starting the task."
        )
    finally:
        sock.close()