# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state for the
# “minor semantic-version bump” exercise.  It purposefully checks that
# the repository is still at version 1.2.3 and that no bump artefacts
# (such as the new CHANGELOG entry or version_bump.log) are present yet.

import json
from pathlib import Path

PROJECT_DIR = Path("/home/user/my-web-app")
PACKAGE_JSON = PROJECT_DIR / "package.json"
CHANGELOG_MD = PROJECT_DIR / "CHANGELOG.md"
VERSION_LOG = Path("/home/user/version_bump.log")


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected project directory {PROJECT_DIR} to exist. "
        "Make sure the repository is cloned in the correct location."
    )


def test_package_json_initial_version():
    assert PACKAGE_JSON.is_file(), f"Missing expected file: {PACKAGE_JSON}"
    with PACKAGE_JSON.open(encoding="utf-8") as fp:
        try:
            data = json.load(fp)
        except json.JSONDecodeError as e:
            raise AssertionError(f"{PACKAGE_JSON} is not valid JSON: {e}")

    expected = {
        "name": "my-web-app",
        "version": "1.2.3",
        "description": "Sample web app",
        "dependencies": {},
    }

    assert data == expected, (
        f"{PACKAGE_JSON} content mismatch.\n"
        f"Expected exactly:\n{json.dumps(expected, indent=2)}\n\n"
        f"Got:\n{json.dumps(data, indent=2)}"
    )


def test_changelog_initial_content():
    assert CHANGELOG_MD.is_file(), f"Missing expected file: {CHANGELOG_MD}"
    content = CHANGELOG_MD.read_text(encoding="utf-8")

    # Required substrings for the initial state.
    required_chunks = [
        "# Changelog",
        "All notable changes to this project will be documented in this file.",
        "## [1.2.3] - 2023-07-01",
        "- Initial release.",
    ]
    for chunk in required_chunks:
        assert chunk in content, f"{CHANGELOG_MD} is missing expected text: {chunk!r}"

    # Ensure the new 1.3.0 section has NOT been created yet.
    assert "## [1.3.0] - 2024-01-01" not in content, (
        f"{CHANGELOG_MD} already contains the 1.3.0 section; "
        "the bump should not be done yet."
    )


def test_version_bump_log_does_not_exist_yet():
    assert not VERSION_LOG.exists(), (
        f"{VERSION_LOG} should NOT exist in the initial state. "
        "It must be created only after performing the version bump."
    )