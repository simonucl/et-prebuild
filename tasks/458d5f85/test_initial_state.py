# test_initial_state.py
#
# This pytest suite validates the baseline operating-system / filesystem
# state **before** the student performs any actions for the “DNS incident
# response” exercise.
#
# What we assert:
# 1. The student’s home directory (/home/user) already exists.
# 2. The target artefact (/home/user/incidents/resolution.log) does *not*
#    yet exist.  (A pre-existing file would invalidate the task.)
# 3. At least one standards-compliant DNS utility (dig, drill, or getent)
#    is available in the $PATH, so the student can complete the task.
# 4. The operating system currently resolves “localhost” to exactly
#    127.0.0.1; this guarantees that the student will obtain the expected
#    answer when they query the A-record.
#
# Only stdlib + pytest are used, and each failure message explains
# precisely what is wrong.

import os
import shutil
import socket
import pytest
from pathlib import Path

HOME = Path("/home/user")
INCIDENTS_DIR = HOME / "incidents"
RESOLUTION_LOG = INCIDENTS_DIR / "resolution.log"
DNS_TOOLS = ("dig", "drill", "getent")


def test_home_directory_exists():
    """Confirm that /home/user is present and is a directory."""
    assert HOME.exists(), "Expected home directory /home/user to exist, but it is missing."
    assert HOME.is_dir(), "/home/user exists but is not a directory."


def test_resolution_log_not_present_yet():
    """
    Ensure the incidents directory or resolution.log file do NOT exist yet.
    The exercise requires the student to create them.
    """
    assert not INCIDENTS_DIR.exists(), (
        f"The directory {INCIDENTS_DIR} already exists. "
        "The environment should be pristine before the student starts."
    )
    assert not RESOLUTION_LOG.exists(), (
        f"The file {RESOLUTION_LOG} already exists. "
        "It must be created by the student during the task."
    )


def test_dns_tool_available():
    """
    At least one of dig, drill, or getent must be available in PATH.
    This guarantees the student has a standards-compliant utility.
    """
    found_tools = [tool for tool in DNS_TOOLS if shutil.which(tool)]
    assert found_tools, (
        "None of the required DNS utilities were found in PATH. "
        "Install at least one of: dig, drill, getent."
    )


def test_localhost_resolves_to_127001():
    """
    Verify that 'localhost' currently resolves to 127.0.0.1.
    The assignment and downstream grading rely on this resolution.
    """
    try:
        ipv4_addr = socket.gethostbyname("localhost")
    except socket.gaierror as exc:  # pragma: no cover
        pytest.fail(f"System could not resolve 'localhost': {exc}")

    assert (
        ipv4_addr == "127.0.0.1"
    ), f"Expected 'localhost' to resolve to 127.0.0.1, but got '{ipv4_addr}'."