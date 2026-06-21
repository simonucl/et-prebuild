# test_initial_state.py
#
# This test-suite validates the **initial** OS / filesystem state
# before the student’s solution is executed.  If any of these tests
# fail, the grading environment itself is malformed.
#
# PLEASE DO NOT MODIFY THE FILESYSTEM UNTIL **AFTER** THESE TESTS PASS.
# ---------------------------------------------------------------------

import os
import re
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
IOT_DIR = HOME / "iot_configs"
FIRMWARE_DIR = HOME / "new_firmware"
BACKUP_DIR = HOME / "old_backups"
DEPLOYMENT_LOG = HOME / "deployment_report.log"

DEVICE_IDS = [f"device_{i:02d}" for i in range(1, 6)]
FIRMWARE_AVAILABLE = {"device_01", "device_02", "device_04", "device_05"}
FIRMWARE_MISSING = {"device_03"}


def _read_lines(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.readlines()


# ---------------------------------------------------------------------
# Basic directory sanity
# ---------------------------------------------------------------------
def test_required_directories_exist():
    for d in (IOT_DIR, FIRMWARE_DIR, BACKUP_DIR):
        assert d.is_dir(), f"Required directory {d} is missing."


# ---------------------------------------------------------------------
# settings.conf files
# ---------------------------------------------------------------------
@pytest.mark.parametrize("device_id", DEVICE_IDS)
def test_settings_conf_exists(device_id):
    cfg_path = IOT_DIR / device_id / "settings.conf"
    assert cfg_path.is_file(), f"Missing settings.conf for {device_id}: {cfg_path}"


@pytest.mark.parametrize("device_id", DEVICE_IDS)
def test_settings_conf_has_correct_initial_content(device_id):
    cfg_path = IOT_DIR / device_id / "settings.conf"
    lines = _read_lines(cfg_path)

    assert len(lines) == 3, (
        f"{cfg_path} must contain exactly 3 lines. Found {len(lines)} lines."
    )

    expected_header = "# IoT Edge Device Config\n"
    expected_device_line = f"DEVICE_ID={device_id}\n"
    expected_deploy_line = "DEPLOY=NO\n"

    # Strip only trailing '\n' when comparing, allow any other whitespace issues
    assert (
        lines[0] == expected_header
    ), f"Line 1 of {cfg_path} should be '{expected_header.rstrip()}', got '{lines[0].rstrip()}'"
    assert (
        lines[1] == expected_device_line
    ), f"Line 2 of {cfg_path} should be '{expected_device_line.rstrip()}', got '{lines[1].rstrip()}'"
    assert (
        lines[2] == expected_deploy_line
    ), f"Line 3 of {cfg_path} should be '{expected_deploy_line.rstrip()}', got '{lines[2].rstrip()}'"


# ---------------------------------------------------------------------
# Firmware files
# ---------------------------------------------------------------------
MD5_RE = re.compile(r"^[0-9a-f]{32}$")


@pytest.mark.parametrize("device_id", FIRMWARE_AVAILABLE)
def test_firmware_and_md5_present(device_id):
    bin_path = FIRMWARE_DIR / f"{device_id}.bin"
    md5_path = FIRMWARE_DIR / f"{device_id}.md5"

    assert bin_path.is_file(), f"Expected firmware binary missing: {bin_path}"
    assert md5_path.is_file(), f"Expected firmware md5 file missing: {md5_path}"

    # Validate that the md5 file contains exactly one valid hash token
    content = _read_lines(md5_path)
    assert (
        len(content) == 1
    ), f"{md5_path} should contain exactly one line, got {len(content)} lines."

    # First field up to whitespace should be the hash
    md5_hash = content[0].strip().split()[0]
    assert MD5_RE.match(
        md5_hash
    ), f"First token in {md5_path} should be 32-char hex hash, got '{md5_hash}'."


@pytest.mark.parametrize("device_id", FIRMWARE_MISSING)
def test_firmware_absent_for_missing_devices(device_id):
    bin_path = FIRMWARE_DIR / f"{device_id}.bin"
    md5_path = FIRMWARE_DIR / f"{device_id}.md5"

    assert not bin_path.exists(), f"Firmware binary for {device_id} should NOT exist: {bin_path}"
    assert not md5_path.exists(), f"Firmware md5 for {device_id} should NOT exist: {md5_path}"


# ---------------------------------------------------------------------
# Backup directory contents
# ---------------------------------------------------------------------
def test_backup_dir_contains_expected_files():
    expected_files = {"stale1.bak", "stale2.bak", "notes.txt"}
    actual_files = {p.name for p in BACKUP_DIR.iterdir() if p.is_file()}

    missing = expected_files - actual_files
    extras = actual_files - expected_files

    assert not missing, f"Missing files in {BACKUP_DIR}: {sorted(missing)}"
    assert not extras, (
        f"Unexpected extra files in {BACKUP_DIR}: {sorted(extras)}. "
        "The initial state should contain exactly stale1.bak, stale2.bak and notes.txt."
    )


def test_bak_files_are_regular_and_writable():
    for bak in ("stale1.bak", "stale2.bak"):
        path = BACKUP_DIR / bak
        st = path.stat()
        assert stat.S_ISREG(
            st.st_mode
        ), f"{path} is not a regular file (mode: {oct(st.st_mode)})"
        assert os.access(path, os.W_OK), f"{path} is not writable by the current user."


# ---------------------------------------------------------------------
# deployment_report.log should NOT exist yet
# ---------------------------------------------------------------------
def test_deployment_report_not_present_yet():
    assert not DEPLOYMENT_LOG.exists(), (
        f"{DEPLOYMENT_LOG} should NOT exist before the student runs their solution."
    )