# test_initial_state.py
#
# Pytest suite to verify the initial, pre-task state of the operating system
# for the “webdev_venv” exercise.
#
# These tests intentionally confirm that NOTHING from the expected end-state
# (virtual-environment directory, its sub-structure, or the confirmation log
# file) is present before the student performs any action.
#
# Only the standard library and pytest are used.

import os
from pathlib import Path

HOME_DIR = Path("/home/user")
VENV_DIR = HOME_DIR / "webdev_venv"
LOG_FILE = HOME_DIR / "venv_created.log"


def test_home_directory_exists():
    """
    Sanity check: the user's home directory must exist.
    """
    assert HOME_DIR.is_dir(), (
        f"Expected home directory {HOME_DIR} to exist, "
        "but it is missing. The test environment is mis-configured."
    )


def test_virtualenv_directory_absent():
    """
    The virtual-environment directory must NOT exist yet.
    """
    assert not VENV_DIR.exists(), (
        f"The directory {VENV_DIR} already exists, but the virtual "
        "environment should be created by the student later. "
        "Ensure you are starting from a clean state."
    )


def test_virtualenv_substructure_absent():
    """
    Even if someone accidentally created partial structure, make sure
    the typical venv contents are absent.
    """
    expected_items = [
        VENV_DIR / "bin",
        VENV_DIR / "lib",
        VENV_DIR / "pyvenv.cfg",
    ]
    for item in expected_items:
        assert not item.exists(), (
            f"Found unexpected item {item}. The virtual environment seems to "
            "have been (partially) created already; start from a clean state."
        )


def test_log_file_absent():
    """
    The confirmation log file must NOT exist before the task is performed.
    """
    assert not LOG_FILE.exists(), (
        f"The log file {LOG_FILE} already exists, but it should be generated "
        "only after the virtual environment is created."
    )