# test_initial_state.py
#
# Pytest suite that validates the machine state *before* the student
# performs any action for the “daily compressed backup” exercise.
#
# The initial, **required** conditions are:
#
#   • Directories
#       /home/user/datasets/
#       /home/user/datasets/raw/
#       /home/user/datasets/backups/
#     must already exist and be mode 755.
#
#   • No cron job for the backup task must be present yet.
#
#   • The file /home/user/cron_verify.log must NOT exist.
#
# If any of these conditions are not met, the tests fail with a clear
# explanation, letting the learner (or course maintainer) know that the
# starting environment is wrong.

import os
import stat
import subprocess
import pytest
from pathlib import Path

HOME = Path("/home/user")
DATASETS_DIR      = HOME / "datasets"
RAW_DIR           = DATASETS_DIR / "raw"
BACKUPS_DIR       = DATASETS_DIR / "backups"
CRON_VERIFY_FILE  = HOME / "cron_verify.log"

# The exact cron line that *should NOT* exist yet
CRON_LINE = (
    "30 2 * * * tar -czf /home/user/datasets/backups/"
    "raw_daily_$(date +\\%Y\\%m\\%d).tar.gz "
    "/home/user/datasets/raw >> /home/user/backup.log 2>&1"
)

@pytest.mark.parametrize(
    "path_obj, description",
    [
        (DATASETS_DIR, "datasets directory"),
        (RAW_DIR,      "raw data directory"),
        (BACKUPS_DIR,  "backups directory"),
    ],
)
def test_required_directories_exist_and_are_755(path_obj: Path, description: str):
    """
    Ensure that the mandatory directory skeleton is in place and has
    mode 755 (rwxr-xr-x).
    """
    assert path_obj.exists(), f"Missing {description}: {path_obj}"
    assert path_obj.is_dir(), f"{description} exists but is not a directory: {path_obj}"

    mode = stat.S_IMODE(path_obj.stat().st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"{description} ({path_obj}) has mode {oct(mode)}, expected {oct(expected_mode)}"
    )

def _current_user_crontab() -> str:
    """
    Return the current user's crontab contents as a string.
    If the user has no crontab installed, return an empty string.
    """
    # `crontab -l` exits with status 0 when a crontab exists,
    # and status 1 when none exists.
    proc = subprocess.run(
        ["crontab", "-l"],
        text=True,
        capture_output=True,
    )
    if proc.returncode == 0:
        return proc.stdout
    # When `crontab -l` returns 1, stderr typically says
    # "no crontab for <user>".  That is acceptable here.
    return ""

def test_no_backup_cron_job_yet():
    """
    The backup cron entry must NOT yet be in the user's crontab.
    (This is the initial state; the exercise asks the student to add it.)
    """
    crontab_text = _current_user_crontab()
    assert CRON_LINE not in crontab_text, (
        "The backup cron job is already present in the user's crontab, "
        "but this should be the *initial* state. Remove it before running the exercise."
    )

def test_cron_verify_file_does_not_exist():
    """
    /home/user/cron_verify.log should *not* exist yet. The student is
    expected to create it while completing the task.
    """
    assert not CRON_VERIFY_FILE.exists(), (
        f"{CRON_VERIFY_FILE} already exists. The initial state must *not* "
        "contain this file."
    )