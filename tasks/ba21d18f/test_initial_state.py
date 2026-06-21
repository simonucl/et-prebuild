# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “FinOps loop-back latency test” exercise.
#
# These checks run **before** the student’s solution is executed; they make
# sure the workstation is in a sane, predictable state and that no part of
# the required deliverable already exists.
#
# IMPORTANT:  Do **not** add assertions about any output artefacts
#             (e.g. /home/user/finops/localhost_ping.log).
#
# Only   stdlib + pytest   are used.

import os
import socket
import shutil
import subprocess
import sys

import pytest

HOME_DIR = "/home/user"


@pytest.mark.dependency(name="home_dir")
def test_home_directory_present():
    """
    Verify that the base home directory exists and is a directory.

    The exercise expects students to work under /home/user, so the path
    itself must be present *before* they begin.
    """
    assert os.path.isdir(HOME_DIR), (
        f"Expected the home directory {HOME_DIR!r} to exist and be "
        "a directory, but it is missing."
    )


@pytest.mark.dependency(name="ping_binary", depends=["home_dir"])
def test_ping_binary_is_available_and_executable():
    """
    Ensure that the standard `ping` tool is available on the PATH.

    The task requires students to use the native ICMP ping utility.
    """
    ping_path = shutil.which("ping")
    assert ping_path is not None, (
        "The `ping` utility could not be found on the system PATH. "
        "Please install the iputils-ping package or provide a compatible "
        "binary so that the student can issue ICMP Echo Requests."
    )
    assert os.access(ping_path, os.X_OK), (
        f"The ping binary located at {ping_path!r} is not executable."
    )


@pytest.mark.dependency(name="localhost_resolves", depends=["home_dir"])
def test_localhost_resolves():
    """
    Confirm that the hostname 'localhost' resolves via libc / NSS.

    A functioning loop-back name resolution is required for the student’s
    network-diagnostic command to succeed.
    """
    try:
        addr_info = socket.getaddrinfo("localhost", None)
    except socket.gaierror as exc:
        pytest.fail(f"Hostname resolution for 'localhost' failed: {exc}")
    # Ensure at least one address in the result list is the IPv4 loop-back.
    assert any(info[4][0] == "127.0.0.1" for info in addr_info), (
        "Resolution of 'localhost' did not return the expected 127.0.0.1 "
        "IPv4 address."
    )


@pytest.mark.dependency(depends=["ping_binary", "localhost_resolves"])
def test_loopback_ping_succeeds():
    """
    Run a *single* quiet ping against the loop-back interface to prove that
    ICMP Echo traffic is permitted for unprivileged users.

    Many Linux distributions include a set-UID `ping`, so this should work
    in a normal teaching container.  If the ping fails it is important that
    the failure is surfaced here (not during grading of the student task).
    """
    # Use -c 1 (one packet) and -q (quiet output except for the summary).
    ping_cmd = ["ping", "-c", "1", "-q", "localhost"]
    proc = subprocess.run(
        ping_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    assert proc.returncode == 0, (
        "A simple loop-back ping failed.  Output was:\n"
        f"{proc.stdout}"
    )

    # Basic sanity check on the summary line.
    # We expect something like: "1 packets transmitted, 1 received, 0% packet loss, time 0ms"
    summary_present = any("packets transmitted" in line for line in proc.stdout.splitlines())
    assert summary_present, (
        "The loop-back ping did not emit a packet-loss summary as expected.  "
        "Raw output:\n"
        f"{proc.stdout}"
    )