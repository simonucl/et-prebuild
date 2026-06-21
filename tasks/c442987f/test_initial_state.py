# test_initial_state.py
#
# Pytest suite to validate the *initial* operating-system / filesystem
# state **before** the student performs any credential-rotation steps.
#
# What we assert:
#   • Source directory /home/user/secure_configs/ exists and already contains
#     the two expected *.conf files.
#   • Destination directory /home/user/remote_backup/ exists and does *not*
#     yet contain those files (it should be empty of them).
#   • Log directory /home/user/rotation_logs/ exists but the rotation-log file
#     /home/user/rotation_logs/2023-credentials-rotation.log does *not* exist.
#
# NOTE:  These tests purposefully avoid checking for any artifacts that will be
#        created by the student action.  They confirm the starting conditions
#        only.

import os
import stat
import pytest

HOME = "/home/user"
SRC_DIR = os.path.join(HOME, "secure_configs")
DST_DIR = os.path.join(HOME, "remote_backup")
LOG_DIR = os.path.join(HOME, "rotation_logs")
LOG_FILE = os.path.join(LOG_DIR, "2023-credentials-rotation.log")

EXPECTED_CONF_FILES = {"secret.conf", "vault.conf"}


def _full_paths(directory, filenames):
    """Return a dict of filename -> full path for convenience."""
    return {fn: os.path.join(directory, fn) for fn in filenames}


def test_secure_configs_directory_exists_and_is_readable():
    assert os.path.isdir(SRC_DIR), (
        f"Required source directory missing: {SRC_DIR}"
    )

    # Directory must be readable (EXECUTE bit required to access files)
    src_stat = os.stat(SRC_DIR)
    assert bool(src_stat.st_mode & stat.S_IXUSR), (
        f"Source directory {SRC_DIR} exists but is not accessible (execute bit missing)."
    )


@pytest.mark.parametrize("conf_file", sorted(EXPECTED_CONF_FILES))
def test_each_expected_conf_file_present_in_source(conf_file):
    file_path = os.path.join(SRC_DIR, conf_file)
    assert os.path.isfile(file_path), (
        f"Expected credential file missing in source directory: {file_path}"
    )

    # Sanity-check that the file is not empty
    assert os.path.getsize(file_path) > 0, (
        f"Credential file {file_path} is unexpectedly empty."
    )


def test_no_extra_conf_files_missing():
    """There should be *at least* the expected conf files in the source."""
    present = {f for f in os.listdir(SRC_DIR) if f.endswith(".conf")}
    missing = EXPECTED_CONF_FILES - present
    assert not missing, (
        "Source directory is missing expected conf files: "
        + ", ".join(sorted(missing))
    )


def test_remote_backup_directory_exists_and_is_writable():
    assert os.path.isdir(DST_DIR), (
        f"Destination directory missing: {DST_DIR}"
    )

    dst_stat = os.stat(DST_DIR)
    assert bool(dst_stat.st_mode & stat.S_IWUSR), (
        f"Destination directory {DST_DIR} exists but is not writable."
    )


@pytest.mark.parametrize("conf_file", sorted(EXPECTED_CONF_FILES))
def test_conf_files_not_yet_in_destination(conf_file):
    """Ensure the destination does not yet contain any of the *.conf files."""
    file_path = os.path.join(DST_DIR, conf_file)
    assert not os.path.exists(file_path), (
        f"Destination already contains {file_path}; "
        "it should be empty before synchronization."
    )


def test_rotation_logs_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Log directory is missing: {LOG_DIR}"
    )


def test_rotation_log_file_not_yet_created():
    assert not os.path.exists(LOG_FILE), (
        f"Rotation log file {LOG_FILE} already exists; "
        "it should not be present before the rotation task."
    )