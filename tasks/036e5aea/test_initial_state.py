# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state
# before the student performs any actions for the “artifact-manager”
# exercise.  It checks only what should already be present and makes
# no assertions about files/directories that will be created later.

from pathlib import Path
import pytest

HOME = Path("/home/user")
AM_ROOT = HOME / "artifact-manager"
REPOS_DIR = AM_ROOT / "repos"
CONF_FILE = AM_ROOT / "artifact-manager.conf"

EXPECTED_CONF_CONTENT = (
    "# Artifact Manager Configuration\n"
    "[global]\n"
    "storage_root = /home/user/artifact-manager/repos\n"
)


def test_artifact_manager_directory_structure():
    """
    The base artifact-manager directory hierarchy must already exist.
    """
    assert AM_ROOT.exists(), (
        f"Required directory missing: {AM_ROOT}\n"
        "Create this directory before proceeding with the task."
    )
    assert AM_ROOT.is_dir(), (
        f"{AM_ROOT} exists but is not a directory."
    )

    assert REPOS_DIR.exists(), (
        f"Required directory missing: {REPOS_DIR}\n"
        "Create this directory before proceeding with the task."
    )
    assert REPOS_DIR.is_dir(), (
        f"{REPOS_DIR} exists but is not a directory."
    )


def test_configuration_file_presence_and_content():
    """
    The configuration file must exist and contain exactly the expected
    three lines (including trailing newlines).
    """
    assert CONF_FILE.exists(), (
        f"Configuration file missing: {CONF_FILE}\n"
        "It must be present **before** you begin modifying it."
    )
    assert CONF_FILE.is_file(), f"{CONF_FILE} exists but is not a regular file."

    content = CONF_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_CONF_CONTENT, (
        f"{CONF_FILE} content is not in the expected initial state.\n"
        "Expected exactly:\n"
        "--------------------\n"
        f"{EXPECTED_CONF_CONTENT}"
        "--------------------\n"
        "Do not modify the existing lines; only append new ones during the task."
    )