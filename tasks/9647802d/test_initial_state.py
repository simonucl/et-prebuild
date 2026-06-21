# test_initial_state.py
#
# Pytest suite that validates the *initial* condition of the operating-system
# and filesystem **before** the student starts working on the assignment.
#
# The tests will PASS only when none of the required artefacts for the finished
# assignment are present yet.  If any of them already exist, the environment is
# considered “dirty” and the tests will FAIL with a clear explanation so the
# student (and the grader) know that a fresh workspace is required.
#
# Allowed imports: only stdlib + pytest.

import os
import subprocess
from pathlib import Path

HOME = Path("/home/user")

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------


def _crontab_contents() -> str:
    """
    Return the current user crontab as text.

    If the user has **no** crontab yet, `crontab -l` exits with status 1.
    We interpret that as an empty crontab.
    """
    proc = subprocess.run(
        ["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    if proc.returncode != 0:
        return ""
    return proc.stdout.decode(errors="ignore")


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------


def test_script_absent():
    """
    The utility script must *not* exist yet.
    """
    script_path = HOME / "tools" / "hello_timer.sh"
    assert (
        not script_path.exists()
    ), f"Unexpected file found: {script_path} – the environment is not clean."


def test_cron_entry_absent():
    """
    The user crontab must not yet contain the scheduled job line.
    """
    expected_line = (
        "57 4 * * * /home/user/tools/hello_timer.sh >> "
        "/home/user/logs/cron_run.log 2>&1"
    )
    crontab_txt = _crontab_contents()
    assert (
        expected_line not in crontab_txt
    ), "The target cron line is already present in the user crontab."


def test_systemd_service_file_absent():
    """
    The systemd **user** service unit must not yet exist.
    """
    svc_path = HOME / ".config" / "systemd" / "user" / "hello_timer.service"
    assert (
        not svc_path.exists()
    ), f"Unexpected systemd service file found: {svc_path}"


def test_systemd_timer_file_absent():
    """
    The systemd **user** timer unit must not yet exist.
    """
    timer_path = HOME / ".config" / "systemd" / "user" / "hello_timer.timer"
    assert (
        not timer_path.exists()
    ), f"Unexpected systemd timer file found: {timer_path}"


def test_verification_summary_absent():
    """
    The verification summary file should not exist before setup.
    """
    summary_path = HOME / "logs" / "setup_check.txt"
    assert (
        not summary_path.exists()
    ), f"Verification summary file already exists at {summary_path}"


def test_runtime_log_files_absent():
    """
    The runtime log files must not exist yet.
    """
    hello_log = HOME / "logs" / "hello_timer.log"
    cron_log = HOME / "logs" / "cron_run.log"

    assert not hello_log.exists(), f"Unexpected log file found: {hello_log}"
    assert not cron_log.exists(), f"Unexpected log file found: {cron_log}"