# test_initial_state.py
#
# This pytest suite verifies that the *initial* state of the operating system
# is clean: none of the artefacts the assignment asks the student to create
# should exist yet.  If any of them are already present, the test will fail
# with a clear, actionable message.
#
# Paths that must be ABSENT at the outset:
#   • /home/user/monitoring/                (directory)
#   • /home/user/logs/                      (directory)
#   • /home/user/monitoring/services.conf   (file)
#   • /home/user/monitoring/monitor.sh      (file, executable)
#   • /home/user/logs/uptime.log            (file)
#
# Only the Python standard library and pytest are used, in accordance with
# the grading system constraints.

import os
import stat
import pytest

HOME = "/home/user"
MONITORING_DIR = os.path.join(HOME, "monitoring")
LOGS_DIR = os.path.join(HOME, "logs")
SERVICES_FILE = os.path.join(MONITORING_DIR, "services.conf")
MONITOR_SCRIPT = os.path.join(MONITORING_DIR, "monitor.sh")
UPTIME_LOG = os.path.join(LOGS_DIR, "uptime.log")


@pytest.mark.parametrize(
    "path, path_type",
    [
        (MONITORING_DIR, "directory"),
        (LOGS_DIR, "directory"),
        (SERVICES_FILE, "file"),
        (MONITOR_SCRIPT, "file"),
        (UPTIME_LOG, "file"),
    ],
)
def test_required_paths_do_not_exist_yet(path: str, path_type: str) -> None:
    """
    Ensure that none of the required artefacts are present before the student
    starts working.  A pre-existing path could indicate that either the VM
    image is tainted or that a previous run failed to clean up.
    """
    assert not os.path.exists(
        path
    ), f"The {path_type} {path!r} already exists but should not be present " \
       f"before the student creates it."


def test_no_residual_executable_bits() -> None:
    """
    A sanity check that *even if* /home/user/monitoring/monitor.sh happens to
    exist (e.g. from a mis-packaged environment), it is not already marked as
    executable.  If the file does not exist, the test is skipped rather than
    failed—absence is already covered in test_required_paths_do_not_exist_yet.
    """
    if not os.path.exists(MONITOR_SCRIPT):
        pytest.skip("monitor.sh does not exist; executable-bit check skipped.")

    st_mode = os.stat(MONITOR_SCRIPT).st_mode
    is_executable = bool(st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert not is_executable, (
        f"{MONITOR_SCRIPT!r} is unexpectedly executable; it should not be "
        f"until the student sets the correct permissions."
    )