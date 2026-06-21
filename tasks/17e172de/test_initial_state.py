# test_initial_state.py
#
# Pytest suite ensuring that the repository is in the *original* state
# before the student performs any actions.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
REPO_ROOT = HOME / "k8s-operator"
DEPLOY_DIR = REPO_ROOT / "deploy"

VERSION_FILE = REPO_ROOT / "VERSION"
DEPLOYMENT_YAML = DEPLOY_DIR / "operator-deployment.yaml"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
LOG_FILE = HOME / "version_bump.log"


@pytest.fixture(scope="module")
def version_contents():
    """Return the text inside VERSION (stripped of trailing newlines)."""
    assert VERSION_FILE.exists(), f"Missing {VERSION_FILE}"
    text = VERSION_FILE.read_text()
    return text.rstrip("\n")


def test_repository_structure_exists():
    assert REPO_ROOT.is_dir(), f"Directory {REPO_ROOT} is missing"
    assert DEPLOY_DIR.is_dir(), f"Directory {DEPLOY_DIR} is missing"
    assert VERSION_FILE.is_file(), f"File {VERSION_FILE} is missing"
    assert DEPLOYMENT_YAML.is_file(), f"File {DEPLOYMENT_YAML} is missing"
    assert CHANGELOG.is_file(), f"File {CHANGELOG} is missing"


def test_version_file_initial(version_contents):
    expected = "1.2.3"
    assert version_contents == expected, (
        f"{VERSION_FILE} should contain exactly '{expected}' "
        f"(found: '{version_contents}')"
    )


def test_deployment_yaml_initial():
    data = DEPLOYMENT_YAML.read_text().splitlines()
    image_lines = [line for line in data if "image:" in line]
    assert image_lines, (
        f"{DEPLOYMENT_YAML} does not contain any 'image:' line to check"
    )

    expected_line = "               image: myrepo/myoperator:1.2.3"
    assert expected_line in data, (
        f"Expected image tag not found in {DEPLOYMENT_YAML}.\n"
        f"Expected line:\n{expected_line}\n"
        f"Make sure the image tag is still 1.2.3 before the task begins."
    )

    forbidden = "myrepo/myoperator:1.3.0"
    assert all(forbidden not in line for line in data), (
        f"Found '{forbidden}' in {DEPLOYMENT_YAML} but it should not be "
        f"present before the version bump."
    )


def test_changelog_initial():
    content = CHANGELOG.read_text().splitlines()
    assert content, f"{CHANGELOG} is empty"

    # 1. Header line must start with the old version.
    header = content[0]
    expected_header = "## [1.2.3] - 2023-05-11"
    assert header == expected_header, (
        f"First line of {CHANGELOG} must be '{expected_header}'\n"
        f"Found: '{header}'"
    )

    # 2. Second line must be blank.
    assert content[1] == "", (
        f"Second line of {CHANGELOG} should be blank "
        f"but found: '{content[1]}'"
    )

    # 3. Third line must be the bullet point for the old version.
    third_line_expected = " - Fix CRD validation issue"
    assert content[2] == third_line_expected, (
        f"Third line of {CHANGELOG} should be "
        f"'{third_line_expected}', but found: '{content[2]}'"
    )

    # Ensure the new version header is NOT yet present.
    assert not any(line.startswith("## [1.3.0]") for line in content), (
        f"{CHANGELOG} already contains a 1.3.0 entry, but this should only "
        f"appear after completing the task."
    )


def test_log_file_absent():
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before any commands are run."
    )