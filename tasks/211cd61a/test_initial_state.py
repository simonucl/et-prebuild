# test_initial_state.py
#
# This pytest file validates the *initial* state of the OS before the student
# completes the “CPU-intensive process snapshot” task.  At this stage, the
# incident-response artifacts must **not** exist yet.  The existence of any of
# these artifacts would indicate that the environment is already “solved”, which
# is an invalid starting point for the exercise.

import os
import stat
import pytest

HOME = "/home/user"
IR_DIR = os.path.join(HOME, "ir_logs")
TOP_CPU_LOG = os.path.join(IR_DIR, "top_cpu.log")


def _path_readable(path):
    """
    Helper that returns True if the current user has read permission on `path`.
    """
    return os.access(path, os.R_OK)


@pytest.mark.describe("Initial environment sanity checks")
class TestInitialState:
    def test_ir_logs_directory_absent(self):
        """
        The directory /home/user/ir_logs must NOT exist prior to the student's
        intervention.  Its presence would imply the exercise has already been
        tackled.
        """
        # It should neither exist as a directory nor a file/symlink/etc.
        assert not os.path.exists(IR_DIR), (
            f"The directory {IR_DIR!r} already exists. "
            "Initial state must be clean—no 'ir_logs' directory should be present."
        )

    def test_top_cpu_log_absent(self):
        """
        The output file /home/user/ir_logs/top_cpu.log must NOT exist yet.
        """
        assert not os.path.exists(TOP_CPU_LOG), (
            f"The file {TOP_CPU_LOG!r} already exists. "
            "Initial state must be clean—no prior log file should be present."
        )

    def test_home_is_readable(self):
        """
        Sanity-check that /home/user itself is intact and readable; this avoids
        false negatives caused by a broken test environment.
        """
        assert os.path.isdir(HOME), (
            f"Expected {HOME!r} to be a directory, but it is missing or not a dir."
        )
        assert _path_readable(HOME), (
            f"{HOME!r} is not readable by the current user—cannot continue tests."
        )