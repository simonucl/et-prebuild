# test_initial_state.py
#
# This test-suite verifies that the workstation is in its ORIGINAL, untouched
# state *before* the learner begins work.  Therefore every artefact that the
# final grader will later require MUST **NOT** exist yet.
#
# If any of the assertions below fails it means that the machine already
# contains part of the target configuration and is therefore unsuitable for
# running the exercise.

import os
import stat
import subprocess
import pwd
import pytest
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants – absolute paths which must **NOT** exist at the start
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

SCRIPT_DIR        = HOME / "ci_cd_scripts"
LOG_DIR           = HOME / "ci_cd_logs"
EVIDENCE_FILE     = LOG_DIR / "ci_job_setup.log"

CLEANUP_SCRIPT    = SCRIPT_DIR / "cleanup_builds.sh"
SYNC_SCRIPT       = SCRIPT_DIR / "sync_to_registry.sh"

SYSTEMD_USER_DIR  = HOME / ".config" / "systemd" / "user"
SYSTEMD_SERVICE   = SYSTEMD_USER_DIR / "ci_sync.service"
SYSTEMD_TIMER     = SYSTEMD_USER_DIR / "ci_sync.timer"

CRON_LINE         = "0 * * * * /home/user/ci_cd_scripts/cleanup_builds.sh"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _crontab_lines_for_user() -> list[str]:
    """
    Return the list of lines currently present in the invoking user's crontab.
    If the user has no crontab, an empty list is returned.
    """
    result = subprocess.run(
        ["crontab", "-l"],
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        # Typical message: "no crontab for user"
        return []
    # normalise line endings and remove any trailing blank line
    return [line.rstrip("\n") for line in result.stdout.splitlines()]


def _is_timer_active(timer_name: str) -> bool:
    """
    Check whether a systemd user timer is listed (enabled/disabled) for
    the current user.
    Returns True if the timer shows up in `systemctl --user list-timers --all`.
    Any non-zero exit status from systemctl will be interpreted as *not active*,
    so that the initial state still passes even on systems without a per-user
    systemd instance.
    """
    try:
        result = subprocess.run(
            ["systemctl", "--user", "list-timers", "--all", "--no-pager"],
            text=True,
            capture_output=True,
            check=False
        )
    except FileNotFoundError:
        # systemctl not present – treat as "timer not active"
        return False

    if result.returncode != 0:
        return False

    for line in result.stdout.splitlines():
        if line.strip().startswith(timer_name):
            return True
    return False


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_directories_do_not_exist():
    """Required directories should NOT exist yet."""
    for path in [SCRIPT_DIR, LOG_DIR]:
        assert not path.exists(), f"Directory {path} already exists – the workspace is not clean."


def test_scripts_do_not_exist():
    """None of the runtime scripts should exist yet."""
    for script in [CLEANUP_SCRIPT, SYNC_SCRIPT]:
        assert not script.exists(), f"Script {script} already present – should be created by the learner."


def test_crontab_is_empty_or_different():
    """User crontab must NOT already contain the target entry (and must not be the only line)."""
    lines = _crontab_lines_for_user()
    assert CRON_LINE not in lines, "Target cron line already found in existing crontab – environment is not pristine."


def test_systemd_unit_files_absent():
    """Systemd-user unit files must not be present."""
    for unit_file in [SYSTEMD_SERVICE, SYSTEMD_TIMER]:
        assert not unit_file.exists(), f"Unit file {unit_file} already exists – initial state is polluted."


def test_timer_not_active():
    """The ci_sync.timer must not yet be listed for the user."""
    assert not _is_timer_active("ci_sync.timer"), "ci_sync.timer already appears as a user timer."


def test_evidence_file_absent():
    """Evidence file must not pre-exist."""
    assert not EVIDENCE_FILE.exists(), f"Evidence file {EVIDENCE_FILE} already present – should be created later."