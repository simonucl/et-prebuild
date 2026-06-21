# test_initial_state.py
#
# Pytest suite to validate the operating-system / filesystem *before*
# the student’s provisioning script is run.
#
# Checks performed (all paths are absolute):
#   1. /home/user/new-certs/ exists and is a directory.
#   2. /home/user/new-certs/ has POSIX permissions 0o755.
#   3. /home/user/new-certs/internal.pem
#        • exists and is a regular file
#        • has POSIX permissions 0o644 (or more restrictive)
#        • is exactly 3 bytes long
#        • contains the ASCII string “abc”
#        • has the expected SHA-256 digest
#   4. /home/user/new-certs/ contains *only* the file internal.pem
#
# NOTE:  The specification explicitly forbids testing for the presence or
#        absence of any *output* paths (e.g. /home/user/managed-certs/),
#        so this file makes no assertions about them.

import hashlib
import os
import stat
import pytest

NEW_CERTS_DIR = "/home/user/new-certs"
INTERNAL_PEM   = os.path.join(NEW_CERTS_DIR, "internal.pem")
EXPECTED_SHA256 = (
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
)
EXPECTED_CONTENT = b"abc"
DIR_PERMS = 0o755
FILE_PERMS = 0o644


def _octal_permissions(path):
    """
    Return the permission bits (e.g. 0o755) of the path, independent of the
    file type bits.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


def test_new_certs_directory_exists_and_has_correct_permissions():
    assert os.path.isdir(NEW_CERTS_DIR), (
        f"Required directory {NEW_CERTS_DIR} is missing or not a directory."
    )

    perms = _octal_permissions(NEW_CERTS_DIR)
    assert perms == DIR_PERMS, (
        f"{NEW_CERTS_DIR} should have permissions {oct(DIR_PERMS)}, "
        f"but has {oct(perms)}."
    )


def test_only_internal_pem_present_in_new_certs():
    contents = sorted(os.listdir(NEW_CERTS_DIR))
    assert contents == ["internal.pem"], (
        f"{NEW_CERTS_DIR} should contain only 'internal.pem' initially. "
        f"Current contents: {contents}"
    )


def test_internal_pem_file_properties():
    # Existence and file type
    assert os.path.isfile(INTERNAL_PEM), (
        f"Required file {INTERNAL_PEM} does not exist."
    )

    # Permissions (must be exactly 644 or stricter)
    perms = _octal_permissions(INTERNAL_PEM)
    assert perms <= FILE_PERMS, (
        f"{INTERNAL_PEM} should have permissions {oct(FILE_PERMS)} or more "
        f"restrictive, but has {oct(perms)}."
    )

    # Size and content
    size = os.path.getsize(INTERNAL_PEM)
    assert size == 3, (
        f"{INTERNAL_PEM} should be exactly 3 bytes, but is {size} bytes."
    )

    with open(INTERNAL_PEM, "rb") as fp:
        data = fp.read()

    assert data == EXPECTED_CONTENT, (
        f"{INTERNAL_PEM} content is {data!r}; expected {EXPECTED_CONTENT!r}."
    )

    # SHA-256 checksum
    sha256 = hashlib.sha256(data).hexdigest()
    assert sha256 == EXPECTED_SHA256, (
        f"SHA-256 of {INTERNAL_PEM} is {sha256}, expected {EXPECTED_SHA256}."
    )