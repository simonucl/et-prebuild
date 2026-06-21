# test_initial_state.py
#
# This test-suite verifies the **initial** operating-system / filesystem
# state before the student carries out any of the steps described in the
# assignment.  It purposefully checks only for pre-existing conditions
# and explicitly confirms that the target artefact files are **absent**
# at this point.
#
# Requirements being validated:
#
# 1. The base directory /home/user/firewall_config **must already exist**.
# 2. Neither of the files that the assignment asks the student to create
#    should be present yet:
#       • /home/user/firewall_config/iptables.rules
#       • /home/user/firewall_config/changes.log
#
# If any of these conditions are not met, the failure message will
# explain exactly what is wrong so the learner can correct the setup
# before proceeding.
#
# NOTE:  Do not add any third-party dependencies—stdlib + pytest only.

import os
from pathlib import Path

BASE_DIR = Path("/home/user/firewall_config")
IPTABLES_RULES = BASE_DIR / "iptables.rules"
CHANGE_LOG = BASE_DIR / "changes.log"


def test_base_directory_exists():
    """
    The directory /home/user/firewall_config must be present *before*
    the learner starts creating files inside it.
    """
    assert BASE_DIR.exists(), (
        f"Expected directory {BASE_DIR} to exist, but it is missing. "
        "Create the directory first (mkdir -p /home/user/firewall_config) "
        "before adding any files."
    )
    assert BASE_DIR.is_dir(), (
        f"The path {BASE_DIR} exists but is not a directory. "
        "Remove or rename the existing path and create a directory "
        "with that name."
    )


def test_no_iptables_rules_yet():
    """
    The iptables.rules file should *not* exist at the beginning.
    It will be created by the learner as part of the assignment.
    """
    assert not IPTABLES_RULES.exists(), (
        f"The file {IPTABLES_RULES} already exists, but it should not be "
        "present prior to running the task.  Remove it so the exercise "
        "starts from a clean state."
    )


def test_no_change_log_yet():
    """
    The changes.log file should *not* exist at the beginning.
    It will be produced during the exercise.
    """
    assert not CHANGE_LOG.exists(), (
        f"The file {CHANGE_LOG} already exists, but it should not be "
        "present prior to running the task.  Remove it so the exercise "
        "starts from a clean state."
    )