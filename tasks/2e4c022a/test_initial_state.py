# test_initial_state.py
#
# Pytest suite to verify that the filesystem is in the expected
# “pre-task” state for the backup-validation exercise.
#
# What we assert:
# 1. The /home/user/backups directory exists and is a directory.
# 2. The metadata file exists, is readable UTF-8 JSON and contains the
#    four expected backup objects, with the exact contents specified in
#    the task description.
# 3. The report and log files that the student is supposed to create
#    later do NOT yet exist.
#
# Any deviation from these expectations will cause the test to fail
# with a clear, actionable message.

import json
import os
import stat
import pytest
from pathlib import Path

BACKUPS_DIR = Path("/home/user/backups")
METADATA_FILE = BACKUPS_DIR / "metadata.json"
REPORT_FILE = BACKUPS_DIR / "validation_report.json"
LOG_FILE = Path("/home/user/backup_validation.log")


def test_backups_directory_exists():
    assert BACKUPS_DIR.exists(), f"Required directory {BACKUPS_DIR} is missing."
    assert BACKUPS_DIR.is_dir(), f"{BACKUPS_DIR} exists but is not a directory."

    # Verify directory permissions are at least 755 (owner rwx, group rx, others rx)
    mode = BACKUPS_DIR.stat().st_mode
    expected_perms = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    assert (mode & 0o777) == expected_perms, (
        f"{BACKUPS_DIR} permissions are {oct(mode & 0o777)}, expected 0o755."
    )


def test_metadata_file_exists_and_is_valid_json():
    assert METADATA_FILE.exists(), f"Required file {METADATA_FILE} is missing."
    assert METADATA_FILE.is_file(), f"{METADATA_FILE} exists but is not a regular file."

    try:
        raw = METADATA_FILE.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{METADATA_FILE} is not valid UTF-8: {exc}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{METADATA_FILE} does not contain valid JSON: {exc}")

    # Validate the JSON structure and exact contents
    assert isinstance(data, list), (
        f"{METADATA_FILE} JSON root must be a list/array, got {type(data).__name__}."
    )
    assert len(data) == 4, (
        f"Expected 4 backup objects in {METADATA_FILE}, found {len(data)}."
    )

    expected_objects = [
        {"id": "bkp-001", "timestamp": "2023-10-01T02:00:00Z", "size": 2048, "status": "completed"},
        {"id": "bkp-002", "timestamp": "2023-10-02T02:00:00Z", "status": "failed"},
        {"id": "bkp-003", "timestamp": "2023-10-03T02:00:00Z", "size": 4096, "status": "completed"},
        {"id": "bkp-004", "timestamp": "2023-10-04T02:00:00Z", "size": 1024},
    ]

    assert data == expected_objects, (
        f"The contents of {METADATA_FILE} do not match the expected initial state."
    )


@pytest.mark.parametrize("path", [REPORT_FILE, LOG_FILE])
def test_output_files_do_not_yet_exist(path: Path):
    assert not path.exists(), (
        f"{path} should NOT exist before the student runs their solution."
    )