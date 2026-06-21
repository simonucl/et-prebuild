# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / filesystem
# state *before* the student performs any actions for the “temperature-sensor”
# edge-computing task.  Everything that the final grader will later require is
# expected to be ABSENT at this stage.
#
# If any of these tests fail it means the workspace is “dirty” (left-overs from
# a previous run, or the student has already started working) and must be
# cleaned before the real assessment can begin.

import os
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants – absolute paths that the FINAL solution will have to create.
# At the *initial* state they must be missing.
# ---------------------------------------------------------------------------
BASE_DIR = "/home/user/iot_edge"
SENSOR_DIR = f"{BASE_DIR}/sensor_collector"
LOG_DIR = f"{SENSOR_DIR}/logs"
SCRIPT_FILE = f"{SENSOR_DIR}/sensor_collector.py"
SUPERVISOR_DIR = f"{BASE_DIR}/supervisor"
SUPERVISOR_FILE = f"{SUPERVISOR_DIR}/sensor_collector.conf"
REPORT_FILE = f"{BASE_DIR}/deployment_report.log"
PIPE_PATH = "/tmp/sensor_pipe"

# All paths that must NOT exist yet.
ALL_EXPECTED_PATHS = [
    BASE_DIR,
    SENSOR_DIR,
    LOG_DIR,
    SCRIPT_FILE,
    SUPERVISOR_DIR,
    SUPERVISOR_FILE,
    REPORT_FILE,
    PIPE_PATH,
]

# ---------------------------------------------------------------------------


@pytest.mark.parametrize("abs_path", ALL_EXPECTED_PATHS)
def test_expected_paths_absent(abs_path):
    """
    Ensure that none of the files, directories, or FIFOs required for the final
    submission are present yet.  A presence now would indicate that either
    the student has already started working or a previous run polluted the
    workspace, which would invalidate the 'initial state' expectation.
    """
    assert not os.path.lexists(
        abs_path
    ), (
        f"The path {abs_path!r} already exists, but the initial state must be "
        "clean.  Remove it before beginning the task."
    )


def test_sensor_pipe_not_a_fifo():
    """
    Extra guard: if /tmp/sensor_pipe *does* exist (the previous test would
    already fail), ensure it is NOT a FIFO.  This provides a clearer error
    message in such a case.
    """
    if os.path.lexists(PIPE_PATH):
        mode = os.stat(PIPE_PATH).st_mode
        is_fifo = stat.S_ISFIFO(mode)
        assert (
            not is_fifo
        ), "/tmp/sensor_pipe is unexpectedly a FIFO—initial state must not include it."