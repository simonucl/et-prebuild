# test_initial_state.py
#
# This test-suite validates that the environment is *clean* before
# the student runs their one-liner.  In particular, none of the
# artefacts that the exercise asks the student to create should be
# present yet.  If any of them are already present, the exercise would
# be meaningless or could yield a false positive later on.

import os
import stat
import pytest

HOME = "/home/user"
SCRIPTS_DIR = os.path.join(HOME, "scripts")
SCRIPT_FILE = os.path.join(SCRIPTS_DIR, "archive_cleanup.sh")
LOG_FILE = os.path.join(HOME, "scripts_creation.log")


def _describe_mode(mode: int) -> str:
    """Return a human-readable string representation of a file mode."""
    perms = stat.filemode(mode)
    return f"{mode:o} ({perms})"


def test_scripts_directory_absent_or_directory():
    """
    /home/user/scripts should **not** contain the target file yet.
    The directory itself may or may not exist; if it does, it must
    indeed be a directory (not a file, symlink, etc.).
    """
    if os.path.exists(SCRIPTS_DIR):
        assert os.path.isdir(
            SCRIPTS_DIR
        ), f"{SCRIPTS_DIR} exists but is not a directory."
        # The directory exists already; that is OK, but it must not yet
        # contain the target script.
        assert not os.path.exists(
            SCRIPT_FILE
        ), f"Unexpected: {SCRIPT_FILE} already exists before the student command is run."
    else:
        # Directory is absent – also perfectly fine at this point.
        assert not os.path.exists(
            SCRIPT_FILE
        ), (
            f"Inconsistent state: {SCRIPT_FILE} exists even though its parent "
            f"directory {SCRIPTS_DIR} is missing."
        )


def test_target_script_does_not_exist():
    """
    The placeholder script file must not exist yet.  It will be created
    by the student's one-liner.
    """
    assert not os.path.exists(
        SCRIPT_FILE
    ), f"{SCRIPT_FILE} should not exist before the student performs the task."


def test_log_file_does_not_exist():
    """
    The confirmation log must not exist yet; it is produced by the
    student's command.
    """
    assert not os.path.exists(
        LOG_FILE
    ), f"{LOG_FILE} should not exist before the student performs the task."