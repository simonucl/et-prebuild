# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the student performs any actions for the “API log backup”
# exercise.
#
# Expectations BEFORE the task starts
# -----------------------------------
# 1. The three log files must already exist under
#       /home/user/api_test/logs/
#    with the exact byte contents / sizes listed below.
#
# 2. Neither the backup archive nor the manifest that the student is asked
#    to create must be present yet.
#
# 3. (Optional) The backups directory itself may or may not exist, but if
#    it does, it must **not** yet contain the target archive or manifest.
#
# If any of these pre-conditions fail, the test suite will raise clear,
# descriptive assertion errors so that the learner understands what needs
# to be fixed *before* proceeding with the task.

import hashlib
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Helper data (expected absolute paths, contents and sizes)                   #
# --------------------------------------------------------------------------- #

LOG_DIR = Path("/home/user/api_test/logs")

EXPECTED_LOG_FILES = {
    "request_20240601.json": b'{"request":"ping"}',      # 18 bytes
    "response_20240601.json": b'{"response":"pong"}',    # 19 bytes
    "error_20240601.json": b'{"error":null}',            # 14 bytes
}

BACKUPS_DIR = Path("/home/user/api_test/backups")
BACKUP_ARCHIVE = BACKUPS_DIR / "logs_backup_20240601.tar.gz"
BACKUP_MANIFEST = BACKUPS_DIR / "latest_backup_manifest.txt"


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_log_directory_exists():
    """Verify that /home/user/api_test/logs exists and is a directory."""
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "Create it and place the JSON log files inside."
    )
    assert LOG_DIR.is_dir(), (
        f"{LOG_DIR} exists but is not a directory. "
        "Ensure it is a directory that contains the log files."
    )


@pytest.mark.parametrize("filename,expected_bytes", EXPECTED_LOG_FILES.items())
def test_each_log_file_exists_and_matches_content(filename, expected_bytes):
    """
    For every expected .json log file:
      • It exists.
      • File size (in bytes) matches the specification.
      • File contents match the exact expected bytes (no trailing newline).
    """
    file_path = LOG_DIR / filename

    # Existence check
    assert file_path.exists(), (
        f"Expected log file {file_path} is missing."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file."
    )

    # Read file in binary mode
    actual_bytes = file_path.read_bytes()

    # Size check
    expected_size = len(expected_bytes)
    actual_size = len(actual_bytes)
    assert actual_size == expected_size, (
        f"File {file_path} should be {expected_size} bytes "
        f"but is {actual_size} bytes."
    )

    # Content check (exact byte-for-byte)
    assert actual_bytes == expected_bytes, (
        f"Contents of {file_path} do not match the expected template.\n"
        f"Expected bytes: {expected_bytes!r}\n"
        f"Actual bytes  : {actual_bytes!r}"
    )


def test_backup_outputs_do_not_exist_yet():
    """
    The student has not run the backup commands yet, so the archive and
    manifest must *not* be present. If they exist already, the initial state
    is wrong (e.g. left-over artefacts from a previous run).
    """
    assert not BACKUP_ARCHIVE.exists(), (
        f"Backup archive {BACKUP_ARCHIVE} already exists *before* the task "
        "has started. Remove it so the student exercise begins from a clean "
        "state."
    )
    assert not BACKUP_MANIFEST.exists(), (
        f"Backup manifest {BACKUP_MANIFEST} already exists *before* the task "
        "has started. Remove it so the student exercise begins from a clean "
        "state."
    )