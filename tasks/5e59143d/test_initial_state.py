# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any actions for the “localhost RTT
# benchmarking” task.  These tests purposefully avoid checking for the
# output artefacts (/home/user/benchmarks and the .bench file) because
# those objects are expected to be created *by* the student solution.
#
# Only the availability of required tools and a sane environment
# (/home/user, ping to 127.0.0.1, etc.) are verified here.
#
# NOTE:  • Stdlib + pytest only.
#        • Clear, instructive assertion messages on failure.

import os
import shutil
import subprocess
import tempfile
import re
import pytest
from pathlib import Path


HOME = Path("/home/user")


# ---------------------------------------------------------------------------
# Filesystem sanity checks
# ---------------------------------------------------------------------------

def test_home_directory_exists_and_is_directory():
    """The /home/user directory must exist and be a directory."""
    assert HOME.exists(), (
        f"Expected home directory {HOME} to exist, but it does not."
    )
    assert HOME.is_dir(), (
        f"Expected {HOME} to be a directory, but it is not."
    )


def test_home_directory_is_writable():
    """
    Regular users must be able to write inside /home/user; create and delete
    a temporary file to confirm.
    """
    try:
        with tempfile.NamedTemporaryFile(dir=HOME, delete=True) as tmp:
            tmp.write(b"probe")
            tmp.flush()
            assert Path(tmp.name).exists(), (
                f"Unable to create files in {HOME}; "
                "check directory permissions."
            )
    except PermissionError as exc:
        pytest.fail(
            f"Write permission missing for {HOME}: {exc}"
        )


# ---------------------------------------------------------------------------
# ping-related checks
# ---------------------------------------------------------------------------

PING_PATH = shutil.which("ping")


def test_ping_command_is_available():
    """The ‘ping’ utility must be present in PATH and executable."""
    assert PING_PATH is not None, (
        "The 'ping' command is not found in the current PATH. "
        "It is required to complete the assignment."
    )
    assert os.access(PING_PATH, os.X_OK), (
        f"Found ping at {PING_PATH} but it is not executable."
    )


def test_ping_localhost_succeeds_and_returns_summary():
    """
    A single ping to 127.0.0.1 should succeed (exit code 0) and the output
    must contain the usual 'min/avg/max' statistics line.
    """
    # Use -c 1 to send exactly one echo request; suppress stderr to avoid
    # noise in the test output.
    proc = subprocess.run(
        ["ping", "-c", "1", "127.0.0.1"],
        capture_output=True,
        text=True
    )

    assert proc.returncode == 0, (
        "Running 'ping -c 1 127.0.0.1' failed. "
        "Check that ICMP is allowed and the ping binary has the proper "
        "capabilities (e.g., CAP_NET_RAW) or setuid bit."
    )

    combined_output = proc.stdout + proc.stderr
    # The summary line in iputils ping contains 'min/avg/max/mdev', but some
    # implementations omit '/mdev'.  Look for the core 'min/avg/max'.
    assert re.search(r"\bmin/avg/max\b", combined_output), (
        "Ping to 127.0.0.1 did not contain the expected 'min/avg/max' "
        "statistics line. The assignment relies on this output format."
    )