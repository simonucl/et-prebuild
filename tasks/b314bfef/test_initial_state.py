# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system / filesystem
# state matches the specification **before** the student performs any action.
#
# IMPORTANT: If any of these tests fail it means the starting point is already
# wrong and the follow-up tasks cannot be graded reliably.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_file_mode(path: Path, expected_oct_perm: int) -> None:
    """
    Assert that the file at `path` has permission bits that match
    `expected_oct_perm` (e.g. 0o600).  Only permission bits are compared
    – ownership, special bits etc. are ignored.
    """
    actual_mode = stat.S_IMODE(path.stat().st_mode)
    assert actual_mode == expected_oct_perm, (
        f"{path} should have mode {oct(expected_oct_perm)}, "
        f"but has {oct(actual_mode)}"
    )

def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Tests for /home/user/secrets
# ---------------------------------------------------------------------------

def test_secrets_directory_exists_and_permissions():
    secrets_dir = HOME / "secrets"
    assert secrets_dir.is_dir(), f"Expected directory {secrets_dir} to exist."
    # 0o700 = rwx------  (only owner can read/write/execute)
    _assert_file_mode(secrets_dir, 0o700)

def test_db_credentials_file_exists_contents_and_permissions():
    cred_file = HOME / "secrets" / "db_credentials.txt"
    assert cred_file.is_file(), f"Expected file {cred_file} to exist."
    _assert_file_mode(cred_file, 0o600)  # rw------- (owner only)

    contents = _read_text(cred_file)
    expected_contents = "db_user=admin\ndb_password=Sup3rS3cr3t\n"
    assert contents == expected_contents, (
        f"{cred_file} contents do not match the expected template. "
        "Do not modify this file before encryption."
    )

def test_encrypted_credentials_file_absent_before_action():
    gpg_file = HOME / "secrets" / "db_credentials.txt.gpg"
    assert not gpg_file.exists(), (
        f"{gpg_file} should NOT exist before the encryption task is performed."
    )

# ---------------------------------------------------------------------------
# Tests for /home/user/incoming
# ---------------------------------------------------------------------------

def test_incoming_directory_exists():
    incoming_dir = HOME / "incoming"
    assert incoming_dir.is_dir(), f"Expected directory {incoming_dir} to exist."

def test_patch_tar_gz_exists_and_contents():
    patch_file = HOME / "incoming" / "patch_v1.tar.gz"
    assert patch_file.is_file(), f"Expected file {patch_file} to exist."

    contents = _read_text(patch_file)
    assert contents == "dummy patch content\n", (
        f"{patch_file} contents are not as expected. "
        "The grader relies on the file being the provided dummy content."
    )

def test_patch_detached_signature_exists_and_contents():
    sig_file = HOME / "incoming" / "patch_v1.tar.gz.asc"
    assert sig_file.is_file(), f"Expected file {sig_file} to exist."

    contents = _read_text(sig_file)
    expected_header = "-----BEGIN PGP SIGNATURE-----"
    expected_footer = "-----END PGP SIGNATURE-----"
    assert contents.startswith(expected_header), (
        f"{sig_file} does not start with '{expected_header}'."
    )
    assert contents.strip().endswith(expected_footer), (
        f"{sig_file} does not end with '{expected_footer}'."
    )

# ---------------------------------------------------------------------------
# Tests for /home/user/logs
# ---------------------------------------------------------------------------

def test_logs_directory_exists_and_clean():
    logs_dir = HOME / "logs"
    assert logs_dir.is_dir(), f"Expected directory {logs_dir} to exist."

    log_file = logs_dir / "patch_v1_verification.log"
    assert not log_file.exists(), (
        f"{log_file} should NOT exist before the signature verification task "
        "is executed."
    )