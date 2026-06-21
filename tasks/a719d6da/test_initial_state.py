# test_initial_state.py
#
# This test-suite verifies that the system starts in a “clean” state
# before the student completes the assignment.  Specifically, we check
# that the diagnostic log file **does not yet exist**.  The assignment
# instructs the student to create—and if necessary overwrite—this file,
# so a pre-existing file would invalidate the starting conditions.

import os
import pytest


SYS_REPORT_PATH = "/home/user/monitoring/sys_report.log"


def test_sys_report_log_absent_before_student_action():
    """
    The sys_report.log file should NOT exist prior to the student's work.
    If it already exists the student cannot demonstrate that they created
    (or overwrote) it during the exercise.

    We do *not* place any requirement on the parent directory; the
    assignment explicitly states that it may or may not be present.
    """
    assert not os.path.exists(
        SYS_REPORT_PATH
    ), (
        f"Precondition failure:\n"
        f"The file {SYS_REPORT_PATH} already exists. "
        f"The assignment requires the student to create (or overwrite) this "
        f"file as part of their solution, so it must be absent at the start."
    )