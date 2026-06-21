# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before** the
# student starts the credential-rotation task.  It makes sure that:
#
#   • The three prerequisite files are present and correct.
#   • None of the files/directories that the student is supposed to create
#     during the rotation process already exist.
#
# Any failing test gives a clear, actionable message.

import os
import pytest
from pathlib import Path

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Read file as UTF-8 text and return its contents."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()

# ---------------------------------------------------------------------------
# Paths that *must* already exist
# ---------------------------------------------------------------------------

OLD_CREDS = HOME / ".config/privrepo/creds.conf"
OLD_KEY   = HOME / ".config/apt/trusted.gpg.d/privrepo_old.gpg"
NEW_KEY   = HOME / "keys/new_privrepo.gpg"

# ---------------------------------------------------------------------------
# Paths that *must NOT* exist yet
# ---------------------------------------------------------------------------

SHOULD_NOT_EXIST = [
    HOME / ".config/privrepo/creds.conf.old",
    HOME / ".config/privrepo/creds.conf.bak",
    HOME / ".config/apt/auth.conf.d/privrepo.conf",
    HOME / ".config/apt/sources.list.d/privrepo.list",
    HOME / ".config/apt/preferences.d/privrepo.pref",
    HOME / ".config/apt/trusted.gpg.d/privrepo.gpg",
    HOME / "rotation_logs",
    HOME / "rotation_logs/2024-credential-rotation.log",
]

# ---------------------------------------------------------------------------
# Tests for the pre-existing items
# ---------------------------------------------------------------------------

def test_old_credential_file_present_and_correct():
    assert OLD_CREDS.is_file(), (
        f"Missing old credentials file at {OLD_CREDS}. "
        "It should contain the 2023 token so the student can back it up."
    )

    expected = "token=OLD-TOKEN-2023\n"
    actual   = read_text(OLD_CREDS)
    assert actual == expected, (
        f"Unexpected content in {OLD_CREDS}.\n"
        f"Expected: {expected!r}\n"
        f"  Actual: {actual!r}"
    )

def test_old_signing_key_exists():
    assert OLD_KEY.is_file(), (
        f"Expected old signing key at {OLD_KEY} to be present so the student "
        "can leave it untouched during the rotation."
    )
    # Spot-check that it *looks* like a GPG key
    header = read_text(OLD_KEY).splitlines()[0]
    assert header.startswith("-----BEGIN PGP PUBLIC KEY BLOCK-----"), (
        f"{OLD_KEY} does not appear to be an ASCII-armoured GPG key."
    )

def test_new_signing_key_to_install_exists():
    assert NEW_KEY.is_file(), (
        f"New signing key that the student must install is missing at {NEW_KEY}."
    )
    header = read_text(NEW_KEY).splitlines()[0]
    assert header.startswith("-----BEGIN PGP PUBLIC KEY BLOCK-----"), (
        f"{NEW_KEY} does not appear to be an ASCII-armoured GPG key."
    )

# ---------------------------------------------------------------------------
# Tests for items that must *not* exist yet
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", SHOULD_NOT_EXIST, ids=lambda p: str(p))
def test_no_future_files_or_dirs_exist_yet(path: Path):
    assert not path.exists(), (
        f"{path} already exists, but it should be created **by the student** "
        "during the credential rotation process."
    )