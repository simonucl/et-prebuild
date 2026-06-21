# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the operating system / file-
system for the checksum-generation exercise.

Only pre-existing artefacts are tested.  Nothing related to the student’s
expected output (e.g., /home/user/logs or its contents) is asserted here.
"""

import hashlib
from pathlib import Path

# Constants for the known-good initial state
HOME = Path("/home/user")
PAYLOAD = HOME / "sample_data" / "testfile.txt"
EXPECTED_SHA256 = (
    "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
)


def test_payload_file_exists_and_is_regular():
    """
    The payload file must already be present and be a regular file.
    """
    assert PAYLOAD.exists(), (
        f"Expected payload file '{PAYLOAD}' to exist, but it is missing."
    )
    assert PAYLOAD.is_file(), (
        f"Expected '{PAYLOAD}' to be a regular file, "
        f"but it is not (might be a directory, symlink, etc.)."
    )


def test_payload_file_content_and_size():
    """
    The payload must contain exactly one byte: the ASCII letter 'a'
    with no trailing newline.
    """
    data = PAYLOAD.read_bytes()
    assert len(data) == 1, (
        f"'{PAYLOAD}' should be exactly 1 byte long, "
        f"but found {len(data)} bytes."
    )
    assert data == b"a", (
        f"'{PAYLOAD}' should contain the single byte 0x61 ('a'), "
        f"but found bytes: {data!r}"
    )


def test_payload_sha256_checksum():
    """
    The SHA-256 checksum of the payload must match the canonical value.
    """
    digest = hashlib.sha256(PAYLOAD.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256, (
        "SHA-256 mismatch for the payload file.\n"
        f"Expected : {EXPECTED_SHA256}\n"
        f"Calculated: {digest}"
    )