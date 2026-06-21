# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state **before**
# the student starts working on the assignment.  It intentionally avoids
# checking for any output artefacts such as /home/user/backup_logs or its
# contents, because those are supposed to be created by the student.
#
# What it *does* check:
#   • /home/user/sample_data.txt must already exist.
#   • The file must contain exactly the three ASCII bytes 0x61 0x62 0x63 ("abc")
#     with NO trailing newline or other characters.
#   • The SHA-256 hash of the file must therefore be
#       ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
#
# Only standard-library modules are used so that the test runs everywhere.

import os
import hashlib
import stat
import pytest

SAMPLE_FILE = "/home/user/sample_data.txt"
EXPECTED_BYTES = b"abc"
EXPECTED_SHA256 = (
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
)


def test_sample_file_exists_and_is_regular():
    """The mandatory sample file must already exist and be a regular file."""
    assert os.path.exists(
        SAMPLE_FILE
    ), f"Required file {SAMPLE_FILE} does not exist."
    assert os.path.isfile(
        SAMPLE_FILE
    ), f"{SAMPLE_FILE} exists but is not a regular file."


def test_sample_file_permissions_are_reasonable():
    """
    The file should at least be readable by the current user so that the
    subsequent content checks can succeed.  We *do not* demand any specific
    mode beyond user-readability.
    """
    st = os.stat(SAMPLE_FILE)
    assert bool(st.st_mode & stat.S_IRUSR), (
        f"{SAMPLE_FILE} is not readable by the current user "
        f"(mode: {oct(st.st_mode & 0o777)})"
    )


def test_sample_file_exact_contents_and_length():
    """The file must contain exactly the three bytes 'abc' and nothing else."""
    with open(SAMPLE_FILE, "rb") as f:
        data = f.read()

    assert (
        data == EXPECTED_BYTES
    ), f"{SAMPLE_FILE} content mismatch: expected b'abc' exactly, got {data!r}"
    assert (
        len(data) == 3
    ), f"{SAMPLE_FILE} must be exactly 3 bytes long; got {len(data)} bytes."


def test_sample_file_sha256_matches_expected():
    """The SHA-256 checksum of the file must match the known good value."""
    h = hashlib.sha256()
    with open(SAMPLE_FILE, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    digest = h.hexdigest()

    assert (
        digest == EXPECTED_SHA256
    ), f"{SAMPLE_FILE} SHA-256 mismatch: expected {EXPECTED_SHA256}, got {digest}"