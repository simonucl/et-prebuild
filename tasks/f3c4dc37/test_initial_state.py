# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state *before*
# the student performs any actions for the IoT-edge firmware task.
#
# The tests purposely check only the pre-existing material inside
# /home/user/iot_workdir/source/edge and make **no reference** to the
# target output paths (/release, /staging, etc.).
#
# Should any assertion fail, the accompanying message pin-points exactly
# what is missing or malformed so the learner can investigate quickly.

import hashlib
import os
import stat
import pytest

BASE_DIR = "/home/user/iot_workdir/source/edge"
FIRMWARE_PATH = os.path.join(BASE_DIR, "firmware_v2.3.1.bin")
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
LICENSE_PATH = os.path.join(BASE_DIR, "LICENSE.txt")

EXPECTED_FIRMWARE_MD5 = "9e107d9d372bb6826bd81d3542a419d6"
EXPECTED_FIRMWARE_TEXT = b"The quick brown fox jumps over the lazy dog"  # 43 bytes, no LF
EXPECTED_LICENSE_SNIPPET = "MIT License"
EXPECTED_CONFIG_KEYS = [
    'version: "2.3.1"',
    'device: "EDGE-NODE-A1"',
    "- gpio",
    "- ble",
    "- wifi",
]


def _file_md5(path):
    """Return the hex MD5 digest of a file in a memory-efficient way."""
    hasher = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@pytest.mark.parametrize(
    "path",
    [
        BASE_DIR,
        FIRMWARE_PATH,
        CONFIG_PATH,
        LICENSE_PATH,
    ],
)
def test_paths_exist(path):
    assert os.path.exists(path), f"Expected path does not exist: {path}"


def test_base_dir_is_directory():
    assert os.path.isdir(BASE_DIR), f"{BASE_DIR} should be a directory"


def test_firmware_file_properties():
    assert os.path.isfile(FIRMWARE_PATH), f"{FIRMWARE_PATH} should be a regular file"

    # Verify file size is exactly 43 bytes
    size = os.stat(FIRMWARE_PATH).st_size
    assert size == 43, f"{FIRMWARE_PATH} should be 43 bytes, found {size}"

    # Check MD5 digest
    digest = _file_md5(FIRMWARE_PATH)
    assert (
        digest == EXPECTED_FIRMWARE_MD5
    ), f"MD5 mismatch for firmware: expected {EXPECTED_FIRMWARE_MD5}, got {digest}"

    # Check exact content (no trailing newline)
    with open(FIRMWARE_PATH, "rb") as fh:
        content = fh.read()
    assert (
        content == EXPECTED_FIRMWARE_TEXT
    ), f"Firmware file content is not the expected 43-byte ASCII string"


def test_config_yaml_contents():
    assert os.path.isfile(CONFIG_PATH), f"{CONFIG_PATH} should be a regular file"

    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        text = fh.read()

    # Basic sanity: must start with YAML start marker
    assert text.lstrip().startswith(
        "---"
    ), f"{CONFIG_PATH} should start with YAML document marker '---'"

    for snippet in EXPECTED_CONFIG_KEYS:
        assert (
            snippet in text
        ), f"{CONFIG_PATH} is missing expected line or key: '{snippet}'"


def test_license_file_content():
    assert os.path.isfile(LICENSE_PATH), f"{LICENSE_PATH} should be a regular file"
    with open(LICENSE_PATH, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert (
        EXPECTED_LICENSE_SNIPPET in content
    ), f"{LICENSE_PATH} should contain the text '{EXPECTED_LICENSE_SNIPPET}'"