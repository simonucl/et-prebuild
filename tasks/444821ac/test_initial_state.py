# test_initial_state.py
#
# This test-suite verifies the operating-system / filesystem state
# *before* the student executes any command.  It checks that the
# container registry is pre-populated exactly as described and that
# none of the output artefacts the student is supposed to create are
# present yet.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")

# ----------------------------------------------------------------------
# Paths that must already exist
REPO_DIR = HOME / "container_repo"
EXPECTED_IMAGES = {
    "backend_2.4.sif",
    "frontend_1.8.sif",
    "nginx_1.21.sif",
    "worker_2.4.sif",
}

# Paths that must **not** exist yet (the student will create them)
DEPLOY_LOG_DIR = HOME / "deployment_logs"
INVENTORY_FILE = DEPLOY_LOG_DIR / "container_inventory.txt"


# ----------------------------------------------------------------------
def test_container_repo_directory_exists_and_is_directory():
    assert REPO_DIR.exists(), (
        f"Required directory {REPO_DIR} is missing. The pre-populated "
        "container registry must be available before the exercise starts."
    )
    assert REPO_DIR.is_dir(), (
        f"{REPO_DIR} exists but is not a directory. It must be a directory "
        "that holds the container image files."
    )


def test_expected_images_present_and_no_extras():
    repo_contents = {p.name for p in REPO_DIR.iterdir() if p.is_file()}

    missing = EXPECTED_IMAGES - repo_contents
    extras = repo_contents - EXPECTED_IMAGES

    assert not missing, (
        "The pre-populated registry is missing the following expected image "
        f"files in {REPO_DIR}: {sorted(missing)}"
    )
    assert not extras, (
        "The container registry contains unexpected extra files. Only the "
        f"following files should be present at start-time: "
        f"{sorted(EXPECTED_IMAGES)}\n"
        f"Extra files found: {sorted(extras)}"
    )


def test_each_image_is_regular_file_and_readable():
    for filename in EXPECTED_IMAGES:
        file_path = REPO_DIR / filename
        assert file_path.is_file(), f"{file_path} is not a regular file."
        mode = file_path.stat().st_mode
        assert stat.S_IMODE(mode) & 0o444, (
            f"{file_path} is not readable (mode {oct(stat.S_IMODE(mode))}). "
            "Files must be readable so the student command can list them."
        )


def test_deployment_logs_directory_absent_initially():
    assert not DEPLOY_LOG_DIR.exists(), (
        f"{DEPLOY_LOG_DIR} already exists before the exercise starts, but "
        "the requirement states the student must create it if it does not "
        "yet exist."
    )


def test_inventory_file_absent_initially():
    assert not INVENTORY_FILE.exists(), (
        f"{INVENTORY_FILE} already exists before the exercise starts, but "
        "the student must create this file with the required content."
    )