# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# before the learner performs any action for the “stub API” exercise.
#
# It asserts that none of the required artefacts (files, directories,
# processes, etc.) yet exist or are in the desired final state.  If any
# of them are already present, the test suite fails with a clear,
# prescriptive message.
#
# Allowed imports: stdlib + pytest only.

import os
import socket
import pytest
from pathlib import Path

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _port_is_listening(host: str, port: int, timeout: float = 0.5) -> bool:
    """Return True if a TCP connection to (host, port) succeeds."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_cm_api_stub_directory_absent_or_empty():
    """
    The directory /home/user/cm_api_stub must *not* yet contain the required
    config_v1.json file with the exact final-state content.  Either the file is
    missing altogether or its content does not match the final specification.
    """
    cm_dir = HOME / "cm_api_stub"
    config_file = cm_dir / "config_v1.json"
    expected_content = b'{"version":"1.0.0","service":"config-manager"}'

    # It is acceptable if the directory is entirely absent.
    if not cm_dir.exists():
        return

    # Directory exists: ensure the target file is not yet in its final form.
    assert not config_file.exists(), (
        f"Pre-task check failed: {config_file} already exists but should "
        "not be present before the exercise begins."
    )

    # If someone *did* create the file but with different content,
    # that is still an early violation because they have started the task.
    if config_file.exists():
        actual = config_file.read_bytes()
        assert actual != expected_content, (
            f"Pre-task check failed: {config_file} already contains the exact "
            "final content; the task appears to have been completed ahead of time."
        )


def test_config_tracker_log_absent():
    """
    The CSV log /home/user/config_tracker/change_log.csv must not yet exist.
    Presence of the directory itself is also unexpected at this stage.
    """
    tracker_dir = HOME / "config_tracker"
    log_file = tracker_dir / "change_log.csv"

    assert not tracker_dir.exists(), (
        f"Pre-task check failed: directory {tracker_dir} already exists; "
        "this suggests the learner has begun or completed the exercise."
    )
    assert not log_file.exists(), (
        f"Pre-task check failed: {log_file} already exists; "
        "the change-log should be created only after running the required probes."
    )


def test_no_server_listening_on_9090():
    """
    Ensure that no process is currently listening on TCP 127.0.0.1:9090.
    A running HTTP server would indicate the task was started prematurely.
    """
    is_open = _port_is_listening("127.0.0.1", 9090)
    assert not is_open, (
        "Pre-task check failed: a process is already listening on "
        "127.0.0.1:9090. The learner should start the server only during "
        "the exercise, not before."
    )