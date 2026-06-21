# test_initial_state.py
#
# This pytest suite validates that the system is in a **clean / initial**
# state *before* the student begins the “policy-as-code” exercise.
#
# NONE of the artefacts that the task asks the student to create should
# be present yet.  If any of them already exist, the initial-state check
# must fail so that the learner starts from a known baseline.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _assert_absent(path: Path):
    """
    Assert that the given path does not exist.

    Parameters
    ----------
    path : Path
        Absolute path that must be absent.

    Raises
    ------
    AssertionError
        If the path exists (file, directory, symlink … whatever).
    """
    assert not path.exists(), (
        f"Initial-state check failed: '{path}' SHOULD NOT exist yet.\n"
        f"Remove it so the policy-as-code exercise starts from a clean state."
    )

# ----------------------------------------------------------------------
# Tests for the initial (pre-exercise) state
# ----------------------------------------------------------------------
def test_private_key_absent():
    """
    Private key MUST NOT exist before the learner generates it.
    """
    _assert_absent(SSH_DIR / "id_ed25519_devsecops_policy")


def test_public_key_absent():
    """
    Public key MUST NOT exist before the learner generates it.
    """
    _assert_absent(SSH_DIR / "id_ed25519_devsecops_policy.pub")


def test_policy_config_absent():
    """
    The per-host configuration snippet must not exist yet.
    """
    _assert_absent(SSH_DIR / "config.d" / "policy_config")


def test_log_file_absent():
    """
    The audit / log file must not pre-exist.
    """
    _assert_absent(HOME / "ssh_key_policy_setup.log")


def test_manifest_absent():
    """
    The YAML manifest must not pre-exist.
    """
    _assert_absent(HOME / "policy_manifest.yaml")