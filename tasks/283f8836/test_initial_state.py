# test_initial_state.py
#
# This pytest suite verifies that the starting state of the operating system
# is clean: none of the artefacts required by the monitoring task are present
# yet.  If any of these tests fail it means the environment is *not* in the
# expected pristine condition that students are supposed to start from.

import os
from pathlib import Path

MONITORING_DIR = Path("/home/user/monitoring")
TARGETS_FILE = MONITORING_DIR / "targets.txt"
CHECK_SCRIPT = MONITORING_DIR / "check_targets.sh"
ALERTS_LOG = MONITORING_DIR / "alerts.log"


def test_home_directory_exists():
    """Sanity-check that /home/user itself exists."""
    home = Path("/home/user")
    assert home.is_dir(), "/home/user is expected to exist on the host."


def test_monitoring_directory_absent():
    """
    The /home/user/monitoring directory must NOT exist yet.
    Students are supposed to create it themselves.
    """
    assert not MONITORING_DIR.exists(), (
        f"Found unexpected directory {MONITORING_DIR}. The environment is "
        f"expected to be clean before the student starts."
    )


def test_targets_file_absent():
    """
    targets.txt must NOT exist yet.
    """
    assert not TARGETS_FILE.exists(), (
        f"Found unexpected file {TARGETS_FILE}. The student has not created "
        f"any artefacts yet, so this file should be absent."
    )


def test_check_script_absent():
    """
    check_targets.sh must NOT exist yet.
    """
    assert not CHECK_SCRIPT.exists(), (
        f"Found unexpected script {CHECK_SCRIPT}. The student should create "
        f"this script during the exercise; it must not be present beforehand."
    )


def test_alerts_log_absent():
    """
    alerts.log must NOT exist yet.
    """
    assert not ALERTS_LOG.exists(), (
        f"Found unexpected file {ALERTS_LOG}. alerts.log should be generated "
        f"only after the student's script runs for the first time."
    )