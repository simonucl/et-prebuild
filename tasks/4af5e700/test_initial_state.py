# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student begins work on the “log-analysis” task.
#
# The expected *pre-existing* artefacts are documented in the challenge text.
# These tests assert ONLY the initial state, **not** the final deliverables.
#
# If any assertion below fails, the starting environment is already in
# an unexpected state and the student cannot reliably complete the task.

import subprocess
from pathlib import Path

import pytest

# --- Constants ----------------------------------------------------------------

HOME = Path("/home/user")
LOGS_DIR = HOME / "logs"
SYSTEM_LOG = LOGS_DIR / "system_events.log"

SCRIPTS_DIR = HOME / "scripts"
ANALYZE_SCRIPT = SCRIPTS_DIR / "analyze_logs.sh"

SUMMARY_LOG = LOGS_DIR / "analysis_summary.log"
TASK_LOG = LOGS_DIR / "analysis_task.log"

CRON_EXPECTED_LINE = (
    "*/5 * * * * /home/user/scripts/analyze_logs.sh >> "
    "/home/user/logs/analysis_cron.log 2>&1"
)

EXPECTED_LOG_LINES = [
    "[2023-04-01 10:00:00] INFO User login: alice",
    "[2023-04-01 10:05:00] WARNING Disk space low on /dev/sda1",
    "[2023-04-01 10:07:24] ERROR Failed to connect to database",
    "[2023-04-01 10:15:42] INFO Scheduled backup started",
    "[2023-04-01 10:45:13] INFO Scheduled backup completed",
    "[2023-04-01 11:00:00] ERROR Failed to send email",
    "[2023-04-01 11:30:23] WARNING High memory usage detected",
    "[2023-04-01 11:45:23] INFO User logout: alice",
    "[2023-04-01 12:00:00] INFO User login: bob",
]

EXPECTED_COUNTS = dict(INFO=5, WARNING=2, ERROR=2)


# --- Helper functions ---------------------------------------------------------

def _safe_crontab_l():
    """
    Returns the current user's `crontab -l` output as text.

    If the user has no crontab yet, crontab(1) exits with code 1 and writes
    "no crontab for user" to stderr.  In that situation we treat the crontab
    as empty and return an empty string instead of raising.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode == 0:
        return proc.stdout
    # crontab -l with exit code 1 means "no crontab for user"
    if proc.returncode == 1 and "no crontab for" in proc.stderr.lower():
        return ""
    # Anything else is unexpected.
    raise RuntimeError(
        f"`crontab -l` failed with exit code {proc.returncode}:\n{proc.stderr}"
    )


# --- Tests --------------------------------------------------------------------

def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), (
        f"Required logs directory missing: {LOGS_DIR}.\n"
        "Create it with `mkdir -p /home/user/logs` before starting the task."
    )


def test_system_events_log_exists_and_contents():
    assert SYSTEM_LOG.is_file(), (
        f"Log file {SYSTEM_LOG} does not exist. "
        "The starter environment must include it."
    )

    with SYSTEM_LOG.open() as fh:
        lines = [line.rstrip("\n") for line in fh]

    assert lines == EXPECTED_LOG_LINES, (
        f"{SYSTEM_LOG} contents differ from the expected nine lines.\n"
        "If you modified this file, restore it before continuing."
    )

    # Verify counts to catch subtle tampering.
    counts = {k: 0 for k in EXPECTED_COUNTS}
    for line in lines:
        for level in counts:
            if level in line:
                counts[level] += 1

    assert counts == EXPECTED_COUNTS, (
        f"Expected counts {EXPECTED_COUNTS} in {SYSTEM_LOG}, "
        f"but found {counts}.  Do not alter the starter log."
    )


def test_solution_artifacts_absent_initially():
    artifacts = [
        (ANALYZE_SCRIPT, "script"),
        (SUMMARY_LOG, "summary log"),
        (TASK_LOG, "task log"),
    ]

    for path, desc in artifacts:
        assert not path.exists(), (
            f"{desc.capitalize()} {path} already exists *before* you start. "
            "Begin with a clean slate."
        )

    # The scripts directory itself may or may not exist; we don't enforce.


def test_crontab_does_not_yet_have_the_new_job():
    crontab_text = _safe_crontab_l()
    assert CRON_EXPECTED_LINE not in crontab_text, (
        "The crontab already contains the scheduled job that is supposed to be "
        "added later by the student.  Start with an empty (or at least "
        "different) crontab."
    )