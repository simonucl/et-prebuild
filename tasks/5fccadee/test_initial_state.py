# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student implements the solution for the
# “artifact-manager” systemd-timer exercise.
#
# These tests guarantee that the grading environment is clean: nothing from
# the final solution is allowed to be present yet, while the source-data
# location (/home/user/artifacts) must already exist.  If any of the checks
# in this file fails, the base image is polluted and later “post-solution”
# tests could yield false positives or negatives.
#
# NOTE:
# – Only the Python standard library and pytest are used.
# – Each failure message is explicit about what should *not* (or should)
#   be present initially.

import os
import stat
import subprocess
from pathlib import Path

HOME = Path("/home/user")

# ---------- paths that MUST exist beforehand ----------
ARTIFACTS_DIR = HOME / "artifacts"  # the directory that is to be cleaned

# ---------- paths that MUST NOT exist beforehand ----------
BIN_SCRIPT          = HOME / "bin" / "cleanup_artifacts.sh"
SERVICE_UNIT        = HOME / ".config" / "systemd" / "user" / "artifact-cleanup.service"
TIMER_UNIT          = HOME / ".config" / "systemd" / "user" / "artifact-cleanup.timer"
TIMER_WANTS_SYMLINK = (
    HOME
    / ".config"
    / "systemd"
    / "user"
    / "timers.target.wants"
    / "artifact-cleanup.timer"
)
LOG_DIR             = HOME / "artifact-cleanup"
LOG_FILE            = LOG_DIR / "validation.log"

###############################################
# Tests for the initial *clean* environment.  #
###############################################

def test_artifacts_directory_exists_and_is_directory():
    """
    The source directory with the actual artifacts must already be present
    so that the student can create *.tmp files there for testing.

    If this directory is missing, neither the task description nor the
    final-state tests make sense.
    """
    assert ARTIFACTS_DIR.exists(), f"Required directory '{ARTIFACTS_DIR}' is missing."
    assert ARTIFACTS_DIR.is_dir(), f"'{ARTIFACTS_DIR}' exists but is not a directory."


def test_cleanup_script_is_absent_initially():
    assert not BIN_SCRIPT.exists(), (
        f"Pre-existing cleanup script found at '{BIN_SCRIPT}'. "
        "Environment must be clean before student starts."
    )


def test_service_unit_is_absent_initially():
    assert not SERVICE_UNIT.exists(), (
        f"Pre-existing systemd service unit found at '{SERVICE_UNIT}'. "
        "This should not exist before the student creates it."
    )


def test_timer_unit_is_absent_initially():
    assert not TIMER_UNIT.exists(), (
        f"Pre-existing systemd timer unit found at '{TIMER_UNIT}'. "
        "This should not exist before the student creates it."
    )


def test_timer_symlink_is_absent_initially():
    assert not TIMER_WANTS_SYMLINK.exists(), (
        f"Pre-existing symlink found at '{TIMER_WANTS_SYMLINK}'. "
        "The timer must not be enabled yet."
    )


def test_log_directory_is_absent_initially():
    assert not LOG_DIR.exists(), (
        f"Pre-existing log directory '{LOG_DIR}' detected. "
        "It should be created by the student's solution."
    )


def test_validation_log_is_absent_initially():
    assert not LOG_FILE.exists(), (
        f"Pre-existing validation log '{LOG_FILE}' detected. "
        "It should be created by the student's solution."
    )


def test_no_crontab_entry_for_cleanup_script():
    """
    The task explicitly forbids using cron.  Make sure no legacy crontab
    entry referencing the script is present.
    """
    try:
        completed = subprocess.run(
            ["crontab", "-l"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        # crontab binary not present in minimal containers – that's fine
        return

    # When there is no crontab, `crontab -l` typically exits with code 1 _and_
    # prints nothing to stdout, but we still examine stdout just in case.
    stdout = completed.stdout or ""
    assert "cleanup_artifacts.sh" not in stdout, (
        "User crontab already contains a reference to 'cleanup_artifacts.sh'. "
        "Cron must NOT be used for this exercise."
    )