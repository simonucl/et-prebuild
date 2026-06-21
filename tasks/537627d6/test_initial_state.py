# test_initial_state.py
"""
Pytest suite that validates the **initial** filesystem state before the
student begins working on the “k8s-operator” exercise.

According to the exercise instructions, *nothing* related to the new
workspace should exist yet.  These tests fail early if remnants of a
previous run (or a pre-populated solution) are detected.

Only the Python standard library and pytest are used.
"""

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user").resolve()
WORKSPACE = HOME / "k8s-operator"
STAGING = WORKSPACE / "staging"

MANIFEST_FILES = [
    WORKSPACE / "nginx-deployment.yaml",
    WORKSPACE / "nginx-service.yaml",
    WORKSPACE / "kustomization.yaml",
]

LOG_FILE = WORKSPACE / "manifest_linecount.log"


def test_user_home_exists():
    """Sanity-check that the /home/user directory itself exists."""
    assert HOME.is_dir(), (
        f"Expected user home directory {HOME} to exist, "
        "but it does not. The test environment is mis-configured."
    )


def test_workspace_directory_absent():
    """
    The /home/user/k8s-operator directory must NOT exist yet.
    The student will create it during the exercise.
    """
    assert not WORKSPACE.exists(), (
        f"Found unexpected directory {WORKSPACE}. "
        "Start from a clean slate before beginning the task."
    )


@pytest.mark.parametrize("path", MANIFEST_FILES)
def test_manifest_files_absent(path):
    """
    None of the Kubernetes manifest files should exist prior to the task.
    """
    assert not path.exists(), (
        f"Found unexpected file {path}. "
        "The workspace must start empty."
    )


def test_log_file_absent():
    """
    The integrity log must not exist at the outset.
    """
    assert not LOG_FILE.exists(), (
        f"Found unexpected file {LOG_FILE}. "
        "The workspace must start empty."
    )


def test_staging_directory_absent():
    """
    The staging sub-directory should not be present yet.
    """
    assert not STAGING.exists(), (
        f"Found unexpected directory {STAGING}. "
        "The workspace must start empty."
    )