# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state before the
# student performs the version-bump task.  If any of these tests fail it means
# the environment was not provisioned as expected and the subsequent task
# cannot be graded reliably.

import json
import os
import re
from pathlib import Path

PROJECT_DIR = Path("/home/user/project")
PKG_JSON = PROJECT_DIR / "package.json"
CHANGELOG = PROJECT_DIR / "CHANGELOG.md"
BUMP_LOG = PROJECT_DIR / "version_bump.log"


def test_project_directory_exists():
    """The project directory must exist and be a directory."""
    assert PROJECT_DIR.exists(), f"Expected directory {PROJECT_DIR} is missing."
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory."


def test_package_json_pre_bump():
    """package.json must exist and have version 1.2.3 before the bump."""
    assert PKG_JSON.exists(), f"Expected file {PKG_JSON} is missing."
    assert PKG_JSON.is_file(), f"{PKG_JSON} exists but is not a regular file."

    # Read & parse JSON
    with PKG_JSON.open("r", encoding="utf-8") as fp:
        try:
            data = json.load(fp)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{PKG_JSON} is not valid JSON: {exc}")

    assert "version" in data, '"version" key missing from package.json.'
    assert data["version"] == "1.2.3", (
        f'Expected "version" to be "1.2.3" in {PKG_JSON}, '
        f'found "{data["version"]}".'
    )


def test_changelog_pre_bump():
    """
    CHANGELOG.md must exist, contain required existing headers, and *not* yet
    contain an entry for 1.2.4.
    """
    assert CHANGELOG.exists(), f"Expected file {CHANGELOG} is missing."
    assert CHANGELOG.is_file(), f"{CHANGELOG} exists but is not a regular file."

    text = CHANGELOG.read_text(encoding="utf-8").splitlines()

    unreleased_pattern = re.compile(r"^##\s+\[Unreleased]$")
    v123_pattern = re.compile(r"^##\s+\[1\.2\.3]\s+-\s+2023-08-01$")
    v124_pattern = re.compile(r"^##\s+\[1\.2\.4]")

    has_unreleased = any(unreleased_pattern.match(line) for line in text)
    has_123 = any(v123_pattern.match(line) for line in text)
    has_124 = any(v124_pattern.match(line) for line in text)

    assert has_unreleased, (
        "CHANGELOG.md is missing the required '## [Unreleased]' header."
    )
    assert has_123, (
        "CHANGELOG.md is missing the existing '## [1.2.3] - 2023-08-01' section."
    )
    assert not has_124, (
        "CHANGELOG.md already contains a '## [1.2.4]' section; "
        "it should not exist before the student performs the bump."
    )


def test_version_bump_log_absent():
    """version_bump.log must NOT exist before the student creates it."""
    assert not BUMP_LOG.exists(), (
        f"{BUMP_LOG} already exists; it should be created only after the "
        "version bump task is executed."
    )