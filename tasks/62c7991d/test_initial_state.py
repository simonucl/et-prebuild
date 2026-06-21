# test_initial_state.py
#
# This pytest suite validates the INITIAL state of the filesystem
# before the student performs any actions for the IoT-device bundle
# task.  Only the pre-existing artifacts are checked; no “output”
# paths that the student is supposed to create are referenced.

import pathlib
import pytest

FIRMWARE_PATH = pathlib.Path("/home/user/sample_firmware_v1.2.bin")
EXPECTED_CONTENT = b"a"  # single byte 0x61


def test_sample_firmware_exists():
    """
    The seed file /home/user/sample_firmware_v1.2.bin must exist and be
    a regular file before the student starts working.
    """
    assert FIRMWARE_PATH.exists(), (
        f"Expected file {FIRMWARE_PATH} is missing."
    )
    assert FIRMWARE_PATH.is_file(), (
        f"{FIRMWARE_PATH} exists but is not a regular file."
    )


def test_sample_firmware_size():
    """
    The firmware seed file must be exactly one byte long.
    """
    size = FIRMWARE_PATH.stat().st_size
    assert size == 1, (
        f"{FIRMWARE_PATH} should be exactly 1 byte, found {size} bytes."
    )


def test_sample_firmware_content():
    """
    The single byte inside the firmware seed file must be ASCII 'a'
    (hex 0x61) and nothing else.
    """
    content = FIRMWARE_PATH.read_bytes()
    assert content == EXPECTED_CONTENT, (
        f"Content mismatch in {FIRMWARE_PATH}: "
        f"expected {EXPECTED_CONTENT!r}, found {content!r}."
    )