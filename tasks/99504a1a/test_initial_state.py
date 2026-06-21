# test_initial_state.py
#
# Pytest suite to validate the initial, pre-task filesystem state
# for the “QA firewall” exercise.
#
# The student has not yet created any artefacts, therefore NONE of the
# following should exist:
#   • /home/user/qa_firewall  (directory)
#   • /home/user/qa_firewall/configure_firewall.sh  (script)
#   • /home/user/qa_firewall/firewall_dry_run.log   (log file)
#
# If any of these paths already exist the environment is considered
# “dirty” and the test(s) will fail with an explanatory message.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")
WORK_DIR = HOME / "qa_firewall"
SCRIPT = WORK_DIR / "configure_firewall.sh"
DRY_RUN_LOG = WORK_DIR / "firewall_dry_run.log"


def _assert_absent(p: Path, what: str):
    """
    Helper: assert that the given path does *not* exist in the filesystem.
    """
    assert not p.exists(), (
        f"{what} already exists at {p}. The initial environment must be clean. "
        f"Remove it before starting the exercise."
    )


def test_home_directory_exists():
    """Sanity-check: /home/user should always be present."""
    assert HOME.exists() and HOME.is_dir(), "/home/user is missing—unexpected test environment."


def test_work_directory_absent():
    """
    The dedicated working directory must NOT exist before the
    student performs any action.
    """
    _assert_absent(WORK_DIR, "Working directory")


def test_firewall_script_absent():
    """
    The firewall configuration script must NOT exist before the
    student performs any action.
    """
    _assert_absent(SCRIPT, "Firewall script")


def test_dry_run_log_absent():
    """
    The dry-run log must NOT exist before the student performs any action.
    """
    _assert_absent(DRY_RUN_LOG, "Dry-run log")