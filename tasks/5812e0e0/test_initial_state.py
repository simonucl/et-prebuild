# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state for the
# “release-manager” task.  It checks that the expected release directories
# and files already exist **before** the student starts creating any output
# artefacts.  Nothing is asserted about the /home/user/deployment/ folder or
# its contents, because those constitute the *output* of the exercise.
#
# If any assertion fails, the error message pin-points exactly what is
# missing or incorrect so that the student can focus on repairing the setup
# rather than guessing.

import os
from pathlib import Path

import pytest


BASE_RELEASES_DIR = Path("/home/user/releases")

# Mapping of expected versions to their critical first-line contents.
EXPECTED_RELEASES = {
    "v2.0.0": {
        "changelog_first_line": "v2.0.0 - 2023-05-10 Major release",
        "release_notes_heading": "# Release Notes for v2.0.0",
    },
    "v2.1.0": {
        "changelog_first_line": "v2.1.0 - 2023-08-12 Minor release",
        "release_notes_heading": "# Release Notes for v2.1.0",
    },
    "v3.0.0-beta": {
        "changelog_first_line": "v3.0.0-beta - 2024-01-20 Beta release",
        "release_notes_heading": "# Release Notes for v3.0.0-beta",
    },
}


def _first_non_empty_line(path: Path) -> str:
    """
    Return the first non-empty line from *path*, stripped of its trailing
    newline but preserving internal spaces.
    """
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.rstrip("\n")
            if stripped.strip():  # any non-whitespace content
                return stripped
    return ""  # empty file


def _first_markdown_h1(path: Path) -> str:
    """
    Return the first Markdown H1 heading (starts with exactly '# ') from *path*,
    including the leading '# ' for comparison convenience.  If none is found,
    return the empty string.
    """
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            candidate = line.rstrip("\n")
            # Allow preceding whitespace but require '# '
            if candidate.lstrip().startswith("# "):
                return candidate.strip()
    return ""


def test_releases_dir_exists_and_is_directory():
    assert BASE_RELEASES_DIR.exists(), (
        f"Expected directory {BASE_RELEASES_DIR} is missing."
    )
    assert BASE_RELEASES_DIR.is_dir(), (
        f"Expected {BASE_RELEASES_DIR} to be a directory, "
        f"but it exists as a different file type."
    )


@pytest.mark.parametrize("version", sorted(EXPECTED_RELEASES))
def test_release_subdirectories_exist(version):
    release_dir = BASE_RELEASES_DIR / version
    assert release_dir.exists(), (
        f"Release directory {release_dir} is missing."
    )
    assert release_dir.is_dir(), (
        f"{release_dir} exists but is not a directory."
    )


@pytest.mark.parametrize("version, expectations", EXPECTED_RELEASES.items())
def test_changelog_first_line(version, expectations):
    changelog_path = BASE_RELEASES_DIR / version / "CHANGELOG.txt"
    expected_line = expectations["changelog_first_line"]

    assert changelog_path.exists(), (
        f"{changelog_path} is missing."
    )
    assert changelog_path.is_file(), (
        f"{changelog_path} exists but is not a regular file."
    )

    actual_line = _first_non_empty_line(changelog_path)
    assert actual_line == expected_line, (
        f"First non-empty line of {changelog_path} was:\n"
        f"    {actual_line!r}\n"
        f"but expected:\n"
        f"    {expected_line!r}"
    )


@pytest.mark.parametrize("version, expectations", EXPECTED_RELEASES.items())
def test_release_notes_first_heading(version, expectations):
    notes_path = BASE_RELEASES_DIR / version / "RELEASE_NOTES.md"
    expected_heading = expectations["release_notes_heading"]

    assert notes_path.exists(), (
        f"{notes_path} is missing."
    )
    assert notes_path.is_file(), (
        f"{notes_path} exists but is not a regular file."
    )

    actual_heading = _first_markdown_h1(notes_path)
    assert actual_heading == expected_heading, (
        f"First Markdown H1 heading in {notes_path} was:\n"
        f"    {actual_heading!r}\n"
        f"but expected:\n"
        f"    {expected_heading!r}"
    )