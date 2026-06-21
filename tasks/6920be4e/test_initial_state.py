# test_initial_state.py
#
# Pytest suite to verify the operating-system state **before** the student
# runs any solution commands.
#
# What we expect to be present:
#   1. Directory : /home/user/backups
#   2. File      : /home/user/backups/app_config_2024-06-01.tar.gz
#   3. Directory : /home/user/restore_scratch   (must be empty)
#
# What we expect NOT to be present yet:
#   1. Directory : /home/user/performance
#   2. File      : /home/user/performance/restore_time.log
#
# These checks guarantee a clean starting point for the exercise.

import os
import tarfile
from pathlib import Path

BACKUP_DIR          = Path("/home/user/backups")
TARBALL_PATH        = BACKUP_DIR / "app_config_2024-06-01.tar.gz"
RESTORE_SCRATCH_DIR = Path("/home/user/restore_scratch")
PERFORMANCE_DIR     = Path("/home/user/performance")
RESTORE_LOG_PATH    = PERFORMANCE_DIR / "restore_time.log"


def test_backup_directory_exists():
    assert BACKUP_DIR.is_dir(), (
        f"Missing required directory: {BACKUP_DIR}. "
        "It should exist before the exercise begins."
    )


def test_backup_tarball_exists_and_is_valid():
    assert TARBALL_PATH.is_file(), (
        f"Missing backup archive: {TARBALL_PATH}. "
        "The exercise requires this tarball to be present."
    )

    # The file should be a valid (gzip-compressed) tar archive.
    assert tarfile.is_tarfile(str(TARBALL_PATH)), (
        f"{TARBALL_PATH} is not a valid tar archive."
    )

    # The specification says it is 'random small tarball, <500 KB'.
    size_kb = TARBALL_PATH.stat().st_size / 1024
    assert size_kb < 500, (
        f"{TARBALL_PATH} is unexpectedly large ({size_kb:.1f} KB). "
        "It should be under 500 KB."
    )


def test_restore_scratch_directory_exists_and_is_empty():
    assert RESTORE_SCRATCH_DIR.is_dir(), (
        f"Missing restore scratch directory: {RESTORE_SCRATCH_DIR}."
    )

    contents = list(RESTORE_SCRATCH_DIR.iterdir())
    assert not contents, (
        f"{RESTORE_SCRATCH_DIR} is expected to be empty before the restore, "
        f"but it already contains: {[p.name for p in contents]}"
    )


def test_performance_directory_not_present_yet():
    # The performance directory (and log file) should not exist beforehand.
    assert not PERFORMANCE_DIR.exists(), (
        f"{PERFORMANCE_DIR} already exists; it should be created "
        "by the student's command, not before."
    )
    assert not RESTORE_LOG_PATH.exists(), (
        f"{RESTORE_LOG_PATH} already exists; it must be generated "
        "by the student's command."
    )