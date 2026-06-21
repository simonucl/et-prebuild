# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem/OS state
# is exactly what the assignment says should already exist **before**
# the student starts working.  It intentionally does **not** refer to
# any files or directories that the student is expected to create.
#
# Only the following pre-existing resources are checked:
#
#   /home/user/manifests/                  (directory)
#   /home/user/manifests/web-deploy.yaml   (file, contains ":v1" image)
#   /home/user/manifests/cache-deploy.yaml (file, contains ":v1" image)
#
# Any mismatch will raise a clear pytest failure explaining
# what is missing or incorrect.

import re
from pathlib import Path

import pytest

MANIFEST_DIR = Path("/home/user/manifests").resolve()
EXPECTED_MANIFESTS = {
    "web-deploy.yaml": "myapp/web:v1",
    "cache-deploy.yaml": "myapp/cache:v1",
}

IMAGE_LINE_RE = re.compile(r"^\s*image:\s*(?P<image>[\w\/\-\.:]+)\s*$")


def test_manifest_directory_exists_and_is_dir():
    assert MANIFEST_DIR.exists(), (
        f"Required directory {MANIFEST_DIR} is missing. "
        "The initial state must include the manifests directory."
    )
    assert MANIFEST_DIR.is_dir(), (
        f"{MANIFEST_DIR} exists but is not a directory. "
        "It must be a directory containing the provided YAML manifests."
    )


@pytest.mark.parametrize("filename,expected_image", EXPECTED_MANIFESTS.items())
def test_each_manifest_file_exists_with_correct_initial_image(filename, expected_image):
    """
    For every expected manifest, ensure:
      1. The file exists at the exact path.
      2. At least one line reads `image: <expected_image>` (with tag :v1).
      3. The document declares `kind: Deployment` (case-sensitive match).
    """
    manifest_path = MANIFEST_DIR / filename
    assert manifest_path.exists(), (
        f"Expected manifest file {manifest_path} is missing in the initial state."
    )
    assert manifest_path.is_file(), (
        f"{manifest_path} exists but is not a regular file."
    )

    text = manifest_path.read_text(encoding="utf-8").splitlines()

    # Check for kind: Deployment
    has_deployment_kind = any(
        line.strip() == "kind: Deployment" for line in text
    )
    assert has_deployment_kind, (
        f"{manifest_path} is expected to be a Deployment manifest "
        "but no line `kind: Deployment` was found."
    )

    # Check for the correct initial image tag (:v1)
    images_found = [
        m.group("image") for line in text if (m := IMAGE_LINE_RE.match(line))
    ]
    assert expected_image in images_found, (
        f"{manifest_path} should contain the image '{expected_image}' "
        "but it was not found.  Ensure the initial manifests reference ':v1' tags."
    )