# test_initial_state.py
#
# This pytest file verifies that the operating-system state is **clean**
# before the student executes any commands for the “cron file” exercise.
#
# Expectations *before* the task is attempted:
#
# 1. The home directory “/home/user” must already exist (otherwise the entire
#    exercise environment is broken).
# 2. The target directory “/home/user/docs” must **not** exist yet.
# 3. Consequently, the file “/home/user/docs/doc_build.cron” must also
#    **not** exist.
#
# These checks guarantee that the student starts from a known baseline and
# that any artefacts detected after task execution were indeed created by
# the student’s command(s).

import os
import pytest
from pathlib import Path

HOME_DIR = Path("/home/user")
DOCS_DIR = HOME_DIR / "docs"
CRON_FILE = DOCS_DIR / "doc_build.cron"


def test_home_directory_exists():
    """The baseline /home/user directory must be present."""
    assert HOME_DIR.exists(), (
        f"Expected base directory {HOME_DIR} to exist, "
        "but it is missing. The exercise environment is not correctly set up."
    )
    assert HOME_DIR.is_dir(), f"{HOME_DIR} exists but is not a directory."


@pytest.mark.order(after="test_home_directory_exists")
def test_docs_directory_absent_before_task():
    """
    The /home/user/docs directory should NOT exist before the student runs
    their compound shell command. Its presence would indicate that the
    environment is dirty or that a previous attempt has polluted the state.
    """
    assert not DOCS_DIR.exists(), (
        f"Pre-existing directory {DOCS_DIR} found. The environment must be "
        "clean before the student starts the task."
    )


@pytest.mark.order(after="test_docs_directory_absent_before_task")
def test_cron_file_absent_before_task():
    """
    The cron file must not be present yet; it should only appear after the
    student completes the task. Finding the file now would invalidate the
    setup.
    """
    assert not CRON_FILE.exists(), (
        f"Unexpected file {CRON_FILE} exists before task execution. "
        "Please reset the environment so the student can create it."
    )