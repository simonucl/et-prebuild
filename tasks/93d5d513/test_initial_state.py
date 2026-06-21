# test_initial_state.py
#
# This test-suite verifies that the filesystem state **before** the student
# performs any action matches the description given in the assignment.
#
# ❗ If any of these tests fail the student starts from a wrong baseline.
#
# Requirements checked:
#   1. Repository folder exists and is writable.
#   2. VERSION file exists and contains exactly "1.3.4\n".
#   3. package.json exists, is valid JSON and its top-level "version" is "1.3.4".
#   4. CHANGELOG.md exists, has the expected first non-comment heading and ends
#      with a trailing newline.
#   5. `version_bump.log` must NOT exist yet.
#
# Only Python’s stdlib and pytest are used.

import json
import os
from pathlib import Path

import pytest

REPO_DIR = Path("/home/user/infra-observability").resolve()
VERSION_FILE = REPO_DIR / "VERSION"
PACKAGE_JSON_FILE = REPO_DIR / "package.json"
CHANGELOG_FILE = REPO_DIR / "CHANGELOG.md"
LOG_FILE = Path("/home/user/version_bump.log")


@pytest.fixture(scope="session")
def repo_path():
    # A fixture that ensures the repository directory exists.
    assert REPO_DIR.exists(), (
        f"Expected repository directory {REPO_DIR} to exist, "
        "but it is missing."
    )
    assert REPO_DIR.is_dir(), (
        f"Expected {REPO_DIR} to be a directory, but it is not."
    )
    return REPO_DIR


def test_repo_is_writable(repo_path):
    """The entire repository directory must be writable by the current user."""
    assert os.access(repo_path, os.W_OK), (
        f"Repository directory {repo_path} is not writable by the current user."
    )


def test_version_file_contents(repo_path):
    """VERSION file must contain exactly '1.3.4\\n'."""
    assert VERSION_FILE.exists(), f"Missing VERSION file at {VERSION_FILE}."
    assert VERSION_FILE.is_file(), f"{VERSION_FILE} exists but is not a file."

    raw = VERSION_FILE.read_text(encoding="utf-8")
    expected = "1.3.4\n"
    assert raw == expected, (
        f"VERSION file content mismatch.\n"
        f"Expected: {repr(expected)}\n"
        f"Actual  : {repr(raw)}"
    )

    # Ensure write permission
    assert os.access(VERSION_FILE, os.W_OK), (
        f"VERSION file {VERSION_FILE} is not writable."
    )


def test_package_json_version(repo_path):
    """package.json must be valid JSON with top-level 'version' == '1.3.4'."""
    assert PACKAGE_JSON_FILE.exists(), (
        f"Missing package.json at {PACKAGE_JSON_FILE}."
    )
    assert PACKAGE_JSON_FILE.is_file(), (
        f"{PACKAGE_JSON_FILE} exists but is not a file."
    )

    try:
        data = json.loads(PACKAGE_JSON_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        pytest.fail(f"package.json is not valid JSON: {exc}")

    assert isinstance(data, dict), "Top-level JSON structure must be an object."
    assert "version" in data, "Key 'version' not found in package.json."
    assert data["version"] == "1.3.4", (
        f"package.json 'version' value expected to be '1.3.4' "
        f"but found '{data['version']}'."
    )

    # Ensure write permission
    assert os.access(PACKAGE_JSON_FILE, os.W_OK), (
        f"package.json {PACKAGE_JSON_FILE} is not writable."
    )


def _first_non_comment_non_empty_line(lines):
    """Return first line that is neither a HTML comment nor blank."""
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("<!--"):
            return stripped
    return None


def test_changelog_initial_block(repo_path):
    """
    CHANGELOG.md must start with the expected heading after an optional
    comment. The first non-comment, non-blank line must be:

        ## [1.3.4] – 2024-05-22
    """
    assert CHANGELOG_FILE.exists(), f"Missing CHANGELOG.md at {CHANGELOG_FILE}."
    assert CHANGELOG_FILE.is_file(), (
        f"{CHANGELOG_FILE} exists but is not a file."
    )

    lines = CHANGELOG_FILE.read_text(encoding="utf-8").splitlines(keepends=False)

    first_meaningful = _first_non_comment_non_empty_line(lines)
    expected_heading = "## [1.3.4] – 2024-05-22"
    assert first_meaningful == expected_heading, (
        "First non-comment line in CHANGELOG.md does not match the expected "
        f"heading.\nExpected: {expected_heading}\nFound   : {first_meaningful}"
    )

    # Must end with a newline (file read without keepends=> original had newline)
    raw = CHANGELOG_FILE.read_bytes()
    assert raw.endswith(b"\n"), "CHANGELOG.md must end with a trailing newline."

    # Ensure write permission
    assert os.access(CHANGELOG_FILE, os.W_OK), (
        f"CHANGELOG.md {CHANGELOG_FILE} is not writable."
    )


def test_version_bump_log_absent():
    """The version_bump.log file must NOT exist before any action is taken."""
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should not exist before the version bump process starts."
    )