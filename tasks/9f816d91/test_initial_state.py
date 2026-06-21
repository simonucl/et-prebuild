# test_initial_state.py
#
# This pytest suite validates that the **initial** filesystem state
# is exactly as expected *before* the student performs any actions.
# It checks for the presence and contents of the original manifest
# files and confirms that the report directory has not been created
# yet.

import re
from pathlib import Path

import pytest


MANIFESTS_DIR = Path("/home/user/manifests")
REPORT_DIR = Path("/home/user/report")

# Expected manifest files and the *exact* image lines they must contain
EXPECTED_IMAGE_LINES = {
    "deployment-frontend.yaml": "        image: myrepo/frontend:v1.0.0",
    "deployment-backend.yaml": "        image: myrepo/backend:v1.0.0",
    "statefulset-db.yaml": "        image: otherrepo/postgres:13",
}

CONFIGMAP_FILE = "configmap.yaml"


@pytest.fixture(scope="module")
def manifests_dir() -> Path:
    return MANIFESTS_DIR


def test_manifests_directory_exists(manifests_dir: Path):
    assert manifests_dir.exists(), f"Expected directory {manifests_dir} to exist."
    assert manifests_dir.is_dir(), f"{manifests_dir} exists but is not a directory."


def test_expected_manifest_files_exist(manifests_dir: Path):
    missing = [fname for fname in list(EXPECTED_IMAGE_LINES) + [CONFIGMAP_FILE]
               if not (manifests_dir / fname).is_file()]
    assert not missing, (
        "The following required manifest files are missing under "
        f"{manifests_dir}: {', '.join(missing)}"
    )


@pytest.mark.parametrize("filename,expected_line", EXPECTED_IMAGE_LINES.items())
def test_manifest_contains_expected_image_line(manifests_dir: Path, filename: str, expected_line: str):
    file_path = manifests_dir / filename
    content = file_path.read_text().splitlines()

    assert expected_line in content, (
        f"{filename} should contain the exact line:\n    {expected_line}\n"
        "but it was not found."
    )

    # Ensure the new tag is NOT present yet
    new_tag_pattern = re.compile(r"^\s{8}image:\s+myrepo/.+:v1\.1\.3$")
    assert not any(new_tag_pattern.match(line) for line in content), (
        f"{filename} already contains the updated v1.1.3 tag, "
        "but this should not be the case before the student runs their solution."
    )


def test_statefulset_other_repo_is_untouched(manifests_dir: Path):
    """Confirm the otherrepo line exists and still uses tag 13."""
    filename = "statefulset-db.yaml"
    expected_line = EXPECTED_IMAGE_LINES[filename]
    content = (manifests_dir / filename).read_text().splitlines()

    assert expected_line in content, (
        f"{filename} should contain the exact line:\n    {expected_line}\n"
        "but it was not found."
    )
    assert not any("v1.1.3" in line for line in content), (
        f"{filename} unexpectedly contains tag v1.1.3."
    )


def test_configmap_has_no_image_lines(manifests_dir: Path):
    cfg_path = manifests_dir / CONFIGMAP_FILE
    content = cfg_path.read_text()
    assert "image:" not in content, (
        f"{CONFIGMAP_FILE} should not contain any 'image:' lines in the initial state."
    )


def test_report_directory_absent():
    assert not REPORT_DIR.exists(), (
        f"Directory {REPORT_DIR} should NOT exist before the student generates the reports."
    )