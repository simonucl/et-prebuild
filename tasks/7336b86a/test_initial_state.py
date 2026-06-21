# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# BEFORE the student starts working on the task.  It asserts that
# the pre-existing resources are in place and that none of the
# “result” artefacts have been created yet.
#
# Only the Python stdlib and pytest are used.



import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_non_empty_lines(path: Path):
    """
    Return the list of non-empty lines (without their trailing newlines)
    from *path*.  Empty / whitespace-only lines are ignored so that the
    comparison is robust against accidental blank lines.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh if line.strip()]


# ---------------------------------------------------------------------------
# Expected reference data
# ---------------------------------------------------------------------------

EXPECTED_BACKUP_LOG_LINES = [
    "2023-07-10 08:12:30 - START_BACKUP - backup_name=home_full",
    "2023-07-10 09:03:02 - BACKUP_COMPLETED - backup_name=home_full status=OK duration=3032s",
    "2023-07-11 11:00:00 - START_RESTORE - backup_name=home_full",
    "2023-07-11 11:05:22 - RESTORE_COMPLETED - backup_name=home_full status=OK duration=322s",
    "2023-07-12 06:45:11 - START_BACKUP - backup_name=db_inc",
    "2023-07-12 06:50:45 - BACKUP_FAILED - backup_name=db_inc status=ERROR code=28",
    "2023-07-12 07:10:00 - START_RESTORE - backup_name=db_inc",
    "2023-07-12 07:15:40 - RESTORE_FAILED - backup_name=db_inc status=ERROR code=28",
    "2023-07-13 14:23:55 - START_RESTORE - backup_name=conf_files",
    "2023-07-13 14:24:05 - RESTORE_COMPLETED - backup_name=conf_files status=OK duration=10s",
    "2023-07-14 17:32:01 - START_RESTORE - backup_name=logs_archive",
    "2023-07-14 17:33:59 - RESTORE_COMPLETED - backup_name=logs_archive status=OK duration=118s",
]

SAMPLE_BACKUP_FILES = {
    "home_full_2023-07-10.tar.gz",
    "conf_files_2023-07-13.tar.gz",
    "logs_archive_2023-07-14.tar.gz",
}

# Paths that MUST NOT exist before the student’s solution runs
FORBIDDEN_EARLY_PATHS = [
    HOME / "restore_tests",
    HOME / "restore_tests" / "restore_success.log",
    HOME / "restore_tests" / "restore_summary.txt",
]

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_logs_directory_and_file_exist():
    """The central logs directory and the main backup.log must pre-exist."""
    logs_dir = HOME / "logs"
    backup_log = logs_dir / "backup.log"

    assert logs_dir.is_dir(), (
        f"Expected logs directory {logs_dir} to exist, "
        "but it is missing."
    )
    assert backup_log.is_file(), (
        f"Expected backup log {backup_log} to exist, "
        "but it is missing."
    )


def test_backup_log_content_is_exact():
    """backup.log must contain the exact expected lines and nothing else."""
    backup_log = HOME / "logs" / "backup.log"
    lines = _read_non_empty_lines(backup_log)

    assert lines == EXPECTED_BACKUP_LOG_LINES, (
        "The content of /home/user/logs/backup.log is not as expected.\n"
        "Differences detected between the file and the reference data."
    )


def test_sample_backups_directory_and_files_exist():
    """The sample_backups directory and its .tar.gz archives must be present."""
    samples_dir = HOME / "sample_backups"
    assert samples_dir.is_dir(), (
        f"Expected directory {samples_dir} to exist, but it is missing."
    )

    existing_files = {p.name for p in samples_dir.glob("*.tar.gz")}
    missing = SAMPLE_BACKUP_FILES - existing_files
    unexpected = existing_files - SAMPLE_BACKUP_FILES

    assert not missing, (
        "The following expected .tar.gz sample backup files are missing "
        f"from {samples_dir}: {', '.join(sorted(missing))}"
    )

    # We are tolerant of additional files; they do no harm.


@pytest.mark.parametrize("path", FORBIDDEN_EARLY_PATHS)
def test_result_files_do_not_exist_yet(path: Path):
    """No result artefacts should exist before the student performs any action."""
    assert not path.exists(), (
        f"Path {path} already exists, but it should NOT be present "
        "before the task is executed."
    )