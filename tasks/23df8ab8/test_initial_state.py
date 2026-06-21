# test_initial_state.py
#
# This test-suite validates that the operating-system is still in the
# pristine “before the student starts” state.  According to the task
# description, **nothing related to the monitoring service should be
# present yet**.  In particular, the directory `/home/user/monitoring`
# (and therefore any files it would contain) must not exist.
#
# If any part of the monitoring hierarchy already exists, the tests will
# fail with a descriptive message so the student immediately knows what
# needs to be removed or cleaned up before proceeding.

import os
import stat
import pytest

MONITORING_DIR = "/home/user/monitoring"
FILES_THAT_MUST_NOT_EXIST = [
    f"{MONITORING_DIR}/targets.txt",
    f"{MONITORING_DIR}/uptime_monitor.sh",
    f"{MONITORING_DIR}/run_once.sh",
    f"{MONITORING_DIR}/uptime.log",
]

@pytest.mark.describe("Initial filesystem state")
class TestInitialState:
    def test_monitoring_directory_absent(self):
        """
        The /home/user/monitoring directory must NOT exist before the
        student begins the task.
        """
        assert not os.path.exists(MONITORING_DIR), (
            f"The directory {MONITORING_DIR} already exists, "
            "but the task specifies that the student must create it.")

    @pytest.mark.parametrize("path", FILES_THAT_MUST_NOT_EXIST)
    def test_individual_files_absent(self, path):
        """
        Ensure none of the expected target files are prematurely present.
        """
        assert not os.path.exists(path), (
            f"Found unexpected pre-existing file or directory: {path}. "
            "The initial state must be completely empty so the student "
            "can create everything from scratch.")