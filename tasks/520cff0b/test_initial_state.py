# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before**
the student performs any work on the OTA-update exercise.

Only the pre-existing CSV inventory is checked; we *do not* test for any of the
files that the student is expected to create later on.

Requirements being verified:
1. /home/user/iot_devices directory exists.
2. /home/user/iot_devices/device_registry.csv is present and readable.
3. The CSV file:
   • Ends with a single trailing newline (and not two).
   • Contains exactly one header row plus five data rows (6 lines total).
   • Header row is precisely
       device_id,mac_addr,location,firmware
   • Device rows are for dev-001 … dev-005, in that order.
   • Firmware versions are distributed as:
       1.2.3 → 3 devices
       1.2.2 → 1 device
       1.2.1 → 1 device
"""

import os
import pathlib
import pytest
import re

IOT_DIR = pathlib.Path("/home/user/iot_devices")
CSV_PATH = IOT_DIR / "device_registry.csv"


def test_iot_directory_exists():
    """Ensure the base directory is present and is a directory."""
    assert IOT_DIR.exists(), f"Required directory {IOT_DIR} is missing."
    assert IOT_DIR.is_dir(), f"{IOT_DIR} exists but is not a directory."


def test_csv_file_exists_and_readable():
    """The inventory CSV must exist and be a regular readable file."""
    assert CSV_PATH.exists(), f"Required file {CSV_PATH} is missing."
    assert CSV_PATH.is_file(), f"{CSV_PATH} exists but is not a regular file."
    # Attempt to open the file to ensure readability.
    with open(CSV_PATH, "rb") as fh:
        fh.read(1)  # read a single byte without raising.


def test_csv_trailing_newline_and_no_extra_blank_line():
    """File must end with exactly one newline and not two."""
    with open(CSV_PATH, "rb") as fh:
        content = fh.read()
    assert content.endswith(b"\n"), (
        f"{CSV_PATH} must end with a single newline character."
    )
    assert not content.endswith(b"\n\n"), (
        f"{CSV_PATH} ends with more than one trailing newline."
    )


def test_csv_structure_and_contents():
    """Validate header row, line count, ordering, and firmware distribution."""
    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()  # strips \n

    # 1. Exact line count: 1 header + 5 data rows
    expected_line_count = 6
    assert len(lines) == expected_line_count, (
        f"{CSV_PATH} should contain {expected_line_count} lines "
        f"(1 header + 5 data rows) but has {len(lines)}."
    )

    # 2. Header row must match exactly
    expected_header = "device_id,mac_addr,location,firmware"
    assert lines[0] == expected_header, (
        f"Header mismatch in {CSV_PATH!s}.\n"
        f"Expected: {expected_header!r}\n"
        f"Found:    {lines[0]!r}"
    )

    # 3. Validate each data row
    device_pattern = re.compile(
        r"^dev-(\d{3}),"                       # device_id
        r"([0-9A-F]{2}(?::[0-9A-F]{2}){5}),"   # mac_addr
        r"([A-Za-z_]+),"                       # location
        r"(1\.2\.(1|2|3))$"                    # firmware 1.2.1 / 1.2.2 / 1.2.3
    )

    devices_seen = []
    firmware_counts = {"1.2.1": 0, "1.2.2": 0, "1.2.3": 0}

    for line_num, row in enumerate(lines[1:], start=2):  # human-friendly line numbers
        match = device_pattern.match(row)
        assert match, (
            f"Line {line_num} in {CSV_PATH} is malformed:\n{row!r}"
        )
        dev_id, mac_addr, location, firmware_full, _ = match.groups()
        devices_seen.append(f"dev-{dev_id}")
        firmware_counts[firmware_full] += 1

    # 4. Ensure we have exactly the expected device IDs in order
    expected_devices = [f"dev-{i:03d}" for i in range(1, 6)]
    assert devices_seen == expected_devices, (
        "Device rows are missing, duplicated, or out of order.\n"
        f"Expected order: {expected_devices}\n"
        f"Found order:    {devices_seen}"
    )

    # 5. Check firmware distribution
    expected_firmware_counts = {"1.2.1": 1, "1.2.2": 1, "1.2.3": 3}
    assert firmware_counts == expected_firmware_counts, (
        "Firmware version counts do not match the expected initial state.\n"
        f"Expected: {expected_firmware_counts}\n"
        f"Found:    {firmware_counts}"
    )