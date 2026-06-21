# test_initial_state.py
#
# Pytest suite that validates the starting filesystem state for the
# “low disk space” alert-rule exercise *before* the student runs any
# command.  It checks only the initial conditions explicitly described
# in the specification.

import os
import stat
import pytest

HOME = "/home/user"
ALERT_RULES_DIR = os.path.join(HOME, "monitoring", "alert_rules")
ALERT_FILE = os.path.join(ALERT_RULES_DIR, "disk_space.alert")
TASK_LOG = os.path.join(HOME, "task.log")


def _describe_path(path):
    """
    Helper returning a human-readable description of a filesystem path
    for assertion error messages.
    """
    return f"'{path}' (absolute path)"


def test_alert_rules_directory_exists_and_is_writable():
    """
    The directory /home/user/monitoring/alert_rules/ must already
    exist and be writable by the current (non-root) user.
    """
    # It must exist.
    assert os.path.exists(ALERT_RULES_DIR), (
        f"Required directory {_describe_path(ALERT_RULES_DIR)} does not exist."
        "\nCreate it before beginning the task."
    )

    # It must be a directory (not a file, link, etc.).
    assert os.path.isdir(ALERT_RULES_DIR), (
        f"{_describe_path(ALERT_RULES_DIR)} exists but is not a directory."
    )

    # It must be writable by the current user (effective UID).
    is_writable = os.access(ALERT_RULES_DIR, os.W_OK)
    assert is_writable, (
        f"{_describe_path(ALERT_RULES_DIR)} is not writable by the current user."
        "\nEnsure permissions allow file creation within it."
    )

    # Optional sanity: directory should not be world-writable without the sticky bit,
    # but we issue only a warning, not a failure.
    mode = os.stat(ALERT_RULES_DIR).st_mode
    world_writable = bool(mode & stat.S_IWOTH)
    sticky = bool(mode & stat.S_ISVTX)
    if world_writable and not sticky:
        pytest.warns(
            UserWarning,
            lambda: None,
            match="Directory is world-writable without the sticky bit set.",
        )


def test_disk_space_alert_file_should_not_exist_yet():
    """
    Before the student starts, *no* disk_space.alert file should be
    present.  Its absence ensures the task genuinely creates it.
    """
    assert not os.path.exists(ALERT_FILE), (
        f"Found unexpected pre-existing file {_describe_path(ALERT_FILE)}."
        "\nRemove or rename it so the student can create a fresh rule file."
    )


def test_task_log_should_not_exist_yet():
    """
    The confirmation log /home/user/task.log must not exist at the
    outset.
    """
    assert not os.path.exists(TASK_LOG), (
        f"Found unexpected pre-existing file {_describe_path(TASK_LOG)}."
        "\nRemove or rename it so the student can create a fresh log."
    )