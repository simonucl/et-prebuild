# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem
# is in the expected **clean** state *before* the student starts
# working on the “monitoring-platform” exercise.  Nothing created
# by the checklist should exist yet.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user").expanduser()
BASE_DIR = HOME / "sys_monitoring"
ALERTS_DIR = BASE_DIR / "alerts"
THRESHOLDS = BASE_DIR / "thresholds.conf"
MONITOR_SCRIPT = BASE_DIR / "monitor_demo.sh"
ALERT_LOG = ALERTS_DIR / "alert.log"


def assert_not_exists(path: Path):
    """
    Helper that asserts the given path does NOT exist and provides
    a helpful, explicit failure message if it does.
    """
    assert not path.exists(), f"{path} should NOT exist before the student starts the task."


def test_home_directory_is_present():
    """
    Sanity-check: the non-privileged user’s home directory must exist.
    Everything else will be created by the student inside this folder.
    """
    assert HOME.exists(), f"Expected home directory {HOME} to exist."
    assert HOME.is_dir(),  f"Expected {HOME} to be a directory."


def test_sys_monitoring_tree_is_absent():
    """
    The /home/user/sys_monitoring directory tree must NOT exist yet.
    """
    assert_not_exists(BASE_DIR)


def test_alerts_directory_is_absent():
    """
    The alerts sub-directory must NOT exist before the task.
    """
    assert_not_exists(ALERTS_DIR)


def test_thresholds_conf_is_absent():
    """
    The thresholds.conf file must NOT exist before the task.
    """
    assert_not_exists(THRESHOLDS)


def test_monitor_script_is_absent():
    """
    The demo monitoring script must NOT exist before the task.
    """
    assert_not_exists(MONITOR_SCRIPT)


def test_alert_log_is_absent():
    """
    The alert.log file must NOT exist before the task.
    """
    assert_not_exists(ALERT_LOG)