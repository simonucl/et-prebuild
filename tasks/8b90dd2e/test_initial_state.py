# test_initial_state.py
"""
Pytest suite verifying that the system starts in a clean state
BEFORE the student creates the required monitoring configuration.

If any of these tests fail, the environment is already “dirty” and
the student will not be able to demonstrate their work from scratch.
"""

import os
from pathlib import Path

MONITOR_DIR = Path("/home/user/monitor")
CONF_DIR = MONITOR_DIR / "conf"
ALERTS_CONF = CONF_DIR / "alerts.conf"
SETUP_LOG = MONITOR_DIR / "setup.log"


def _assert_not_exists(path: Path):
    """
    Helper that fails with a clear message when `path` already exists.
    """
    assert not path.exists(), (
        f"Found pre-existing path: {path!s}\n"
        "The environment must be clean before the student begins; "
        "no monitor configuration artifacts should exist yet."
    )


def test_monitor_directory_is_absent_or_empty():
    """
    `/home/user/monitor` must either not exist at all or, if it exists
    (perhaps created by other coursework), it must NOT already contain
    the `conf` sub-directory or the `setup.log` file.
    """
    if not MONITOR_DIR.exists():
        # Ideal case: nothing exists yet.
        return

    # The directory exists; ensure it does NOT yet contain the required artifacts.
    _assert_not_exists(CONF_DIR)
    _assert_not_exists(SETUP_LOG)


def test_conf_directory_absent():
    """
    The required configuration directory should not pre-exist.
    """
    _assert_not_exists(CONF_DIR)


def test_alerts_conf_absent():
    """
    The alerts configuration file must not exist prior to the student's work.
    """
    _assert_not_exists(ALERTS_CONF)


def test_setup_log_absent():
    """
    The setup confirmation log must not exist prior to the student's work.
    """
    _assert_not_exists(SETUP_LOG)