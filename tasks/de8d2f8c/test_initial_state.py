# test_initial_state.py
#
# This test-suite is executed *before* the learner starts the exercise.
# It confirms that the working environment is clean, i.e. the target
# logfile does **not** yet exist.  This prevents a situation where
# leftover artifacts from a previous run cause the assessment to pass
# or fail incorrectly.

import os
from pathlib import Path

# Absolute paths used throughout the tasks
LOG_DIR  = Path("/home/user/logs")
LOG_FILE = LOG_DIR / "system_diag.log"


def test_log_file_does_not_exist():
    """
    The diagnostic file must NOT exist before the student performs any action.

    If this test fails, delete the file (and optionally the directory) so
    that the exercise starts from a known, clean slate.
    """
    assert not LOG_FILE.exists(), (
        f"Pre-condition failed: {LOG_FILE} already exists. "
        "Remove this file before starting the task."
    )


def test_log_directory_is_clean():
    """
    The logs directory may or may not exist yet.

    • If it exists, it must be a directory (not a file or symlink).
    • The target file must not already be present inside it.
    """
    if LOG_DIR.exists():
        # Ensure /home/user/logs is actually a directory
        assert LOG_DIR.is_dir(), (
            f"Pre-condition failed: {LOG_DIR} exists but is not a directory."
        )
        # Ensure system_diag.log is not present
        unexpected = LOG_DIR / "system_diag.log"
        assert not unexpected.exists(), (
            f"Pre-condition failed: {unexpected} already exists inside {LOG_DIR}. "
            "Remove it before starting the task."
        )