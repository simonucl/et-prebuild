# test_initial_state.py
#
# This pytest test-suite validates the *initial* state of the filesystem
# before the student creates the diff patch and log file requested in the
# task description.

import os
from pathlib import Path

OLD_DIR = Path("/home/user/pipeline_configs/old")
NEW_DIR = Path("/home/user/pipeline_configs/new")
OLD_CFG = OLD_DIR / "config.yml"
NEW_CFG = NEW_DIR / "config.yml"

PATCH_DIR = Path("/home/user/ci_cd_patch")
PATCH_FILE = PATCH_DIR / "ci_config.patch"
LOG_FILE = PATCH_DIR / "generation.log"


def test_old_config_directory_exists():
    assert OLD_DIR.is_dir(), (
        f"Expected directory '{OLD_DIR}' is missing. "
        "The old pipeline configuration directory must exist."
    )


def test_old_config_file_exists():
    assert OLD_CFG.is_file(), (
        f"Expected file '{OLD_CFG}' is missing. "
        "The old pipeline config file must be present."
    )


def test_new_config_directory_exists():
    assert NEW_DIR.is_dir(), (
        f"Expected directory '{NEW_DIR}' is missing. "
        "The new pipeline configuration directory must exist."
    )


def test_new_config_file_exists():
    assert NEW_CFG.is_file(), (
        f"Expected file '{NEW_CFG}' is missing. "
        "The new pipeline config file must be present."
    )


def test_config_files_have_expected_key_differences():
    """
    Sanity-check that the two config files actually differ in the ways
    the subsequent diff operation is supposed to capture.  This ensures
    the student has meaningful source material to work with.
    """
    old_text = OLD_CFG.read_text().splitlines()
    new_text = NEW_CFG.read_text().splitlines()

    # Minimal expected differences: version bump and new notifications block.
    assert 'version: "1.0"' in old_text, (
        f"Old config '{OLD_CFG}' does not contain the expected version line."
    )
    assert 'version: "1.1"' in new_text, (
        f"New config '{NEW_CFG}' does not contain the expected updated version line."
    )
    assert any(line.startswith("notifications:") for line in new_text), (
        f"New config '{NEW_CFG}' is expected to introduce a 'notifications:' block."
    )
    assert old_text != new_text, (
        "The old and new configuration files appear to be identical. "
        "They must differ so that a meaningful patch can be generated."
    )


def test_patch_directory_does_not_exist_yet():
    """
    Before the student runs their solution, the patch directory and its
    artefacts must *not* exist.
    """
    assert not PATCH_DIR.exists(), (
        f"Directory '{PATCH_DIR}' should not exist before the patch is generated."
    )


def test_patch_and_log_files_do_not_exist_yet():
    assert not PATCH_FILE.exists(), (
        f"Patch file '{PATCH_FILE}' should not exist before the student creates it."
    )
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' should not exist before the student creates it."
    )