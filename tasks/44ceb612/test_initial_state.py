# test_initial_state.py
#
# This test-suite validates that the operating-system is in its **initial**
# (pre-task) state.  None of the artefacts that the student is asked to create
# during the challenge may already exist.

import os
import stat
from pathlib import Path
import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

PRIVATE_KEY = SSH_DIR / "id_ed25519_harden"
PUBLIC_KEY = SSH_DIR / "id_ed25519_harden.pub"
AUTHORIZED_KEYS = SSH_DIR / "authorized_keys"
LOG_FILE = HOME / "ssh_setup_log.txt"


def _octal_mode(path: Path) -> str:
    """
    Return the file's mode as a zero-padded 3-digit octal string,
    e.g. '600' or '644'.
    """
    mode = path.stat().st_mode & 0o777
    return f"{mode:03o}"


def test_private_key_does_not_exist():
    assert not PRIVATE_KEY.exists(), (
        f"Precondition failed: the private key '{PRIVATE_KEY}' must NOT exist "
        "before the student starts the task."
    )


def test_public_key_does_not_exist():
    assert not PUBLIC_KEY.exists(), (
        f"Precondition failed: the public key '{PUBLIC_KEY}' must NOT exist "
        "before the student starts the task."
    )


def test_authorized_keys_absent_or_clean():
    """
    The file may legitimately be absent.  If it exists already, it must NOT
    contain the comment that will belong to the new key the student is asked
    to add (“secure-harden@example.com”).
    """
    if not AUTHORIZED_KEYS.exists():
        pytest.skip("authorized_keys does not exist yet — OK for initial state")

    # File exists; ensure it is not already hardened.
    with AUTHORIZED_KEYS.open("r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    forbidden_comment = "secure-harden@example.com"
    assert forbidden_comment not in content, (
        f"Precondition failed: '{AUTHORIZED_KEYS}' already contains the comment "
        f"'{forbidden_comment}'.  The new key must NOT be present yet."
    )

    # Also ensure the existing file is not already locked down with 600
    # *specifically for the new key*.  Permission may vary; we therefore do NOT
    # assert on the mode here.  This note is only to clarify intent.


def test_log_file_does_not_exist():
    assert not LOG_FILE.exists(), (
        f"Precondition failed: the log file '{LOG_FILE}' must NOT exist before "
        "the student runs their setup commands."
    )


def test_no_stray_key_files():
    """
    Guard against the exact filenames showing up elsewhere under the user's
    home directory.  There must be no additional copies lying around.
    """
    stray_private = list(HOME.rglob("id_ed25519_harden"))
    stray_public = list(HOME.rglob("id_ed25519_harden.pub"))

    # Filter out the canonical paths we already test above (should not exist
    # either, but to keep the assertion messages clear).
    stray_private = [p for p in stray_private if p != PRIVATE_KEY]
    stray_public = [p for p in stray_public if p != PUBLIC_KEY]

    assert not stray_private, (
        "Precondition failed: found unexpected file(s) named "
        "'id_ed25519_harden' outside the target location:\n"
        + "\n".join(str(p) for p in stray_private)
    )
    assert not stray_public, (
        "Precondition failed: found unexpected file(s) named "
        "'id_ed25519_harden.pub' outside the target location:\n"
        + "\n".join(str(p) for p in stray_public)
    )