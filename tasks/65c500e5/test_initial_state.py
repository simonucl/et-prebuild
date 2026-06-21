# test_initial_state.py
#
# This pytest suite verifies that the starting filesystem/OS state
# exactly matches the specification *before* the student performs
# any actions.  If any test here fails, the exercise cannot be
# considered in its initial state.

import os
import stat
import textwrap
import pytest

HOME = "/home/user"
TARGET_FILE = os.path.join(HOME, "targets", "old_server_certificate.txt")
AUDIT_DIR = os.path.join(HOME, "audit")
LOG_FILE = os.path.join(AUDIT_DIR, "cert_scan.log")


# The precise, canonical content that must already be present in
# /home/user/targets/old_server_certificate.txt.  Note that:
#   * Every space and newline is significant.
#   * The block ends with a single trailing newline.
EXPECTED_CERT_DUMP = (
    "Certificate:\n"
    "    Data:\n"
    "        Version: 3 (0x2)\n"
    "        Serial Number:\n"
    "            04:00:00:00:00:01 (268435457)\n"
    "    Signature Algorithm: sha256WithRSAEncryption\n"
    "        Issuer: CN=Old Vulnerable Server\n"
    "        Validity\n"
    "            Not Before: Apr  1 00:00:00 2022 GMT\n"
    "            Not After : Apr  1 00:00:00 2023 GMT\n"
    "        Subject: CN=Old Vulnerable Server\n"
    "        Subject Public Key Info:\n"
    "            Public Key Algorithm: rsaEncryption\n"
    "                Public-Key: (2048 bit)\n"
    "                Modulus:\n"
    "                    00:c6:33:24:2a:4c:5e:3b:c5:70:b0...\n"
    "                Exponent: 65537 (0x10001)\n"
    "        X509v3 extensions:\n"
    "            X509v3 Basic Constraints:\n"
    "                CA:TRUE\n"
    "            X509v3 Key Usage: critical\n"
    "                Digital Signature, Key Cert Sign, CRL Sign\n"
    "    Signature Algorithm: sha256WithRSAEncryption\n"
    "         53:71:a1:9a:ce:9b:9a:8c:44:6b:c4:49:73:41:69...\n"
    "-----END CERTIFICATE-----\n"
)


def test_target_file_exists_and_is_regular():
    """Verify that the certificate dump file exists and is a regular file."""
    assert os.path.exists(
        TARGET_FILE
    ), f"Expected {TARGET_FILE} to exist, but it is missing."

    assert os.path.isfile(
        TARGET_FILE
    ), f"Expected {TARGET_FILE} to be a regular file."


def test_target_file_permissions():
    """Basic sanity-check: file must be readable by the current user."""
    st = os.stat(TARGET_FILE)
    readable = bool(st.st_mode & stat.S_IRUSR)
    assert readable, f"{TARGET_FILE} exists but is not readable by the current user."


def test_target_file_content_exact_match():
    """
    The provided certificate dump must match the canonical text byte-for-byte.
    This guards against accidental editing, DOS/Unix line-ending issues,
    or other corruption before the student starts.
    """
    with open(TARGET_FILE, "r", encoding="utf-8") as fh:
        actual = fh.read()

    assert (
        actual == EXPECTED_CERT_DUMP
    ), (
        "The content of {0} does not match the expected initial certificate dump.\n"
        "If this file was modified, restore it to the exact original contents.".format(
            TARGET_FILE
        )
    )


def test_audit_directory_exists_and_is_empty():
    """The /home/user/audit directory must exist, be a directory, and be empty."""
    assert os.path.exists(
        AUDIT_DIR
    ), f"Expected directory {AUDIT_DIR} to exist, but it is missing."
    assert os.path.isdir(
        AUDIT_DIR
    ), f"{AUDIT_DIR} exists but is not a directory."

    # Gather non-hidden entries (ignore . and .. and dotfiles)
    non_hidden_entries = [
        entry
        for entry in os.listdir(AUDIT_DIR)
        if entry not in (".", "..") and not entry.startswith(".")
    ]
    assert (
        not non_hidden_entries
    ), f"{AUDIT_DIR} should be empty at the start, but contains: {non_hidden_entries}"


def test_log_file_absent_initially():
    """The cert_scan.log file must NOT exist before the student creates it."""
    assert not os.path.exists(
        LOG_FILE
    ), f"{LOG_FILE} already exists, but it must be created by the student's solution."