# test_initial_state.py
#
# This pytest file verifies the *initial* filesystem state that must be
# present **before** the student creates the backup artifacts requested in
# the task description.  It checks that:
#
# 1. The directory /home/user/k8s-manifests exists and is a directory.
# 2. The three expected YAML manifest files exist as regular files inside
#    that directory.
# 3. No backup directory (/home/user/k8s-backup) is present yet.
#
# Any failure points out exactly what is missing or unexpectedly present so
# that the student can start from a clean, known-good baseline.

import os
from pathlib import Path
import pytest

MANIFEST_DIR = Path("/home/user/k8s-manifests")
EXPECTED_MANIFESTS = {
    MANIFEST_DIR / "deployment.yaml",
    MANIFEST_DIR / "service.yaml",
    MANIFEST_DIR / "configmap.yaml",
}

BACKUP_DIR = Path("/home/user/k8s-backup")


def test_manifest_directory_exists_and_is_directory():
    """The manifests directory must exist and be a directory."""
    assert MANIFEST_DIR.exists(), (
        f"Expected directory {MANIFEST_DIR} is missing. "
        "Create it and place the Kubernetes manifests inside it."
    )
    assert MANIFEST_DIR.is_dir(), (
        f"{MANIFEST_DIR} exists but is not a directory. "
        "It must be a directory containing the manifest YAML files."
    )


@pytest.mark.parametrize("manifest_path", sorted(EXPECTED_MANIFESTS))
def test_each_expected_manifest_exists_and_is_file(manifest_path: Path):
    """Each individual manifest file must exist and be a regular file."""
    assert manifest_path.exists(), (
        f"Expected manifest file {manifest_path} is missing."
    )
    assert manifest_path.is_file(), (
        f"{manifest_path} exists but is not a regular file."
    )
    assert manifest_path.stat().st_size > 0, (
        f"Manifest file {manifest_path} is empty; it should contain YAML data."
    )


def test_no_extra_yaml_files_present():
    """
    There should be exactly the three expected YAML files and no others.
    This guarantees deterministic backup behaviour later.
    """
    yaml_files = {p for p in MANIFEST_DIR.iterdir() if p.suffix.lower() == ".yaml"}
    missing = EXPECTED_MANIFESTS - yaml_files
    extra = yaml_files - EXPECTED_MANIFESTS

    assert not missing, (
        f"The following expected YAML files are missing from {MANIFEST_DIR}: "
        f"{', '.join(map(str, sorted(missing)))}"
    )
    assert not extra, (
        f"The following unexpected YAML files are present in {MANIFEST_DIR}: "
        f"{', '.join(map(str, sorted(extra)))}. "
        "The directory must contain only the three required manifests."
    )


def test_backup_directory_does_not_exist_yet():
    """
    The backup directory should NOT exist before the backup operation.
    Its presence would indicate that the backup has already been created
    or that the starting state is polluted.
    """
    assert not BACKUP_DIR.exists(), (
        f"Backup directory {BACKUP_DIR} already exists, "
        "but it should not be present before running the backup procedure."
    )