# test_initial_state.py
#
# This test-suite validates the filesystem **before** the student performs any work.
# It asserts that the initial project structure and file contents match the
# specification given in the task description.

import json
from pathlib import Path

import pytest

# Base paths
HOME = Path("/home/user")
APP_DIR = HOME / "secure-app"
CONFIG_DIR = APP_DIR / "config"

VERSION_FILE = APP_DIR / "VERSION"
CHANGELOG_FILE = APP_DIR / "CHANGELOG.md"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"


def _read_text(path: Path) -> str:
    """Read a text file using UTF-8 and return its contents."""
    return path.read_text(encoding="utf-8")


def test_secure_app_directory_exists():
    assert APP_DIR.is_dir(), f"Expected directory {APP_DIR} to exist."


@pytest.mark.parametrize(
    "path,should_exist",
    [
        (VERSION_FILE, True),
        (CHANGELOG_FILE, True),
        (CREDENTIALS_FILE, True),
    ],
)
def test_required_files_exist(path: Path, should_exist: bool):
    assert path.exists() is should_exist, f"File {path} {'is missing' if should_exist else 'should not exist'}."
    if should_exist:
        assert path.is_file(), f"Expected {path} to be a regular file."


def test_version_file_contents():
    expected = "3.2.0\n"
    actual = _read_text(VERSION_FILE)
    assert (
        actual == expected
    ), f"{VERSION_FILE} content mismatch.\nExpected: {repr(expected)}\nFound:    {repr(actual)}"


def test_changelog_file_contents():
    expected = (
        "# Changelog\n"
        "\n"
        "All notable changes to this project will be documented in this file.\n"
        "\n"
        "## [3.2.0] - 2024-01-15\n"
        "### Added\n"
        "- Initial public release.\n"
    )
    actual = _read_text(CHANGELOG_FILE)
    assert (
        actual == expected
    ), f"{CHANGELOG_FILE} content does not match the expected initial changelog."


def test_credentials_file_contents_and_structure():
    raw = _read_text(CREDENTIALS_FILE)
    # Ensure the file ends with exactly one newline
    assert raw.endswith(
        "\n"
    ), f"{CREDENTIALS_FILE} must end with a single trailing newline."
    # The JSON parser will raise if the file is not valid JSON
    data = json.loads(raw)
    # Exact keys expected
    expected_keys = ["api_key", "db_password"]
    assert list(data.keys()) == expected_keys, (
        f"{CREDENTIALS_FILE} keys mismatch.\n"
        f"Expected order: {expected_keys}\nFound order:    {list(data.keys())}"
    )
    assert (
        data["api_key"] == "OLD_SECRET_KEY"
    ), f"Expected 'api_key' to be 'OLD_SECRET_KEY' in {CREDENTIALS_FILE}."
    assert (
        data["db_password"] == "unchanged"
    ), f"Expected 'db_password' to remain 'unchanged' in {CREDENTIALS_FILE}."


# NOTE:
# The rotation.log file is intentionally *not* checked here because it will be
# created by the student as part of the task and is therefore an output file.