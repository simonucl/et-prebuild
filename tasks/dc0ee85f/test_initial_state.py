# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any action for the “CPU hog” performance-snapshot task.
#
# Expectations for the pristine state:
#   1. /home/user/cpu_hog.sh      must exist, be a regular file, and be executable.
#   2. /home/user/perf_logs       must *not* exist yet.
#   3. /home/user/perf_logs/cpu_hog_metrics.log must *not* exist yet.
#   4. No running process whose command contains the string “cpu_hog.sh”.
#
# Only the Python standard library and pytest are used.

import os
import stat
import subprocess
import sys
import re
import pytest

HOME = "/home/user"
HELPER_SCRIPT = os.path.join(HOME, "cpu_hog.sh")
PERF_DIR = os.path.join(HOME, "perf_logs")
METRICS_LOG = os.path.join(PERF_DIR, "cpu_hog_metrics.log")


def _is_executable(path: str) -> bool:
    """Return True if *path* is executable by its owner."""
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return False
    return bool(st.st_mode & stat.S_IXUSR)


def _running_cpu_hog_pids() -> list[int]:
    """
    Return a list of PIDs whose command (comm or args) contains 'cpu_hog.sh'.
    Uses `ps` which is available on all POSIX systems.
    """
    try:
        ps_out = subprocess.check_output(
            ["ps", "ax", "-o", "pid=,comm=,args="], text=True, stderr=subprocess.DEVNULL
        )
    except Exception as exc:  # pragma: no cover
        # If ps is missing, something is very wrong with the test environment.
        pytest.skip(f"Cannot run `ps`: {exc}")

    pids: list[int] = []
    for line in ps_out.splitlines():
        line = line.strip()
        if not line:
            continue
        # Line format: "<pid> <comm> <args>"
        parts = line.split(None, 2)
        if not parts:
            continue
        pid_part = parts[0]
        rest = " ".join(parts[1:])  # comm + args
        if "cpu_hog.sh" in rest:
            try:
                pids.append(int(pid_part))
            except ValueError:
                # Should not happen, but ignore malformed lines.
                pass
    return pids


def test_helper_script_present_and_executable():
    assert os.path.isfile(
        HELPER_SCRIPT
    ), f"Required helper script {HELPER_SCRIPT!r} is missing or not a regular file."
    assert _is_executable(
        HELPER_SCRIPT
    ), f"Helper script {HELPER_SCRIPT!r} exists but is not executable (expected mode 0755)."


def test_perf_logs_directory_absent():
    assert not os.path.exists(
        PERF_DIR
    ), f"Directory {PERF_DIR!r} should NOT exist before the exercise starts."


def test_metrics_log_file_absent():
    assert not os.path.exists(
        METRICS_LOG
    ), f"Log file {METRICS_LOG!r} should NOT exist before the exercise starts."


def test_no_cpu_hog_process_running():
    pids = _running_cpu_hog_pids()
    assert (
        not pids
    ), f"Found running cpu_hog.sh process(es) with PID(s): {pids}. No such process should be running at the start."