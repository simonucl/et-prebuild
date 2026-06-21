# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system / file
# system before the student performs any actions for the “Grafana dashboard
# backup” task.  It confirms that the expected source dashboards exist with the
# correct contents, that supporting directories are present, and that no backup
# artefacts (archive or log file) exist yet.  Failures will give a clear,
# actionable explanation of what is missing or incorrect.
#
# NOTE: These tests purposefully do *not* check for the end-state artefacts
# (`dashboards_backup.tar.gz`, updated `backup.log`, etc.) because they should
# not exist prior to the student’s work.

import json
import os
from pathlib import Path

# Absolute paths used throughout the tests
HOME = Path("/home/user")
DASHBOARDS_DIR = HOME / "projects" / "obs-dashboards" / "dashboards"
CPU_JSON_FILE = DASHBOARDS_DIR / "cpu.json"
MEM_JSON_FILE = DASHBOARDS_DIR / "memory.json"

BACKUP_LOGS_DIR = HOME / "backup_logs"
BACKUP_LOG_FILE = BACKUP_LOGS_DIR / "backup.log"

BACKUPS_DIR = HOME / "backups"
ARCHIVE_FILE = BACKUPS_DIR / "dashboards_backup.tar.gz"


def test_dashboards_directory_exists():
    assert DASHBOARDS_DIR.is_dir(), (
        f"Expected dashboards directory at '{DASHBOARDS_DIR}'. "
        "Directory is missing."
    )


def _assert_json_file(path: Path, expected_dict: dict):
    assert path.is_file(), f"Expected file '{path}' to exist but it does not."

    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"File '{path}' exists but does not contain valid JSON: {exc}"
        ) from exc

    assert (
        data == expected_dict
    ), f"Contents of '{path}' are incorrect. Expected {expected_dict!r}."


def test_cpu_json_content():
    expected = {"dashboard": "cpu", "version": 1}
    _assert_json_file(CPU_JSON_FILE, expected)


def test_memory_json_content():
    expected = {"dashboard": "memory", "version": 1}
    _assert_json_file(MEM_JSON_FILE, expected)


def test_backup_logs_directory_exists():
    assert BACKUP_LOGS_DIR.is_dir(), (
        f"Required directory '{BACKUP_LOGS_DIR}' is missing. "
        "Create this directory so the backup script can write logs."
    )


def test_backup_log_file_absent():
    assert not BACKUP_LOG_FILE.exists(), (
        f"Log file '{BACKUP_LOG_FILE}' should NOT exist before the task starts. "
        "It must be created by the student's backup command."
    )


def test_archive_absent():
    assert not ARCHIVE_FILE.exists(), (
        f"Archive '{ARCHIVE_FILE}' should NOT exist before the task starts. "
        "It must be created by the student's backup command."
    )


def test_backups_path_not_a_file():
    """
    The path /home/user/backups/ may or may not already exist as a directory,
    but it must *not* be a regular file (would block directory creation).
    """
    if BACKUPS_DIR.exists():
        assert BACKUPS_DIR.is_dir(), (
            f"Path '{BACKUPS_DIR}' exists but is not a directory. "
            "Remove or rename it so a directory of that name can be used."
        )