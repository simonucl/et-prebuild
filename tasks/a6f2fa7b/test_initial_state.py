# test_initial_state.py
"""
Pytest suite verifying the pre-task state of the operating system / filesystem.

These tests assert that the Python virtual-environment and its accompanying
log file do **not** exist prior to the student performing any action.  A clean
slate is required so that the creation steps can be validated unambiguously.

If any of these tests fail, it indicates that residual artefacts from previous
runs are present and must be removed before proceeding.
"""

import os
import stat
import pytest

# Constants for paths that must *NOT* exist yet.
VENV_DIR = "/home/user/api_integration_env"
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
LOG_DIR = "/home/user/setup_logs"
LOG_FILE = os.path.join(LOG_DIR, "venv_creation.log")


def _assert_path_absent(path: str) -> None:
    """
    Helper to assert that a path does not exist.

    Parameters
    ----------
    path : str
        Absolute path to check.

    Raises
    ------
    AssertionError
        If the path (file, directory, or symlink) exists.
    """
    assert not os.path.exists(
        path
    ), f"Pre-task state violation: '{path}' already exists but must be absent."


def test_venv_directory_absent():
    """
    The target virtual-environment directory must not exist yet.
    """
    _assert_path_absent(VENV_DIR)


def test_venv_python_executable_absent():
    """
    The virtual-environment's python executable must not exist yet.
    """
    _assert_path_absent(VENV_PYTHON)


def test_log_file_absent():
    """
    The venv creation log file must not exist yet.
    """
    _assert_path_absent(LOG_FILE)


def test_log_directory_state():
    """
    The log directory may or may not exist; if it exists, it must not already
    contain the venv creation log file.  Additionally, ensure the directory,
    when present, is writable by the current user so that the forthcoming
    steps can create the log file.
    """
    if os.path.exists(LOG_DIR):
        # Directory exists: confirm writability and absence of log file.
        assert os.path.isdir(
            LOG_DIR
        ), f"Expected '{LOG_DIR}' to be a directory, but it is not."
        assert os.access(
            LOG_DIR, os.W_OK
        ), f"Directory '{LOG_DIR}' exists but is not writable by the current user."
        # Redundant check (already done in test_log_file_absent) but guards against
        # race conditions if order changes.
        _assert_path_absent(LOG_FILE)
    else:
        # Directory does not exist — acceptable (it will be created later).
        assert True, "Log directory does not exist yet, which is acceptable."


def test_no_leftover_venv_bin_directory():
    """
    Guard against scenarios where only part of the virtual-env structure
    exists (e.g., /home/user/api_integration_env/bin without other parts).
    """
    partial_bin_path = os.path.join(VENV_DIR, "bin")
    _assert_path_absent(partial_bin_path)