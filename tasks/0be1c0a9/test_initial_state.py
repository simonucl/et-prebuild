# test_initial_state.py
#
# Pytest suite to validate the _initial_ operating-system / filesystem state
# _before_ the student performs any of the actions described in the assignment:
#
#   • No results directory or summary file should yet exist.
#   • A working “ping” executable must be available so the student can use it.
#
# These tests use only the Python standard library and pytest.

import os
import shutil
import subprocess
import sys
import stat
import pytest

# --------------------------------------------------------------------------- #
# CONSTANTS
# --------------------------------------------------------------------------- #

HOME = "/home/user"
NET_BENCH_DIR = os.path.join(HOME, "net_benchmark")
SUMMARY_FILE = os.path.join(NET_BENCH_DIR, "loopback_ping_summary.txt")


# --------------------------------------------------------------------------- #
# HELPERS
# --------------------------------------------------------------------------- #

def _is_executable(path: str) -> bool:
    """
    Return True if 'path' exists, is a regular file and has at least one
    executable bit set for owner/group/other.
    """
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return False

    if not stat.S_ISREG(st.st_mode):
        return False

    return bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def _system_has_ipv4_loopback() -> bool:
    """
    Quick sanity check that 127.0.0.1 is reachable via ping.
    We intentionally send only 1 packet so as not to disturb anything.
    If ping is missing we skip this check elsewhere.
    """
    ping = shutil.which("ping")
    if not ping:
        return False
    try:
        # The command should complete quickly; 1 packet, 1 second deadline.
        subprocess.run(
            [ping, "-c", "1", "-w", "1", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


# --------------------------------------------------------------------------- #
# TESTS
# --------------------------------------------------------------------------- #

def test_no_benchmark_directory_yet():
    """
    The directory /home/user/net_benchmark must NOT exist before the student
    starts.  The task explicitly instructs the student to create it.
    """
    assert not os.path.exists(
        NET_BENCH_DIR
    ), (
        f"The directory {NET_BENCH_DIR!r} already exists.\n"
        "The assignment requires the student to create it; "
        "please remove it so the initial state is clean."
    )


def test_no_summary_file_yet():
    """
    The summary file must be absent prior to running the benchmark.
    """
    assert not os.path.exists(
        SUMMARY_FILE
    ), (
        f"The summary file {SUMMARY_FILE!r} already exists.\n"
        "It should be produced _after_ the student runs the benchmark."
    )


def test_ping_command_present_and_executable():
    """
    Validate that a usable 'ping' command is available somewhere in $PATH.
    This is essential for the student to complete the benchmark.
    """
    ping_path = shutil.which("ping")
    assert ping_path is not None, (
        "The 'ping' utility is not found in PATH; "
        "a minimal Linux install must provide it."
    )
    assert _is_executable(ping_path), (
        f"The detected ping binary at {ping_path!r} is not executable."
    )


def test_ipv4_loopback_is_reachable():
    """
    A single-packet ping to 127.0.0.1 should succeed on a healthy system.
    If ping is missing, this test is skipped (covered by the previous test).
    """
    ping_path = shutil.which("ping")
    if ping_path is None:
        pytest.skip("'ping' command not present; loopback reachability not testable")

    reachable = _system_has_ipv4_loopback()
    assert reachable, (
        "The IPv4 loopback address 127.0.0.1 is not reachable via ping.\n"
        "This indicates a fundamental networking issue that must be resolved "
        "before the assignment can proceed."
    )