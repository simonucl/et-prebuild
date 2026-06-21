# test_initial_state.py
#
# This test-suite verifies that the system is still in the *initial* state,
# i.e. none of the artefacts that the student is asked to create already
# exist.  If any of these tests fail, it means the operating-system /
# filesystem has been modified before the task begins.

import subprocess
import sys
from pathlib import Path

import pytest


HOME = Path("/home/user")
SECURITY_DIR = HOME / "security"

ROTATE_SCRIPT = SECURITY_DIR / "rotate_creds.sh"
CRONTAB_EXPORT = SECURITY_DIR / "final_crontab.txt"
SETUP_LOG = SECURITY_DIR / "rotation_setup.log"

CRON_LINE = "45 2 1 * * /home/user/security/rotate_creds.sh"


def _crontab_available() -> bool:
    """
    Return True if the `crontab` executable is available on this system.
    We rely only on stdlib (no shutil.which in Python <3.3 on some test boxes).
    """
    from shutil import which

    return which("crontab") is not None


def _get_user_crontab() -> str:
    """
    Return the current user's crontab text (may be empty).
    If the user has no crontab yet, crontab -l exits with status 1.
    We treat that as an empty crontab.
    """
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:  # crontab command absent
        return ""

    # If the user has no crontab yet, crontab exits with non-zero status.
    if result.returncode != 0:
        return ""

    return result.stdout


@pytest.mark.order(1)
def test_security_directory_absent():
    assert (
        not SECURITY_DIR.exists()
    ), f"Directory {SECURITY_DIR} already exists but should not be present before the exercise starts."


@pytest.mark.order(2)
def test_rotate_script_absent():
    assert (
        not ROTATE_SCRIPT.exists()
    ), f"File {ROTATE_SCRIPT} already exists; the student must create it during the exercise."


@pytest.mark.order(3)
def test_final_crontab_file_absent():
    assert (
        not CRONTAB_EXPORT.exists()
    ), f"File {CRONTAB_EXPORT} already exists; it should only be created after the exercise is completed."


@pytest.mark.order(4)
def test_setup_log_absent():
    assert (
        not SETUP_LOG.exists()
    ), f"File {SETUP_LOG} already exists; it should only be created after the exercise is completed."


@pytest.mark.order(5)
def test_crontab_does_not_contain_rotation_job():
    if not _crontab_available():
        pytest.skip("crontab command not available on this system; skipping crontab check.")

    crontab_text = _get_user_crontab()
    assert (
        CRON_LINE not in crontab_text
    ), (
        "The user's crontab already contains the rotation job line:\n"
        f"    {CRON_LINE}\n"
        "The crontab should be empty (or at least not contain this line) at the start of the exercise."
    )