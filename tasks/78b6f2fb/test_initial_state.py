# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system
# before the student has taken any action.  It confirms that the working
# environment is clean and ready for the assignment.
#
# Requirements checked:
#   1. The home directory /home/user exists and is a directory.
#   2. The target output file /home/user/firewall_rule_8443.txt is NOT
#      present yet.  Its presence would indicate that a previous run or a
#      mis-configured image has already created the file, which would
#      invalidate the exercise.

import os
from pathlib import Path

HOME_DIR = Path("/home/user")
OUTPUT_FILE = HOME_DIR / "firewall_rule_8443.txt"


def test_home_directory_exists():
    """
    The base working directory must exist so the student has somewhere to
    create the output file.  If it is missing or is not a directory, the
    environment is broken.
    """
    assert HOME_DIR.exists(), (
        f"The required home directory {HOME_DIR} does not exist. "
        "The exercise environment is not correctly provisioned."
    )
    assert HOME_DIR.is_dir(), (
        f"The path {HOME_DIR} exists but is not a directory. "
        "Expected a directory for the user's home."
    )


def test_firewall_rule_file_is_absent():
    """
    Before the student performs the task, the file that they are supposed
    to create **must not** be present.  A pre-existing file would make the
    assignment trivial and would hide potential permission issues.
    """
    assert not OUTPUT_FILE.exists(), (
        f"The file {OUTPUT_FILE} already exists. "
        "The environment should be clean before the student starts; "
        "remove this file so the student can create it as part of the task."
    )