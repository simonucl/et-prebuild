# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be
# present *before* the student runs any backup commands.  It purposefully
# does *NOT* look for the output artefacts that the student is expected to
# create later on.
#
# What we check:
#   1. Mandatory directories exist (logs root and backups target).
#   2. The six specific “.log” files are present.
#   3. No other “.log” files are lurking anywhere under the logs root.
#   4. The backups directory is writable by the current user.
#
# Only the Python stdlib and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
LOGS_ROOT = os.path.join(HOME, "microservices", "logs")
BACKUPS_DIR = os.path.join(HOME, "backups")

EXPECTED_LOG_FILES = {
    os.path.join(LOGS_ROOT, "auth-service", "auth.log"),
    os.path.join(LOGS_ROOT, "auth-service", "error.log"),
    os.path.join(LOGS_ROOT, "billing-service", "billing.log"),
    os.path.join(LOGS_ROOT, "billing-service", "error.log"),
    os.path.join(LOGS_ROOT, "shipping-service", "shipping.log"),
    os.path.join(LOGS_ROOT, "shipping-service", "error.log"),
}


def _gather_log_files(root):
    """
    Walk ``root`` and return a set of absolute paths of all files whose
    names end with `.log` (case-sensitive).
    """
    discovered = set()
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith(".log"):
                discovered.add(os.path.join(dirpath, fname))
    return discovered


def test_logs_root_exists_and_is_dir():
    assert os.path.isdir(LOGS_ROOT), (
        f"Required directory {LOGS_ROOT!r} is missing or is not a directory."
    )


def test_backups_dir_exists_and_is_writable():
    assert os.path.isdir(BACKUPS_DIR), (
        f"Required directory {BACKUPS_DIR!r} is missing or is not a directory."
    )

    # Check write permission for the current (real) user.
    can_write = os.access(BACKUPS_DIR, os.W_OK)
    assert can_write, f"Directory {BACKUPS_DIR!r} is not writable by the current user."


def test_exactly_expected_log_files_exist():
    discovered_logs = _gather_log_files(LOGS_ROOT)

    # 1) All expected files are present.
    missing = EXPECTED_LOG_FILES - discovered_logs
    assert not missing, (
        "The following required .log files are missing:\n" +
        "\n".join(sorted(missing))
    )

    # 2) No extra .log files are present.
    extra = discovered_logs - EXPECTED_LOG_FILES
    assert not extra, (
        "Unexpected .log files were found under the logs directory:\n" +
        "\n".join(sorted(extra))
    )


@pytest.mark.parametrize("log_path", sorted(EXPECTED_LOG_FILES))
def test_each_log_file_is_non_empty_and_readable(log_path):
    assert os.path.isfile(log_path), f"{log_path!r} is not a regular file."
    assert os.access(log_path, os.R_OK), f"{log_path!r} is not readable."

    size = os.stat(log_path).st_size
    assert size > 0, f"{log_path!r} is empty (0 bytes)."


def test_service_directories_exist():
    """
    Check that each expected service sub-directory exists directly under
    LOGS_ROOT.  This helps students avoid typos like 'auth_service'.
    """
    expected_service_dirs = {  # names only
        "auth-service",
        "billing-service",
        "shipping-service",
    }

    actual_service_dirs = {
        name
        for name in os.listdir(LOGS_ROOT)
        if os.path.isdir(os.path.join(LOGS_ROOT, name))
    }

    missing = expected_service_dirs - actual_service_dirs
    assert not missing, (
        "The following service directories are missing under "
        f"{LOGS_ROOT!r}: {', '.join(sorted(missing))}"
    )