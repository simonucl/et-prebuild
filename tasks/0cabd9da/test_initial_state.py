# test_initial_state.py
#
# This test-suite validates the **pre-task** operating-system / filesystem state
# for the “network engineer quick backup” exercise.
#
# It asserts ONLY the conditions that must already be true *before* the student
# performs any action.  Output artefacts (e.g. the timestamped backup directory,
# archives, logs, checksum files, etc.) are **NOT** referenced here in any way,
# per the grading rules.

import os
from pathlib import Path

import pytest

# Fixed absolute paths used throughout the initial state
DEVICE_CONFIG_DIR = Path("/home/user/device_configs")
ROUTER1_CFG = DEVICE_CONFIG_DIR / "router1.cfg"
ROUTER2_CFG = DEVICE_CONFIG_DIR / "router2.cfg"
NET_BACKUPS_DIR = Path("/home/user/net_backups")

# --------------------------------------------------------------------------- #
# Helper functions                                                             #
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """Read the entire file as UTF-8 text."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------- #
# Tests for initial filesystem state                                           #
# --------------------------------------------------------------------------- #
def test_device_config_directory_exists():
    assert DEVICE_CONFIG_DIR.is_dir(), (
        f"Required directory not found: {DEVICE_CONFIG_DIR}"
    )


@pytest.mark.parametrize(
    "path,expected_content",
    [
        (
            ROUTER1_CFG,
            (
                "hostname Router1\n"
                "interface eth0\n"
                " ip address 10.0.0.1/24\n"
                "!\n"
            ),
        ),
        (
            ROUTER2_CFG,
            (
                "hostname Router2\n"
                "interface eth0\n"
                " ip address 10.0.1.1/24\n"
                "!\n"
            ),
        ),
    ],
)
def test_router_configs_exist_with_correct_content(path: Path, expected_content: str):
    assert path.is_file(), f"Expected config file is missing: {path}"
    actual_content = read_text(path)
    assert (
        actual_content == expected_content
    ), (
        f"Contents of {path} do not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "---- Actual ----\n"
        f"{actual_content!r}"
    )


def test_net_backups_top_level_directory_exists():
    assert NET_BACKUPS_DIR.is_dir(), (
        f"Top-level backup directory should pre-exist: {NET_BACKUPS_DIR}"
    )