# test_initial_state.py
#
# This test-suite validates that the operating-system is in a pristine
# state *before* the learner generates the single-purpose SSH key-pair
# required for the integration tests.  Nothing related to the key-pair,
# its registration, or the JSON log file should exist yet.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
PRIVATE_KEY = SSH_DIR / "id_api_integration"
PUBLIC_KEY = SSH_DIR / "id_api_integration.pub"
AUTH_KEYS = SSH_DIR / "authorized_keys"
LOG_FILE = HOME / "ssh_setup.log"

# ------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------


def _mode(path: Path) -> int:
    """
    Return a file's permission bits (the lower 12 bits produced by `stat`).
    """
    return path.stat().st_mode & 0o7777


# ------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------


def test_ssh_dir_precondition():
    """
    The ~/.ssh directory should either be absent or already have 0700
    permissions (drwx------).  If it exists with weaker permissions,
    the pre-condition fails because it would interfere with secure key
    generation.
    """
    if SSH_DIR.exists():
        assert SSH_DIR.is_dir(), (
            f"{SSH_DIR} exists but is not a directory; please clean up the "
            "environment before proceeding."
        )
        assert _mode(SSH_DIR) == 0o700, (
            f"{SSH_DIR} exists with permissions {_mode(SSH_DIR):o}; expected "
            "0700 to keep SSH secure."
        )


@pytest.mark.parametrize(
    "path,description",
    [
        (PRIVATE_KEY, "Ed25519 private key"),
        (PUBLIC_KEY, "Ed25519 public key"),
        (LOG_FILE, "one-line JSON log file"),
    ],
)
def test_key_material_absent(path: Path, description: str):
    """
    None of the artefacts that the learner is expected to create should
    be present yet.
    """
    assert not path.exists(), (
        f"Unexpected {description} found at {path}.  The environment must "
        "start clean so the upcoming task can create it from scratch."
    )


def test_authorized_keys_clean():
    """
    If ~/.ssh/authorized_keys already exists, it must *not* yet contain
    an entry with the comment 'integration-dev@example.com'.  The learner
    will be responsible for appending exactly one such line.
    """
    if AUTH_KEYS.exists():
        assert AUTH_KEYS.is_file(), (
            f"{AUTH_KEYS} exists but is not a regular file; cannot proceed."
        )
        with AUTH_KEYS.open("r", encoding="utf-8") as fh:
            for ln in fh:
                assert "integration-dev@example.com" not in ln, (
                    f"Found a pre-existing key line with the comment "
                    "'integration-dev@example.com' in {AUTH_KEYS}; the file "
                    "must not yet contain that entry."
                )