# test_initial_state.py
#
# Pytest suite that validates the filesystem *before* the student’s
# shell/awk/sed script runs.  It asserts that the three expected
# IoT-device configuration files exist with the exact contents and
# that no deployment artefacts are yet present.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
CFG_DIR = HOME / "iot_configs"
DEPLOY_DIR = HOME / "deployment"

EXPECTED_CONFIGS = {
    "dev01.cfg": [
        "device_id=dev01\n",
        "ip=192.168.1.101\n",
        "status=online\n",
        "firmware_version=1.0.2\n",
    ],
    "dev02.cfg": [
        "device_id=dev02\n",
        "ip=192.168.1.102\n",
        "status=offline\n",
        "firmware_version=1.0.2\n",
    ],
    "dev03.cfg": [
        "device_id=dev03\n",
        "ip=192.168.1.103\n",
        "status=online\n",
        "firmware_version=1.0.1\n",
    ],
}


def _read_lines(path: Path):
    """Read file in text mode preserving EOL, return list of lines."""
    with path.open("r", encoding="utf-8", newline="") as fh:
        return fh.readlines()


def test_iot_configs_directory_present():
    assert CFG_DIR.is_dir(), (
        f"Required directory '{CFG_DIR}' is missing. "
        "All *.cfg files must reside here."
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_CONFIGS.keys()))
def test_each_cfg_file_exists(filename):
    cfg_path = CFG_DIR / filename
    assert cfg_path.is_file(), f"Missing configuration file: '{cfg_path}'."


@pytest.mark.parametrize("filename, expected_lines", EXPECTED_CONFIGS.items())
def test_cfg_file_exact_contents(filename, expected_lines):
    cfg_path = CFG_DIR / filename
    actual_lines = _read_lines(cfg_path)

    # 1. Correct number of lines
    assert len(actual_lines) == 4, (
        f"File '{cfg_path}' should have exactly 4 lines; "
        f"found {len(actual_lines)}."
    )

    # 2. Line-by-line content match
    assert actual_lines == expected_lines, (
        f"File '{cfg_path}' contents do not match expected template.\n"
        "Expected:\n"
        + "".join(expected_lines)
        + "\nActual:\n"
        + "".join(actual_lines)
    )

    # 3. Final newline present (redundant if lines compare, but explicit)
    with cfg_path.open("rb") as fh:
        fh.seek(-1, os.SEEK_END)
        last_byte = fh.read(1)
    assert last_byte == b"\n", f"File '{cfg_path}' must end with a newline."


def test_no_deployment_outputs_exist_yet():
    """
    Before the student performs any action, the deployment artefacts
    should *not* exist.
    """
    online_csv = DEPLOY_DIR / "online_devices.csv"
    log_file = DEPLOY_DIR / "firmware_update.log"

    assert not online_csv.exists(), (
        f"'{online_csv}' should not exist before the task is run."
    )
    assert not log_file.exists(), (
        f"'{log_file}' should not exist before the task is run."
    )