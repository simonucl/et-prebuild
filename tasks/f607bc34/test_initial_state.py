# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student performs any actions for the cron-policy task.

import os
from pathlib import Path

WEEKLY_LINE = "0 0 * * 0 /home/user/scripts/weekly_maintenance.sh"
POLICY_FILE = Path("/home/user/policies/allowed_cron_jobs.txt")
CRONTAB_FILE = Path("/home/user/cron/enforced_user_crontab")
REPORT_FILE = Path("/home/user/logs/cron_policy_report.log")
BACKUP_DIR = Path("/home/user/backup")
LOGS_DIR = Path("/home/user/logs")


def _read_lines(p: Path):
    """Return non-empty, stripped lines from a text file."""
    with p.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh.readlines() if ln.strip()]


def test_policy_file_initial_state_exists_and_contains_only_weekly_job():
    assert POLICY_FILE.is_file(), (
        f"Policy file not found at expected path: {POLICY_FILE}"
    )
    lines = _read_lines(POLICY_FILE)
    assert lines == [WEEKLY_LINE], (
        "Policy file should contain exactly one line—the weekly maintenance job.\n"
        f"Expected:\n  {WEEKLY_LINE!r}\nFound:\n  {lines!r}"
    )


def test_effective_crontab_initial_state_exists_and_contains_only_weekly_job():
    assert CRONTAB_FILE.is_file(), (
        f"Effective crontab file not found at expected path: {CRONTAB_FILE}"
    )
    lines = _read_lines(CRONTAB_FILE)
    assert lines == [WEEKLY_LINE], (
        "Effective crontab should initially contain only the weekly maintenance job.\n"
        f"Expected:\n  {WEEKLY_LINE!r}\nFound:\n  {lines!r}"
    )


def test_logs_directory_exists_and_report_file_absent():
    assert LOGS_DIR.is_dir(), f"Logs directory is missing at: {LOGS_DIR}"
    assert not REPORT_FILE.exists(), (
        "Compliance report should not exist before the student generates it.\n"
        f"Unexpected file found at: {REPORT_FILE}"
    )


def test_backup_directory_should_not_exist_yet():
    assert not BACKUP_DIR.exists(), (
        "Backup directory should not exist before the student creates it.\n"
        f"Unexpected path found at: {BACKUP_DIR}"
    )