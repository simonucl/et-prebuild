# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / file-system
# conditions before the student performs any actions for the assignment.
#
# These checks purposefully confirm that ONLY the provided starting artefacts
# exist and that nothing from the target solution is present yet.

import json
import os
import socket
import subprocess
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
README_PATH = PROJECT_DIR / "README.md"
WEBDOCS_DIR = PROJECT_DIR / "webdocs"
SERVER_LOG = PROJECT_DIR / "server_launch.log"

EXPECTED_README_CONTENT = "Project README\n"
SERVER_BIND_ADDRESS = "127.0.0.1"
SERVER_PORT = 8088
SERVER_CMD_LINE = "python3 -m http.server 8088 --bind 127.0.0.1"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def port_is_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Attempt to open a TCP connection to *host*:*port*.
    Returns True if the connection succeeds (port open),
    False if it is refused / unreachable.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False
        else:
            return True


def command_running_exact(cmd_line: str) -> bool:
    """
    Check /proc for a process whose **full** command line exactly equals *cmd_line*.
    Uses only the POSIX /proc filesystem, so no external dependencies.
    """
    proc_root = Path("/proc")
    for proc in proc_root.iterdir():
        if not proc.is_dir():
            continue
        if not proc.name.isdigit():
            continue
        cmdline_file = proc / "cmdline"
        try:
            data = cmdline_file.read_bytes()
            # Data are NUL ('\0') separated.
            if not data:
                continue
            # Convert NUL-separated byte string to argv list
            argv = data.rstrip(b"\0").split(b"\0")
            cmd = " ".join(arg.decode() for arg in argv)
            if cmd == cmd_line:
                return True
        except (FileNotFoundError, PermissionError):
            continue
    return False


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_project_directory_exists():
    assert PROJECT_DIR.exists(), f"Expected directory {PROJECT_DIR} to exist, but it does not."
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory."


def test_project_contains_only_readme(tmp_path_factory):
    """
    The initial repository should contain exactly one file (README.md)
    and no sub-directories yet.
    """
    entries = sorted(PROJECT_DIR.iterdir(), key=lambda p: p.name)
    names = [p.name for p in entries]

    assert names == ["README.md"], (
        f"Initial project directory should contain only 'README.md'. "
        f"Found: {', '.join(names) if names else '(empty directory)'}"
    )


def test_readme_exists_with_expected_content():
    assert README_PATH.exists(), f"Expected {README_PATH} to exist."
    assert README_PATH.is_file(), f"{README_PATH} exists but is not a regular file."

    content = README_PATH.read_text()
    assert content == EXPECTED_README_CONTENT, (
        f"{README_PATH} content mismatch.\n"
        f"Expected:\n{EXPECTED_README_CONTENT!r}\n"
        f"Got:\n{content!r}"
    )


def test_webdocs_directory_not_present_yet():
    assert not WEBDOCS_DIR.exists(), (
        f"The directory {WEBDOCS_DIR} should NOT exist before the student starts the task."
    )


def test_server_launch_log_absent():
    assert not SERVER_LOG.exists(), (
        f"{SERVER_LOG} should NOT exist before the student starts the task."
    )


def test_no_http_server_running_yet():
    # 1. Port should not be open
    assert not port_is_open(SERVER_BIND_ADDRESS, SERVER_PORT), (
        f"A process is already listening on {SERVER_BIND_ADDRESS}:{SERVER_PORT}. "
        f"The server must be launched only after the task is performed."
    )

    # 2. No python http.server process with the exact command line should be running
    assert not command_running_exact(SERVER_CMD_LINE), (
        "Found a running process with command line:\n"
        f"    {SERVER_CMD_LINE}\n"
        "The development server must be started as part of the task, "
        "so it should NOT be running at this point."
    )