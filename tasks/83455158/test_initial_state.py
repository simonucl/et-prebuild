# test_initial_state.py
#
# This pytest file verifies the *initial* state of the project on disk,
# i.e. before the student performs any actions.  Only the pre-existing
# artefacts are checked; no assertions are made about files that will be
# created or modified later (per the instructions).

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
PROJECT_ROOT = HOME / "ds_cleaning"
VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


def read_bytes(path: Path) -> bytes:
    """Utility: read a file in binary mode, fail clearly if it is missing."""
    if not path.exists():
        pytest.fail(f"Expected file does not exist: {path}")
    if not path.is_file():
        pytest.fail(f"Path exists but is not a regular file: {path}")
    return path.read_bytes()


def test_project_directory_exists_and_is_dir():
    assert PROJECT_ROOT.exists(), f"Missing project directory: {PROJECT_ROOT}"
    assert PROJECT_ROOT.is_dir(), f"Expected {PROJECT_ROOT} to be a directory."


def test_version_file_content_is_exactly_1_0_0_newline():
    expected = b"1.0.0\n"
    actual = read_bytes(VERSION_FILE)
    assert (
        actual == expected
    ), f"{VERSION_FILE} content mismatch.\nExpected: {expected!r}\nActual:   {actual!r}"


def test_changelog_file_content_matches_expected_initial_state():
    expected_text = (
        "# Changelog\n"
        "\n"
        "All notable changes to this project will be documented in this file.\n"
        "\n"
        "## [1.0.0] - 2022-12-01\n"
        "### Added\n"
        "- Initial release\n"
    )
    expected = expected_text.encode()

    actual = read_bytes(CHANGELOG_FILE)
    assert (
        actual == expected
    ), (
        f"{CHANGELOG_FILE} content does not match the expected initial state.\n\n"
        "---- Expected ----\n"
        f"{expected_text!r}\n"
        "---- Actual ----\n"
        f"{actual.decode(errors='replace')!r}\n"
        "------------------"
    )