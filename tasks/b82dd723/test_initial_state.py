# test_initial_state.py
# This test-suite validates the *initial* state of the operating system
# before the student performs any action for the “vulnerability-scanning
# workspace” exercise.

import os
from pathlib import Path

HOME_DIR = Path("/home/user")
WORKSPACE_DIR = HOME_DIR / "vuln_scans"
CONF_FILE = WORKSPACE_DIR / "default_scan.conf"


def test_home_directory_exists():
    """Sanity-check that the base home directory is present."""
    assert HOME_DIR.is_dir(), (
        "Expected the base directory /home/user to exist. "
        "The testing environment itself is malformed."
    )


def test_workspace_directory_absent():
    """
    The /home/user/vuln_scans directory should *not* exist yet.
    Students will create it with a single command.
    """
    assert not WORKSPACE_DIR.exists(), (
        "The directory /home/user/vuln_scans is already present. "
        "The workspace must be created by the student; "
        "please reset the environment so the directory is absent."
    )


def test_config_file_absent():
    """
    The configuration file must not exist prior to the student's action.
    It will be created inside /home/user/vuln_scans by the student's command.
    """
    assert not CONF_FILE.exists(), (
        "The file /home/user/vuln_scans/default_scan.conf already exists. "
        "The initial state should be clean; remove the file before testing."
    )