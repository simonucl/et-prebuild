# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “nightly restore workflow” exercise, **before** the student performs
# any actions.

import os
import stat
import pytest

HOME = "/home/user"
BACKUPS_DIR = os.path.join(HOME, "backups")
BACKUP_OLD = os.path.join(BACKUPS_DIR, "2024-05-01")
BACKUP_NEW = os.path.join(BACKUPS_DIR, "2024-06-01")
SYMLINK_LATEST = os.path.join(HOME, "backup_latest")
LOG_FILE = os.path.join(HOME, "restore_test.log")


def _is_dir(path):
    """Return True if path exists and is a directory."""
    return os.path.isdir(path)


def _is_symlink(path):
    """Return True if path exists and is a symbolic link."""
    return os.path.islink(path)


def _symlink_target(path):
    """Return the absolute, resolved target of a symlink."""
    # os.path.realpath follows the symlink chain and returns
    # an absolute path independent of how the link was written
    return os.path.realpath(path)


def test_backups_directory_exists():
    """The /home/user/backups directory must exist and be a directory."""
    assert _is_dir(BACKUPS_DIR), (
        f"Expected directory {BACKUPS_DIR!r} to exist, "
        "but it is missing or not a directory."
    )


@pytest.mark.parametrize(
    "subdir",
    [
        BACKUP_OLD,
        BACKUP_NEW,
    ],
)
def test_timestamped_backup_subdirs_exist(subdir):
    """Required timestamped sub-directories must be present inside /home/user/backups/."""
    assert _is_dir(subdir), (
        f"Expected backup subdirectory {subdir!r} to exist inside {BACKUPS_DIR!r}, "
        "but it is missing or not a directory."
    )


def test_backup_latest_is_symlink():
    """/home/user/backup_latest must exist and be a symlink (not a file or directory)."""
    assert _is_symlink(SYMLINK_LATEST), (
        f"{SYMLINK_LATEST!r} should be a symbolic link pointing to "
        f"{BACKUP_OLD!r}, but it is missing or not a symlink."
    )


def test_backup_latest_points_to_old_backup():
    """
    The *initial* target of /home/user/backup_latest must be
    /home/user/backups/2024-05-01 (resolved absolute path).
    """
    target = _symlink_target(SYMLINK_LATEST)
    assert target == BACKUP_OLD, (
        f"{SYMLINK_LATEST!r} is expected to point to {BACKUP_OLD!r} "
        f"before the exercise begins, but it actually points to {target!r}."
    )


def test_restore_log_does_not_exist_yet():
    """The restore_test.log file must not exist before the student runs their solution."""
    assert not os.path.exists(LOG_FILE), (
        f"Log file {LOG_FILE!r} already exists; the initial state should not "
        "contain this file."
    )