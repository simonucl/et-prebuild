# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / file-system
# state before the student performs any actions for the “firmware checksum”
# exercise.
#
# ONLY the stdlib and pytest are used.
#
# What is verified:
#   1. /home/user/support  directory exists and is accessible.
#   2. /home/user/support/firmware_v2.1.0.bin
#        - exists as a regular file
#        - is exactly 0 bytes
#        - has the correct SHA-256 digest for an empty file
#   3. /home/user/support/reference.sha256
#        - exists as a regular file
#        - contains exactly one line with the expected digest/filename pair
#          and a single trailing newline
#   4. Neither /home/user/support/checksums.log nor
#      /home/user/support/verification.log should exist yet.
#
# Each assertion includes a helpful error message so that a failure pinpoints
# the specific precondition that is not met.

import hashlib
import os
import stat
import pytest

SUPPORT_DIR = "/home/user/support"
FIRMWARE_PATH = os.path.join(SUPPORT_DIR, "firmware_v2.1.0.bin")
REFERENCE_PATH = os.path.join(SUPPORT_DIR, "reference.sha256")
CHECKSUM_LOG = os.path.join(SUPPORT_DIR, "checksums.log")
VERIFICATION_LOG = os.path.join(SUPPORT_DIR, "verification.log")

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)
REFERENCE_LINE = (
    f"{EMPTY_SHA256}  firmware_v2.1.0.bin\n"
)


def test_support_directory_exists():
    assert os.path.isdir(SUPPORT_DIR), (
        f"Required directory {SUPPORT_DIR} is missing or is not a directory."
    )

    # Basic permission sanity: ensure owner can read/execute the directory
    st = os.stat(SUPPORT_DIR)
    assert bool(st.st_mode & stat.S_IRUSR), (
        f"Directory {SUPPORT_DIR} is not readable by the owner."
    )
    assert bool(st.st_mode & stat.S_IXUSR), (
        f"Directory {SUPPORT_DIR} is not accessible (execute bit missing)."
    )


def test_firmware_file_properties():
    assert os.path.isfile(FIRMWARE_PATH), (
        f"Firmware file {FIRMWARE_PATH} is missing or is not a regular file."
    )

    size = os.path.getsize(FIRMWARE_PATH)
    assert size == 0, (
        f"Firmware file {FIRMWARE_PATH} should be empty (0 bytes) "
        f"but is {size} bytes."
    )

    # Compute SHA-256 digest
    hasher = hashlib.sha256()
    with open(FIRMWARE_PATH, "rb") as fp:
        hasher.update(fp.read())
    digest = hasher.hexdigest()

    assert digest == EMPTY_SHA256, (
        f"SHA-256 digest of {FIRMWARE_PATH} is {digest}, "
        f"expected {EMPTY_SHA256}."
    )


def test_reference_sha256_file_contents():
    assert os.path.isfile(REFERENCE_PATH), (
        f"Reference checksum file {REFERENCE_PATH} is missing or is not a "
        f"regular file."
    )

    with open(REFERENCE_PATH, "rb") as fp:
        content = fp.read()

    assert content == REFERENCE_LINE.encode(), (
        f"Contents of {REFERENCE_PATH} are incorrect.\n"
        f"Expected exactly:\n{REFERENCE_LINE!r}\n"
        f"Actual content:\n{content!r}"
    )

    # Ensure single line (i.e., only one newline character, at the end)
    num_newlines = content.count(b"\n")
    assert num_newlines == 1, (
        f"{REFERENCE_PATH} should contain exactly one newline, found "
        f"{num_newlines}."
    )


@pytest.mark.parametrize("path", [CHECKSUM_LOG, VERIFICATION_LOG])
def test_output_files_do_not_exist_yet(path):
    assert not os.path.exists(path), (
        f"Output file {path} should NOT exist before the student runs their "
        f"solution, but it is already present."
    )