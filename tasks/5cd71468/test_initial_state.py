# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the sandbox **before**
# the student performs any actions required by the task.
#
# Preconditions we enforce:
#   1. The target rule file /home/user/firewall/mock_rules.conf must NOT
#      exist yet.  The student is expected to create (or overwrite) it.
#   2. If the parent path /home/user/firewall does exist, it must be a
#      directory (not a regular file).  It is acceptable for the directory
#      to be absent at this stage; creating it is part of the assignment.
#
# These checks ensure that:
#   • The environment is clean (no “pre-baked” correct answers).
#   • The student can safely create/overwrite the required files without
#     running into unexpected filesystem states.

import pathlib
import os


RULE_DIR = pathlib.Path("/home/user/firewall")
RULE_FILE = RULE_DIR / "mock_rules.conf"


def test_firewall_directory_is_absent_or_directory():
    """
    The path /home/user/firewall should *either* not exist yet, or exist
    as a directory.  It must not be a regular file, symlink to a file,
    or any other non-directory entity that would block `mkdir -p`.
    """
    if RULE_DIR.exists():
        # If the path exists, ensure it is a directory.
        assert RULE_DIR.is_dir(), (
            f"{RULE_DIR} exists but is not a directory. "
            "Please remove or rename it before running the task."
        )
    # If the path does not exist, that is acceptable — the student will create it.


def test_mock_rules_file_must_not_exist_yet():
    """
    The rule file should not exist before the student writes it.
    A pre-existing file would either give away the correct content or
    interfere with the single-command overwrite requirement.
    """
    assert not RULE_FILE.exists(), (
        f"The file {RULE_FILE} already exists, but the task requires the "
        "student to create (or overwrite) it in one command. "
        "Remove the file before starting the task."
    )