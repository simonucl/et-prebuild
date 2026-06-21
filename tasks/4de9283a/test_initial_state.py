# test_initial_state.py
#
# This pytest suite verifies that the operating-system / file-system
# starts in a clean state *before* the student carries out any steps
# of the “daily cost report” exercise.

import os
import subprocess
from pathlib import Path

# Absolute paths used throughout the exercise
FINOPS_DIR         = Path("/home/user/finops")
SCRIPTS_DIR        = FINOPS_DIR / "scripts"
LOGS_DIR           = FINOPS_DIR / "logs"
SCRIPT_PATH        = SCRIPTS_DIR / "daily_cost_report.sh"
SUMMARY_PATH       = FINOPS_DIR / "setup_summary.txt"

CRON_TARGET_LINE = (
    "0 6 * * 1-5 /home/user/finops/scripts/daily_cost_report.sh "
    ">> /home/user/finops/logs/daily_cost_report.log 2>&1"
)


def _read_user_crontab():
    """
    Returns the current user's crontab as a list of strings (one per line).
    If the user has no crontab, an empty list is returned.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # When there is *no* crontab, the command returns exit-code 1 and writes
    # a message like "no crontab for <user>" to stderr.  We treat this case
    # as an empty crontab.
    if proc.returncode != 0:
        return []

    # Split into raw lines (keep newline stripping simple and predictable)
    return proc.stdout.splitlines()


def _active_cron_lines(crontab_lines):
    """
    Filters out blank lines and comments from the crontab and returns only the
    active (effective) entries.
    """
    active = []
    for line in crontab_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            active.append(stripped)
    return active


def test_directories_absent():
    """
    Neither /home/user/finops/scripts nor /home/user/finops/logs should exist
    before the student starts the task.
    """
    assert not SCRIPTS_DIR.exists(), (
        f"Directory {SCRIPTS_DIR} already exists; the environment must be clean "
        "before the exercise begins."
    )
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} already exists; the environment must be clean "
        "before the exercise begins."
    )


def test_script_absent():
    """
    The reporting script must *not* exist yet.
    """
    assert not SCRIPT_PATH.exists(), (
        f"File {SCRIPT_PATH} already exists; the student has not started the "
        "exercise yet, so this file should be absent."
    )


def test_summary_file_absent():
    """
    The human-readable summary file must *not* exist yet.
    """
    assert not SUMMARY_PATH.exists(), (
        f"File {SUMMARY_PATH} already exists; the environment must start in a "
        "clean state."
    )


def test_crontab_is_empty():
    """
    The user's crontab should contain no active lines before the exercise.
    Comment and blank lines are allowed.  Any active entry will be treated as
    pollution of the initial state.
    """
    crontab_lines = _read_user_crontab()
    active_lines = _active_cron_lines(crontab_lines)

    assert not active_lines, (
        "The user already has active cron entries:\n\n"
        + "\n".join(active_lines)
        + "\n\nThe initial state must have *no* active cron lines."
    )

    # Additionally, ensure the specific target line is not already present.
    assert CRON_TARGET_LINE not in active_lines, (
        "The target cron line is already present in the user's crontab, "
        "but the exercise has not been performed yet."
    )