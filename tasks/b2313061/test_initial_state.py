# test_initial_state.py
#
# Pytest suite to verify the **initial** state of the laboratory image
# BEFORE the learner adds a personal cron entry or generates any artefacts.
#
# The pre-lab image must already provide:
#   • Directory  : /home/user/backup
#   • Script file: /home/user/backup/cleanup.sh
#
# The following **must NOT** yet exist (they will be created by the learner):
#   • /home/user/backup/crontab_after.txt
#   • /home/user/backup/verification.log
#
# Furthermore, the learner has not yet installed the target cron line:
#   30 3 * * * /home/user/backup/cleanup.sh >> /home/user/backup/cleanup.log 2>&1
#
# Only stdlib + pytest are used, in accordance with the grading harness.


import subprocess
from pathlib import Path

import pytest


BACKUP_DIR = Path("/home/user/backup")
CLEANUP_SCRIPT = BACKUP_DIR / "cleanup.sh"
CRONTAB_AFTER = BACKUP_DIR / "crontab_after.txt"
VERIFICATION_LOG = BACKUP_DIR / "verification.log"

TARGET_CRON_LINE = (
    "30 3 * * * /home/user/backup/cleanup.sh >> "
    "/home/user/backup/cleanup.log 2>&1"
)


def test_backup_directory_exists():
    """The /home/user/backup directory must already exist."""
    assert BACKUP_DIR.is_dir(), (
        f"Required directory missing: {BACKUP_DIR} "
        "(the laboratory image is not correctly initialised)."
    )


def test_cleanup_script_present():
    """cleanup.sh must be present inside the backup directory."""
    assert CLEANUP_SCRIPT.is_file(), (
        f"Required script missing: {CLEANUP_SCRIPT} "
        "(students need this script to reference in their cron job)."
    )
    # Not strictly required, but helpful to flag if the script isn't executable.
    assert CLEANUP_SCRIPT.stat().st_mode & 0o111, (
        f"Script {CLEANUP_SCRIPT} exists but is not executable; "
        "please set an executable bit so the cron job can run it."
    )


@pytest.mark.parametrize("path_obj", [CRONTAB_AFTER, VERIFICATION_LOG])
def test_output_files_do_not_exist_yet(path_obj: Path):
    """
    Neither crontab_after.txt nor verification.log should be present *before*
    the learner performs any actions.
    """
    assert not path_obj.exists(), (
        f"File {path_obj} already exists before the exercise starts. "
        "The initial state should be clean—remove this file from the base image."
    )


def test_target_cron_line_not_already_installed():
    """
    Ensure that the target cron entry is NOT yet present in the user's crontab.
    The learner will add this line; it must not pre-exist.
    """
    # Try to read the current user's crontab. When no personal crontab exists,
    # `crontab -l` exits with status 1 and prints an explanatory message.
    proc = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    crontab_contents = proc.stdout if proc.returncode == 0 else ""

    assert TARGET_CRON_LINE not in crontab_contents.splitlines(), (
        "The target cron line is already present in the user's crontab. "
        "It should be absent at the start of the exercise so the learner "
        "can add it themselves."
    )