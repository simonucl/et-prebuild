# test_initial_state.py
#
# Pytest suite that verifies the initial OS / filesystem state
# before the student performs any actions for the “network_logs”
# connectivity-performance snapshot exercise.
#
# Truth (pre-task state):
#   • The directory /home/user/network_logs must NOT exist.
#   • Consequently, the file /home/user/network_logs/ping_test.log
#     must also NOT exist.
#   • The standard CLI tool “ping” should be available on PATH.
#
# Any deviation from the above constitutes an invalid starting
# environment and must fail loudly so the learner and graders
# immediately see what is wrong.

import os
import shutil
import stat
import subprocess

import pytest

NETWORK_LOG_DIR = "/home/user/network_logs"
PING_LOG_FILE = "/home/user/network_logs/ping_test.log"


def _describe_path(path: str) -> str:
    """Return a human-readable description of the path for error msgs."""
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return f"{path!r} (path does not exist)"
    else:
        mode = stat.filemode(st.st_mode)
        return f"{path!r} (exists – mode: {mode}, type: {'directory' if stat.S_ISDIR(st.st_mode) else 'file'})"


def test_network_logs_directory_absent():
    """
    The directory /home/user/network_logs should NOT exist prior to the task.
    If it already exists, the starting state is incorrect.
    """
    assert not os.path.exists(
        NETWORK_LOG_DIR
    ), f"Pre-task directory unexpectedly present: {_describe_path(NETWORK_LOG_DIR)}. The directory must NOT exist before the exercise begins."


def test_ping_log_file_absent():
    """
    The file /home/user/network_logs/ping_test.log must not exist because the
    directory itself should be absent at this stage.
    """
    assert not os.path.exists(
        PING_LOG_FILE
    ), f"Pre-task file unexpectedly present: {_describe_path(PING_LOG_FILE)}. The log file must NOT exist before the exercise begins."


def test_ping_tool_available():
    """
    Ensure the standard 'ping' CLI tool is available; otherwise, the learner
    cannot fulfil the assignment using minimal Linux utilities.
    """
    ping_path = shutil.which("ping")
    assert ping_path is not None, "The 'ping' command is not available on the system PATH; it is required for the assignment."
    # Sanity-check that running 'ping -V' or 'ping -h' exits successfully.
    # We use a very short timeout to avoid delays in CI.
    try:
        subprocess.run(
            [ping_path, "-V"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=False,
        )
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to execute '{ping_path} -V'. Error: {exc}")