# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any action for the “file-synchronisation”
# task.  All assertions are intentionally strict so that any deviation from
# the expected starting conditions is made explicit.

import os
import stat
import pytest

HOME = "/home/user"
INCOMING_DIR = os.path.join(HOME, "incoming")
REMOTE_BACKUP_DIR = os.path.join(HOME, "remote_backup")
SYNC_LOG_DIR = os.path.join(HOME, "sync_logs")
SYNC_LOG_FILE = os.path.join(SYNC_LOG_DIR, "last_sync.log")

EXPECTED_INCOMING_FILES = {
    "report.txt": b"Quarterly data\n",   # 14 bytes
    "image.png": b"PNG",                 # 3 bytes
}

EXPECTED_INCOMING_PERMS = 0o755
EXPECTED_REMOTE_PERMS = 0o755


def _mode(path):
    "Return filesystem permission bits for `path` (e.g. 0o755)."
    return stat.S_IMODE(os.stat(path).st_mode)


@pytest.mark.order(1)
def test_directories_exist_and_permissions():
    # /home/user/incoming
    assert os.path.isdir(INCOMING_DIR), (
        f"Expected directory {INCOMING_DIR!r} to exist."
    )
    assert _mode(INCOMING_DIR) == EXPECTED_INCOMING_PERMS, (
        f"Directory {INCOMING_DIR!r} should have permissions "
        f"{oct(EXPECTED_INCOMING_PERMS)}, found {oct(_mode(INCOMING_DIR))}."
    )

    # /home/user/remote_backup
    assert os.path.isdir(REMOTE_BACKUP_DIR), (
        f"Expected directory {REMOTE_BACKUP_DIR!r} to exist."
    )
    assert _mode(REMOTE_BACKUP_DIR) == EXPECTED_REMOTE_PERMS, (
        f"Directory {REMOTE_BACKUP_DIR!r} should have permissions "
        f"{oct(EXPECTED_REMOTE_PERMS)}, found {oct(_mode(REMOTE_BACKUP_DIR))}."
    )


@pytest.mark.order(2)
def test_remote_backup_starts_empty():
    contents = os.listdir(REMOTE_BACKUP_DIR)
    assert contents == [] or contents == {}, (
        f"Directory {REMOTE_BACKUP_DIR!r} must be empty at start; "
        f"found: {contents}"
    )


@pytest.mark.order(3)
def test_incoming_contains_expected_files_and_only_them():
    incoming_files = sorted(os.listdir(INCOMING_DIR))
    expected_files_sorted = sorted(EXPECTED_INCOMING_FILES.keys())
    assert incoming_files == expected_files_sorted, (
        f"{INCOMING_DIR!r} should contain only {expected_files_sorted}, "
        f"found {incoming_files}"
    )


@pytest.mark.order(4)
@pytest.mark.parametrize("filename,expected_bytes", EXPECTED_INCOMING_FILES.items())
def test_each_incoming_file_has_correct_content(filename, expected_bytes):
    path = os.path.join(INCOMING_DIR, filename)
    assert os.path.isfile(path), f"Missing expected file: {path!r}"

    # File size check
    size = os.path.getsize(path)
    expected_size = len(expected_bytes)
    assert size == expected_size, (
        f"{filename!r} should be {expected_size} bytes, found {size} bytes."
    )

    # Content check (binary-exact)
    with open(path, "rb") as fh:
        content = fh.read()
    assert content == expected_bytes, (
        f"Content of {filename!r} does not match expected bytes."
    )


@pytest.mark.order(5)
def test_sync_log_does_not_exist_yet():
    assert not os.path.exists(SYNC_LOG_FILE), (
        f"Log file {SYNC_LOG_FILE!r} should NOT exist before the task begins."
    )