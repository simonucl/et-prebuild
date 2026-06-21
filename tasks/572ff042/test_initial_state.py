# test_initial_state.py
#
# Pytest suite that verifies the initial state of the filesystem
# for the “IoT fleet” exercise _before_ the student’s shell commands
# are executed.  It checks only the directories and files that are
# guaranteed to exist at the beginning and deliberately avoids looking
# for any of the files or folders that the student is expected to
# create later (archive dir, log files, *.json.gz, etc.).

import os
from pathlib import Path

import pytest

# Base directory that must already be present
BASE = Path("/home/user/iot_fleet").resolve()

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def assert_is_dir(path: Path) -> None:
    """Fail with a clear message if *path* is not an existing directory."""
    assert path.exists(), f"Expected directory {path} to exist, but it is missing."
    assert path.is_dir(), f"Expected {path} to be a directory, but it is not."

def assert_is_file(path: Path) -> None:
    """Fail with a clear message if *path* is not an existing regular file."""
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file, but it is not."


# ----------------------------------------------------------------------
# 1. Top-level directory structure
# ----------------------------------------------------------------------
def test_base_directories_exist():
    required_dirs = [
        BASE,
        BASE / "firmware_packages",
        BASE / "devices_info",
        BASE / "deployment_logs",
    ]
    for d in required_dirs:
        assert_is_dir(d)


# ----------------------------------------------------------------------
# 2. Firmware files: presence and exact file list
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "filename",
    [
        "sensorA_v1.2.fw",
        "sensorA_v3.1.fw",
        "camB_v2.9.fw",
        "camB_v3.0.fw",
        "gateway_v2.5.fw",
        "gateway_v3.2.fw",
    ],
)
def test_each_firmware_file_exists(filename):
    fw_path = BASE / "firmware_packages" / filename
    assert_is_file(fw_path)
    # Zero-byte firmware images would be suspicious.
    assert fw_path.stat().st_size > 0, f"Firmware file {fw_path} is empty."

def test_no_extra_firmware_files_present():
    expected = {
        "sensorA_v1.2.fw",
        "sensorA_v3.1.fw",
        "camB_v2.9.fw",
        "camB_v3.0.fw",
        "gateway_v2.5.fw",
        "gateway_v3.2.fw",
    }
    fw_dir = BASE / "firmware_packages"
    found = {p.name for p in fw_dir.iterdir() if p.is_file()}
    assert found == expected, (
        "The set of firmware files in "
        f"{fw_dir} does not match the expected initial set.\n"
        f"Expected only: {sorted(expected)}\n"
        f"Found instead: {sorted(found)}"
    )


# ----------------------------------------------------------------------
# 3. Device JSON files: presence and size checks
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "filename, min_size_bytes, size_relation_description",
    [
        ("sensorA.json", 1024, "larger than 1024 bytes"),   # ≈1500 bytes
        ("camB.json",    1024, "smaller or equal to 1024 bytes"),  # ≈800 bytes
        ("gateway.json", 1024, "larger than 1024 bytes"),   # ≈2048 bytes
        ("edgeHub.json", 1024, "larger than 1024 bytes"),   # ≈3000 bytes
    ],
)
def test_json_files_exist_and_sizes(filename, min_size_bytes, size_relation_description):
    json_path = BASE / "devices_info" / filename
    assert_is_file(json_path)

    size = json_path.stat().st_size
    if "larger" in size_relation_description:
        assert (
            size > min_size_bytes
        ), f"Expected {json_path} to be {size_relation_description}, but its size is {size} bytes."
    else:
        # smaller or equal
        assert (
            size <= min_size_bytes
        ), f"Expected {json_path} to be {size_relation_description}, but its size is {size} bytes."