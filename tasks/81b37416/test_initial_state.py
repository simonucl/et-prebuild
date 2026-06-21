# test_initial_state.py
#
# This test-suite verifies that the operating-system/filesystem is in the
# expected “before the student starts” state for the *loopback-ping log*
# exercise.
#
# Expectations BEFORE any student action:
#   1.  /home/user/logs            MUST NOT exist.
#   2.  /home/user/logs/loopback_ping.log  MUST NOT exist.
#   3.  A working `ping` executable must be available on the PATH
#       (commonly /bin/ping or /usr/bin/ping) and must be able to send
#       a single ICMP echo request to 127.0.0.1 successfully.
#
# If any of these assertions fail, the student’s environment is not in the
# required initial state and the test will raise an informative error.

import os
import subprocess
import shutil
import sys
import pytest
from pathlib import Path


HOME_DIR = Path("/home/user").expanduser()
LOG_DIR = HOME_DIR / "logs"
LOG_FILE = LOG_DIR / "loopback_ping.log"


def _find_ping_executable() -> Path:
    """
    Locate a usable 'ping' binary.
    Returns a pathlib.Path object pointing at the binary if found,
    otherwise raises FileNotFoundError.
    """
    # First, check common absolute locations.
    for candidate in (Path("/bin/ping"), Path("/usr/bin/ping"), Path("/sbin/ping")):
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate

    # Fallback: use shutil.which to search the PATH.
    location = shutil.which("ping")
    if location and os.access(location, os.X_OK):
        return Path(location)

    raise FileNotFoundError("No executable 'ping' command found on the system.")


@pytest.mark.order(1)
def test_home_directory_exists():
    assert HOME_DIR.is_dir(), (
        f"Expected home directory '{HOME_DIR}' to exist before the task starts."
    )


@pytest.mark.order(2)
def test_logs_directory_absent():
    assert not LOG_DIR.exists(), (
        f"'{LOG_DIR}' should NOT exist before the student runs the task. "
        "Please remove it to reset the environment."
    )


@pytest.mark.order(3)
def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' should NOT exist before the student runs the task. "
        "Please remove it to reset the environment."
    )


@pytest.mark.order(4)
def test_ping_executable_available_and_works():
    """
    Ensure that an executable 'ping' command exists and that a single ICMP
    echo request to 127.0.0.1 succeeds (exit status 0).
    """
    ping_path = _find_ping_executable()  # Raises FileNotFoundError if not found.

    # Run a minimal connectivity test: exactly one packet to the loopback
    # address.  `-c 1` sends one packet, `-q` suppresses per-packet output and
    # prints only the summary (which we discard here; we only care about exit
    # status).
    try:
        completed = subprocess.run(
            [str(ping_path), "-c", "1", "-q", "127.0.0.1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,  # seconds
            check=False,
        )
    except Exception as exc:
        pytest.fail(
            f"Executing '{ping_path}' failed with exception: {exc}. "
            "The system must be able to run the 'ping' command."
        )

    assert completed.returncode == 0, (
        "The 'ping' command could not successfully send a packet to 127.0.0.1 "
        f"(return code {completed.returncode}). Ensure basic connectivity and "
        "that ICMP is permitted."
    )