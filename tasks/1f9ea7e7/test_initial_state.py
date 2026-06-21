# test_initial_state.py
#
# Pytest suite that verifies the filesystem is in its expected
# "clean slate" prior to the student executing their one-liner.
# The task requirements explicitly state that the directory
# /home/user/benchmarks and the file /home/user/benchmarks/loadavg.log
# do NOT exist before the solution is run.  These tests confirm that.

from pathlib import Path

BENCHMARKS_DIR = Path("/home/user/benchmarks")
LOADAVG_LOG = BENCHMARKS_DIR / "loadavg.log"


def test_benchmarks_directory_absent():
    """
    The /home/user/benchmarks directory must NOT exist before the
    student's command is executed.  Its creation is part of the task.
    """
    assert not BENCHMARKS_DIR.exists(), (
        f"The directory {BENCHMARKS_DIR} should not exist before "
        "running the student's command, but it does."
    )


def test_loadavg_log_absent():
    """
    The log file must also be absent prior to execution.
    Even if someone created /home/user/benchmarks manually,
    the specific log file must not pre-exist.
    """
    assert not LOADAVG_LOG.exists(), (
        f"The file {LOADAVG_LOG} should not exist before "
        "running the student's command, but it does."
    )