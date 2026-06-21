# test_initial_state.py
#
# Pytest suite that validates the machine **before** the student starts
# working on the “sensor-collector” exercise.  These tests assert that
# none of the required artefacts are present yet and that no related
# process is already running.  If any test fails, it means the starting
# environment is not clean and the student would get misleading
# feedback once they begin the task.

import os
import subprocess
import re
import pytest
from pathlib import Path

# Constants for absolute paths that must **NOT** exist yet.
IOT_DIR = Path("/home/user/iot_edge")
SCRIPT_PATH = IOT_DIR / "sensor_collector.sh"
DATA_LOG = IOT_DIR / "data.log"
PID_FILE = IOT_DIR / "collector.pid"
PROCESS_LOG = IOT_DIR / "process_log.txt"


def _ps_output() -> str:
    """
    Return the full 'ps -eo pid,comm,args' output as text.
    Using only stdlib (subprocess) to stay within allowed libraries.
    """
    result = subprocess.run(
        ["ps", "-eo", "pid,comm,args"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def _collector_pids_from_ps() -> set[int]:
    """
    Parse `ps` output for any line that looks like sensor_collector.sh.
    Returns a set of matching PIDs (empty set if none found).
    """
    pids: set[int] = set()
    pattern = re.compile(r"\b(sensor_collector\.sh)\b")
    for line in _ps_output().splitlines():
        if pattern.search(line):
            # The line format from ps -eo pid,comm,args starts with PID
            pid_str = line.split(None, 1)[0]
            if pid_str.isdigit():
                pids.add(int(pid_str))
    return pids


@pytest.mark.parametrize(
    "path_obj,desc",
    [
        (IOT_DIR, "directory /home/user/iot_edge"),
        (SCRIPT_PATH, "script /home/user/iot_edge/sensor_collector.sh"),
        (DATA_LOG, "log file /home/user/iot_edge/data.log"),
        (PID_FILE, "PID file /home/user/iot_edge/collector.pid"),
        (PROCESS_LOG, "process log /home/user/iot_edge/process_log.txt"),
    ],
)
def test_paths_do_not_exist_yet(path_obj: Path, desc: str):
    """
    Assert that none of the deliverable paths exist before the student
    has started.  Ensures a clean slate.
    """
    assert not path_obj.exists(), (
        f"Expected {desc} to be absent before task start, "
        f"but it already exists at {path_obj}."
    )


def test_no_sensor_collector_process_running():
    """
    The workload must not be running at the initial state.
    We parse the system's process table for anything that looks like
    'sensor_collector.sh'.
    """
    pids = _collector_pids_from_ps()
    assert (
        not pids
    ), f"Found unexpected running sensor_collector.sh process(es) with PID(s): {sorted(pids)}. " \
       "The environment should start with no such process running."


def test_directory_parent_exists():
    """
    Sanity-check that the parent directory /home/user exists so that
    students can create /home/user/iot_edge without path issues.
    """
    parent = Path("/home/user")
    assert parent.is_dir(), (
        "/home/user must exist on the test system; it is the designated "
        "home directory where the student will create /home/user/iot_edge."
    )