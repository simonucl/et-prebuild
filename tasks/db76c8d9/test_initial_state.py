# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# before the student performs any action for the “auditable checksum” task.
#
# What we expect to be present *right now*:
#   1. A file  /home/user/documents/policy.txt   whose *exact* byte contents are
#      the three ASCII characters “abc” (no trailing newline or other bytes).
#
# What we intentionally do *not* check for (because they are OUTPUT artifacts):
#   • /home/user/audit/                (directory)
#   • /home/user/audit/policy_checksum.log  (log file)
#
# Any failure message should clearly state what is missing or incorrect.
#
# Only stdlib + pytest are used.

import hashlib
from pathlib import Path

POLICY_PATH = Path("/home/user/documents/policy.txt")
EXPECTED_BYTES = b"abc"
EXPECTED_SHA256_HEX = (
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
)


def test_policy_file_exists_as_regular_file():
    """
    The policy file must exist as a regular file at the exact absolute path
    /home/user/documents/policy.txt.
    """
    assert POLICY_PATH.exists(), (
        f"Expected file {POLICY_PATH} to exist but it does not."
    )
    assert POLICY_PATH.is_file(), (
        f"Expected {POLICY_PATH} to be a regular file, "
        "but it is not (it may be a directory, symlink, etc.)."
    )


def test_policy_file_contents_are_exact_and_match_known_checksum():
    """
    The file must contain exactly the bytes 'abc' (no newline).  We additionally
    compute its SHA-256 digest to guard against invisible differences.
    """
    data = POLICY_PATH.read_bytes()

    # 1. Exact byte-for-byte comparison.
    assert data == EXPECTED_BYTES, (
        f"{POLICY_PATH} must contain the three bytes b'abc' with no newline.\n"
        f"Found {len(data)} bytes: {data!r}"
    )

    # 2. Confirm checksum for completeness.
    sha256_hex = hashlib.sha256(data).hexdigest()
    assert sha256_hex == EXPECTED_SHA256_HEX, (
        f"SHA-256 checksum of {POLICY_PATH} is {sha256_hex}, "
        f"but expected {EXPECTED_SHA256_HEX}.  File contents are incorrect."
    )