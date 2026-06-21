# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student begins the task described in the README.  It checks
# only the files that must already be present; it intentionally avoids
# touching or asserting about any files/directories that are supposed to
# be created or modified by the student later.

import pathlib
import pytest

# Base paths
IOT_DIR = pathlib.Path("/home/user/iot")
DEPLOY_DIR = IOT_DIR / "deploy"

# ----------------------------------------------------------------------
# Helper data ­– the exact contents that must be present *before* work
# starts.  A final newline is required for each file.
# ----------------------------------------------------------------------

EXPECTED_INVENTORY = (
    "device01,edge-lab,68,45,ok\n"
    "device02,edge-lab,77,50,ok\n"
    "device03,edge-lab,72,85,ok\n"
    "device04,field,80,90,error\n"
    "device05,field,60,40,ok\n"
)

EXPECTED_CONFIG = (
    "[deployment]\n"
    "device_group=edge\n"
    "version=1.4.2\n"
)


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_directories_exist():
    """Verify that the fundamental directories laid out in the spec exist."""
    assert IOT_DIR.is_dir(), (
        f"Required directory {IOT_DIR} is missing. "
        "The initial resources should be available in this path."
    )
    assert DEPLOY_DIR.is_dir(), (
        f"Required directory {DEPLOY_DIR} is missing. "
        "It should contain config.ini before any work is done."
    )


def test_inventory_csv_presence_and_content():
    """inventory.csv must exist with the exact expected content."""
    inventory_path = IOT_DIR / "inventory.csv"
    assert inventory_path.is_file(), (
        f"Expected file {inventory_path} is missing."
    )
    data = inventory_path.read_text(encoding="utf-8")
    assert data == EXPECTED_INVENTORY, (
        f"Content mismatch in {inventory_path}.\n"
        "If this file was modified, restore it to the original state "
        "provided by the task setup."
    )
    assert data.endswith("\n"), (
        f"{inventory_path} must terminate with a single newline character."
    )


def test_config_ini_presence_and_content():
    """config.ini must exist and still contain version 1.4.2."""
    config_path = DEPLOY_DIR / "config.ini"
    assert config_path.is_file(), (
        f"Expected file {config_path} is missing."
    )
    content = config_path.read_text(encoding="utf-8")
    assert content == EXPECTED_CONFIG, (
        f"Content mismatch in {config_path}.\n"
        "Ensure the file has not been changed before starting the task."
    )
    assert content.endswith("\n"), (
        f"{config_path} must terminate with a single newline character."
    )