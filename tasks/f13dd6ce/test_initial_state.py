# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student performs any action for the “weekday docs build”
# task.  These tests guarantee that the starting environment is clean and ready
# for the student-authored changes.
#
# Rules enforced:
#   • No expected output artifacts (cron job or crontab snapshot file) should
#     exist yet.
#   • Required pre-existing resources (directories, scripts, log file) must be
#     present and accessible.
#   • The user crontab must **not** already contain the target job line.
#
# Only Python’s standard library and pytest are used.

import os
import pwd
import stat
import subprocess
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
SCRIPT_DIR = HOME / "scripts"
BUILD_SCRIPT = SCRIPT_DIR / "build_docs.sh"
BUILD_LOG = LOG_DIR / "build_docs.log"
CRONTAB_SNAPSHOT = LOG_DIR / "crontab_after_task.txt"

CRON_LINE = (
    "30 09 * * 1-5 /home/user/scripts/build_docs.sh >> "
    "/home/user/logs/build_docs.log 2>&1"
)


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _current_uid_gid():
    """Return (uid, gid) of the effective user running the tests."""
    return os.geteuid(), os.getegid()


def _can_write(path: Path) -> bool:
    """Return True iff the current user can create a file inside `path`."""
    uid, gid = _current_uid_gid()
    st = path.stat()
    mode = st.st_mode

    # Owner perms
    if uid == st.st_uid and (mode & stat.S_IWUSR):
        return True
    # Group perms
    if gid == st.st_gid and (mode & stat.S_IWGRP):
        return True
    # Other perms
    if mode & stat.S_IWOTH:
        return True
    return False


def _read_user_crontab() -> str:
    """
    Return the string contents of the current user’s crontab.
    If the user has no crontab, returns an empty string.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        text=True,
        capture_output=True,
        check=False,
    )

    # A non-zero exit status with the well-known phrase means “no crontab”.
    if proc.returncode != 0:
        return ""
    return proc.stdout.rstrip("\n")  # strip trailing newline for easier compare


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_logs_directory_exists_and_writable():
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} is missing or not a directory."
    )
    assert _can_write(LOG_DIR), (
        f"Current user lacks write permission on {LOG_DIR}."
    )


def test_build_script_exists_and_is_executable():
    assert BUILD_SCRIPT.is_file(), (
        f"Required script {BUILD_SCRIPT} is missing."
    )
    assert os.access(BUILD_SCRIPT, os.X_OK), (
        f"Script {BUILD_SCRIPT} exists but is not executable."
    )


def test_build_log_file_exists_and_is_writable():
    assert BUILD_LOG.is_file(), (
        f"Existing log file {BUILD_LOG} is missing."
    )
    assert os.access(BUILD_LOG, os.W_OK), (
        f"Log file {BUILD_LOG} exists but is not writable by the current user."
    )


def test_crontab_does_not_already_contain_target_job():
    crontab_contents = _read_user_crontab().splitlines()
    matches = [line for line in crontab_contents if line.strip() == CRON_LINE]

    assert (
        len(matches) == 0
    ), (
        "User crontab already contains the target cron job. "
        "Initial state should be clean; remove existing entry before starting."
    )


def test_crontab_snapshot_file_not_present_yet():
    assert not CRONTAB_SNAPSHOT.exists(), (
        f"Snapshot file {CRONTAB_SNAPSHOT} already exists. "
        "It must be created only after the task is completed."
    )