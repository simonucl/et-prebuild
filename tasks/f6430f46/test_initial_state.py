# test_initial_state.py
#
# This pytest suite verifies the operating-system state *before* the
# student generates the audit log.  It confirms that all prerequisites
# are present and correct, and that the target log file does **not**
# yet exist.

import hashlib
import os
from pathlib import Path
import pytest


CERTS_DIR = Path("/home/user/compliance/certs")
AUDIT_TRAILS_DIR = Path("/home/user/compliance/audit/trails")
CERT_FILE = CERTS_DIR / "server.crt"
EXPECTED_SHA256 = (
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
)
TARGET_LOG = AUDIT_TRAILS_DIR / "cert_audit_2024-01-01.log"


def test_certs_directory_exists():
    assert CERTS_DIR.is_dir(), (
        f"Required directory missing: {CERTS_DIR}. "
        "The certificate directory must already exist."
    )


def test_certificate_file_exists_and_contents():
    assert CERT_FILE.is_file(), (
        f"Required certificate file missing: {CERT_FILE}."
    )

    data = CERT_FILE.read_bytes()
    # The staged certificate is exactly three bytes: b"abc"
    assert data == b"abc", (
        f"{CERT_FILE} exists but its contents are not the expected "
        f"bytes. Expected b'abc' (hex: 61 62 63), got {data!r}"
    )


def test_certificate_sha256_matches_expected():
    hasher = hashlib.sha256()
    with CERT_FILE.open("rb") as f:
        hasher.update(f.read())
    digest = hasher.hexdigest()
    assert digest == EXPECTED_SHA256, (
        f"SHA-256 digest of {CERT_FILE} is {digest}, "
        f"but expected {EXPECTED_SHA256}. "
        "The pre-staged certificate must be unmodified."
    )


def test_audit_trails_directory_exists_and_writable():
    assert AUDIT_TRAILS_DIR.is_dir(), (
        f"Required directory missing: {AUDIT_TRAILS_DIR}."
    )
    assert os.access(AUDIT_TRAILS_DIR, os.W_OK), (
        f"Directory {AUDIT_TRAILS_DIR} is not writable by the current user. "
        "It must be writable so the audit log can be created."
    )


def test_target_log_file_not_yet_present():
    assert not TARGET_LOG.exists(), (
        f"The audit log {TARGET_LOG} already exists, but it should *not* be "
        "present before the student runs their single command."
    )