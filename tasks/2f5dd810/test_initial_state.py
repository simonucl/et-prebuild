# test_initial_state.py
#
# This pytest suite verifies that the *initial* operating-system / filesystem
# state is clean before the student starts the assignment “tiny internal HTTP
# service”.  In particular, it asserts that nothing related to the target
# service (directory structure, files, or background process) is already
# present.  If any of these artefacts are found, the test will fail with a
# clear explanation so the learner knows the environment is not in the
# expected pristine state.

import os
import pytest


MONITORING_DIR = "/home/user/monitoring"
ALERTS_DIR = os.path.join(MONITORING_DIR, "alerts")
LOG_FILE = os.path.join(MONITORING_DIR, "webserver_7070.log")
STATUS_FILE = os.path.join(ALERTS_DIR, "webserver.status")


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _iter_pids():
    """
    Iterate over all numeric PIDs visible in /proc (Linux).
    Falls back to an empty iterator on non-Linux systems.
    """
    if not os.path.isdir("/proc"):
        return []
    for name in os.listdir("/proc"):
        if name.isdigit():
            yield name


def _http_server_7070_pids():
    """
    Return a list of PIDs whose command line contains BOTH
    'http.server' and '7070'.  Only /proc is used (stdlib only).
    """
    matches = []
    for pid in _iter_pids():
        cmd_path = os.path.join("/proc", pid, "cmdline")
        try:
            with open(cmd_path, "rb") as fh:
                # cmdline is '\0' separated
                raw = fh.read().split(b'\0')
                # decode silently; ignore undecodable bytes
                parts = [p.decode(errors="ignore") for p in raw if p]
        except (FileNotFoundError, PermissionError):
            # Process may have exited or we lack permissions; skip it
            continue

        # Quick “contains” check (no strict ordering needed here)
        joined = " ".join(parts)
        if "http.server" in joined and "7070" in joined:
            matches.append(int(pid))
    return matches


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_no_python_http_server_on_7070_yet():
    """
    The student has not started the server yet; therefore **no** python3
    http.server process listening on port 7070 should be running.
    """
    pids = _http_server_7070_pids()
    assert (
        len(pids) == 0
    ), f"Expected no python3 http.server 7070 process yet, but found PID(s): {pids}"


def test_no_log_file_present():
    """
    The web-server’s log file must NOT exist before the learner starts
    the task.
    """
    assert not os.path.exists(
        LOG_FILE
    ), f"Unexpected pre-existing log file found at {LOG_FILE!r}. Please start from a clean state."


def test_no_status_file_present():
    """
    The status file must NOT exist prior to task execution.
    """
    assert not os.path.exists(
        STATUS_FILE
    ), f"Unexpected pre-existing status file found at {STATUS_FILE!r}. The directory should be created by the learner."


def test_alerts_dir_not_precreated():
    """
    The alerts directory itself should not be present yet.  It will be
    created by the learner as part of the task.  A pre-existing directory
    indicates the environment is not pristine.
    """
    assert not os.path.exists(
        ALERTS_DIR
    ), f"Directory {ALERTS_DIR!r} already exists; expected a clean slate."