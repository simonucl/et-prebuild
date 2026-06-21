# test_initial_state.py
#
# Pytest suite that validates the starting state of the filesystem
# BEFORE the student creates the symbolic link and log file.
#
# Expected initial conditions:
#   1. The directory /home/user/qa_env/bin already exists.
#   2. The path /home/user/tools must NOT exist yet.
#   3. The path /home/user/qa_symlink_setup.log must NOT exist yet.
#
# Only stdlib and pytest are used.

import os
from pathlib import Path
import stat
import pytest

# Constant paths used throughout the tests
QA_ENV_BIN_DIR = Path("/home/user/qa_env/bin")
TOOLS_SYMLINK  = Path("/home/user/tools")
LOG_FILE       = Path("/home/user/qa_symlink_setup.log")

def test_qa_env_bin_directory_exists_and_is_directory():
    """
    The environment should already provide /home/user/qa_env/bin
    as an actual directory.  This is the only pre-existing artefact
    the student relies on.
    """
    assert QA_ENV_BIN_DIR.exists(), (
        f"Missing required directory: {QA_ENV_BIN_DIR}. "
        "It must exist before the task begins."
    )
    # Must be a real directory, not a symlink, file, etc.
    assert QA_ENV_BIN_DIR.is_dir(), (
        f"{QA_ENV_BIN_DIR} exists but is not a directory."
    )

def test_tools_symlink_not_yet_created():
    """
    The symbolic link /home/user/tools must NOT exist before the
    student's solution runs.  Its presence would indicate that the
    workspace is contaminated or that a previous solution leaked state.
    """
    assert not TOOLS_SYMLINK.exists(), (
        f"{TOOLS_SYMLINK} already exists.  "
        "The workspace must start WITHOUT this symlink."
    )

def test_log_file_not_yet_created():
    """
    The log file /home/user/qa_symlink_setup.log must NOT exist before
    the student's solution runs.  It will be created by the student.
    """
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists.  "
        "The workspace must start WITHOUT this log file."
    )