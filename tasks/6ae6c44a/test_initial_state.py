# test_initial_state.py
#
# Pytest suite that validates the operating-system / file-system *before*
# the student performs any actions for the “backup-integrity” exercise.
#
# It confirms that:
#   1. The three seed files exist under /home/user/data_backup/2023-11-01
#      with the exact byte contents (verified via SHA-256 digests).
#   2. No SSH key-pair for “backup_audit” is present yet.
#   3. No integrity-report artefacts exist yet.
#
# The tests purposefully **fail** if the system is in an unexpected state,
# giving clear, actionable messages.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DATA_ROOT = HOME / "data_backup"
SEED_DIR = DATA_ROOT / "2023-11-01"
SSH_DIR = HOME / ".ssh"
PRIV_KEY = SSH_DIR / "backup_audit_ed25519"
PUB_KEY = SSH_DIR / "backup_audit_ed25519.pub"
INTEGRITY_DIR = HOME / "backup_integrity"
AUTHORIZED_KEYS = INTEGRITY_DIR / "authorized_keys"
FINGERPRINT_TXT = INTEGRITY_DIR / "ssh_fingerprint.txt"
INTEGRITY_LOG = INTEGRITY_DIR / "integrity_report.log"

EXPECTED_HASHES = {
    "2023-11-01/db.sql": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    "2023-11-01/photos.tar.gz": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    "2023-11-01/docs.zip": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def sha256_of_file(path: Path) -> str:
    """Return lower-case hex SHA-256 digest of a file’s bytes."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _assert_absent(path: Path):
    assert not path.exists(), f"Pre-state error: {path} already exists but must be absent before you start."


@pytest.mark.parametrize("relative_path,expected_digest", sorted(EXPECTED_HASHES.items()))
def test_seed_file_exists_and_matches_hash(relative_path: str, expected_digest: str):
    """
    Each seed file must exist and have the exact expected SHA-256 digest.
    This guarantees the student starts from a clean, known data set.
    """
    full_path = DATA_ROOT / relative_path
    assert full_path.is_file(), f"Required seed file missing: {full_path}"
    observed_digest = sha256_of_file(full_path)
    assert (
        observed_digest == expected_digest
    ), f"{full_path} has unexpected contents.\nExpected digest: {expected_digest}\nObserved digest: {observed_digest}"


def test_no_backup_audit_key_pair_yet():
    """
    The ED25519 key-pair for “backup_audit” must NOT exist before the task starts.
    """
    _assert_absent(PRIV_KEY)
    _assert_absent(PUB_KEY)


def test_no_integrity_outputs_yet():
    """
    The artefacts that the student is supposed to create later must not pre-exist.
    """
    _assert_absent(AUTHORIZED_KEYS)
    _assert_absent(FINGERPRINT_TXT)
    _assert_absent(INTEGRITY_LOG)