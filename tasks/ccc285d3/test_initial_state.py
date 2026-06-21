# test_initial_state.py
#
# This pytest suite validates that the operating-system state is **clean**
# before the student starts the assignment.  In particular, it checks that
# the student has NOT already created any of the resources that the task
# later requires (/home/user/migration_baseline and the accompanying log
# file).  A failure here means the environment is in the wrong state *before*
# the student’s solution runs.

import os
from pathlib import Path
import pytest

HOME_DIR = Path("/home/user")
BASELINE_DIR = HOME_DIR / "migration_baseline"
LOG_FILE = BASELINE_DIR / "latest_metrics.log"


def test_home_directory_exists():
    """
    Sanity-check that the base home directory for the exercise is present.
    If this fails, the container / test runner itself is mis-configured.
    """
    assert HOME_DIR.exists(), (
        f"Expected home directory {HOME_DIR} to exist, "
        "but it is missing. The test runner environment is not configured "
        "correctly."
    )
    assert HOME_DIR.is_dir(), (
        f"Expected {HOME_DIR} to be a directory, "
        "but it is not. The test runner environment is not configured "
        "correctly."
    )


def test_migration_baseline_directory_absent():
    """
    Before the student starts, the directory /home/user/migration_baseline
    must NOT exist.  The exercise requires the student to create it.
    """
    assert not BASELINE_DIR.exists(), (
        f"The directory {BASELINE_DIR} already exists, "
        "but it should NOT be present prior to running the student solution. "
        "Remove it so the task starts from a clean slate."
    )


def test_latest_metrics_log_absent():
    """
    Likewise, the metrics log file must not exist ahead of time; the student
    must create and populate it during their solution.
    """
    assert not LOG_FILE.exists(), (
        f"The file {LOG_FILE} already exists, "
        "but it should NOT be present before the student runs their code. "
        "Ensure a pristine starting state."
    )