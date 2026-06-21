# test_initial_state.py
#
# This test-suite validates that the sandbox **before** the learner’s work
# matches the expected initial state described in the project brief.
#
# It checks:
#   1. Presence of the /home/user/k8s-manifests/ directory.
#   2. Exactly three manifest files exist inside that directory.
#   3. The contents of each file are as expected, especially the image tag
#      inside deployment-app.yml (must be `mycorp/app:0.9` and NOT 1.0 yet).
#   4. No confirmation log (fix-report.log) is present yet.
#
# Only the Python stdlib and pytest are used, per requirements.

import os
from pathlib import Path
import re
import pytest

MANIFEST_DIR = Path("/home/user/k8s-manifests")
DEPLOYMENT_FILE = MANIFEST_DIR / "deployment-app.yml"
SERVICE_FILE = MANIFEST_DIR / "service-app.yml"
CONFIGMAP_FILE = MANIFEST_DIR / "configmap-app.yml"
LOG_FILE = MANIFEST_DIR / "fix-report.log"


def test_manifest_directory_exists_and_is_dir():
    assert MANIFEST_DIR.exists(), (
        "Expected directory '/home/user/k8s-manifests/' does not exist."
    )
    assert MANIFEST_DIR.is_dir(), (
        f"'{MANIFEST_DIR}' exists but is not a directory."
    )


def test_manifest_directory_contains_exactly_three_expected_files():
    expected_files = {
        DEPLOYMENT_FILE.name,
        SERVICE_FILE.name,
        CONFIGMAP_FILE.name,
    }
    actual_files = {p.name for p in MANIFEST_DIR.iterdir() if p.is_file()}

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    assert not missing, (
        f"Missing expected file(s) in '{MANIFEST_DIR}': {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected extra file(s) found in '{MANIFEST_DIR}': {', '.join(sorted(extra))}"
    )
    # Exactly three files (no hidden surprises)
    assert len(actual_files) == 3, (
        f"Expected exactly 3 files in '{MANIFEST_DIR}', found {len(actual_files)}."
    )


def _read_file(path: Path) -> str:
    assert path.exists(), f"Required file '{path}' does not exist."
    return path.read_text(encoding="utf-8")


def test_deployment_contains_old_image_tag_only():
    """deployment-app.yml must reference mycorp/app:0.9 and NOT 1.0 (yet)."""
    content = _read_file(DEPLOYMENT_FILE)

    # There should be exactly one 'image:' line and it must be the old tag.
    image_lines = [ln.strip() for ln in content.splitlines() if ln.strip().startswith("image:")]

    assert image_lines, (
        f"No 'image:' key found in {DEPLOYMENT_FILE}. One is required."
    )
    assert len(image_lines) == 1, (
        f"Expected exactly 1 'image:' line in {DEPLOYMENT_FILE}, found {len(image_lines)}."
    )

    image_line = image_lines[0]
    assert image_line == "image: mycorp/app:0.9", (
        f"First 'image:' line in {DEPLOYMENT_FILE} must be "
        "'image: mycorp/app:0.9' (was: '{image_line}')."
    )

    # Ensure the correct tag (1.0) is *not* already present.
    assert "mycorp/app:1.0" not in content, (
        f"{DEPLOYMENT_FILE} already contains the updated image tag 'mycorp/app:1.0'; "
        "it should still reference 0.9 before the task begins."
    )


def test_service_contains_no_image_tags():
    """service-app.yml should not have any container image references."""
    content = _read_file(SERVICE_FILE)
    assert "image:" not in content, (
        f"{SERVICE_FILE} unexpectedly contains an 'image:' key."
    )


def test_configmap_contains_no_image_tags():
    """configmap-app.yml should not have any container image references."""
    content = _read_file(CONFIGMAP_FILE)
    assert "image:" not in content, (
        f"{CONFIGMAP_FILE} unexpectedly contains an 'image:' key."
    )


def test_fix_report_log_does_not_exist_yet():
    """The confirmation log should not exist before the learner makes changes."""
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' already exists; it should be created only after the fix."
    )