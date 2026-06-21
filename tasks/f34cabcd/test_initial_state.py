# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the system **before**
# the student has carried out any actions required by the assignment.
#
# The assignment asks the student to create
# /home/user/tech_logs/performance_benchmark.log
# and to populate it with specific content.  At this point in time,
# that file (and, possibly, even the parent directory) must **not**
# exist.  If they already exist, the exercise would be meaningless
# or would require the student to overwrite existing artefacts.
#
# These tests therefore assert that:
#   • The parent directory may or may not be present (the spec says
#     to create it "if it does not already exist"), so we do *not*
#     fail if the directory is already there.
#   • The log file itself must **not** exist yet.
#
# Any failure gives a clear explanation so the student or course
# author can reset the environment before the graded portion runs.

import os
import pytest
from pathlib import Path

# Constants
HOME = Path("/home/user")
TECH_LOG_DIR = HOME / "tech_logs"
LOG_FILE = TECH_LOG_DIR / "performance_benchmark.log"


def test_performance_log_not_present_yet():
    """
    The performance benchmark log file must not exist *before* the student
    performs the assignment steps.  Its presence would indicate that the
    environment is already 'solved' or has stale data, which violates the
    clean-slate requirement for this task.
    """
    assert not LOG_FILE.exists(), (
        f"The file {LOG_FILE} already exists. "
        "The exercise expects the student to create this file during their solution, "
        "so it must be absent at the start."
    )

    # The directory may or may not exist—both states are acceptable.
    # However, if the directory *does* exist, ensure that it does not
    # already contain the target log file (covered above) or any other
    # misleading artefacts (e.g., backup files with the same base name).
    if TECH_LOG_DIR.is_dir():
        conflicting = sorted(
            p for p in TECH_LOG_DIR.iterdir()
            if p.name.startswith("performance_benchmark") and p.suffix != ".log"
        )
        assert not conflicting, (
            f"Found unexpected files in {TECH_LOG_DIR}: {conflicting}. "
            "The directory should be clean before the student runs their commands."
        )