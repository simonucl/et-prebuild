# test_initial_state.py
#
# This pytest suite verifies that the repository is in its expected *initial*
# state before the student performs any actions.  It deliberately avoids
# asserting on any artefacts that the student is supposed to create or change
# (e.g. backup_verification.log, new version number, updated CHANGELOG, etc.).
#
# The tests will fail with an explicit, easy-to-understand message if anything
# from the expected initial layout is missing or wrong.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROJECT_ROOT = HOME / "projects" / "backup-tool"
BACKUPS_DIR = PROJECT_ROOT / "backups"
VERSION_FILE = PROJECT_ROOT / "version.txt"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.fail(f"Expected file '{path}' to exist, but it is missing.")
    except IsADirectoryError:
        pytest.fail(f"Expected '{path}' to be a file, but it is a directory.")


def assert_file_exists(path: Path):
    if not path.exists():
        pytest.fail(f"Expected file '{path}' to exist, but it is missing.")
    if not path.is_file():
        pytest.fail(f"Expected '{path}' to be a regular file.")


def assert_dir_exists(path: Path):
    if not path.exists():
        pytest.fail(f"Expected directory '{path}' to exist, but it is missing.")
    if not path.is_dir():
        pytest.fail(f"Expected '{path}' to be a directory.")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_version_txt_initial_content():
    """
    version.txt must exist and contain exactly one line: '1.2.3'
    """
    assert_file_exists(VERSION_FILE)
    contents = read_text(VERSION_FILE).splitlines(keepends=False)
    assert len(contents) == 1, (
        f"{VERSION_FILE} should contain exactly one line, found {len(contents)}."
    )
    assert contents[0] == "1.2.3", (
        f"{VERSION_FILE} should contain '1.2.3' but found: '{contents[0]}'."
    )


def test_changelog_initial_top_entry():
    """
    CHANGELOG.md must exist and its very first line must be
    '## [1.2.3] - 2023-08-15'
    """
    assert_file_exists(CHANGELOG_FILE)
    first_line = read_text(CHANGELOG_FILE).splitlines(keepends=False)[0]
    expected = "## [1.2.3] - 2023-08-15"
    assert first_line == expected, (
        f"First line of {CHANGELOG_FILE} expected to be:\n"
        f'    "{expected}"\n'
        f"but got:\n"
        f'    "{first_line}"'
    )


def test_backups_directory_structure_and_contents():
    """
    The backups directory must contain exactly the three expected files
    with the precise contents described in the task.
    """
    assert_dir_exists(BACKUPS_DIR)

    expected_files = {
        "backup_2023-01-01.txt": "BACKUP DATA 2023-01-01\n",
        "backup_2023-02-01.txt": "BACKUP DATA 2023-02-01\n",
        "backup_2023-03-01.txt": "BACKUP DATA 2023-03-03\n",  # deliberate typo '03'
    }

    # Verify file list matches exactly
    actual_filenames = sorted(p.name for p in BACKUPS_DIR.iterdir() if p.is_file())
    expected_filenames = sorted(expected_files.keys())
    assert actual_filenames == expected_filenames, (
        f"The backups directory should contain exactly these files:\n"
        f"    {expected_filenames}\n"
        f"but the actual files are:\n"
        f"    {actual_filenames}"
    )

    # Verify each file's content
    for filename, expected_content in expected_files.items():
        path = BACKUPS_DIR / filename
        assert_file_exists(path)
        actual_content = read_text(path)
        assert actual_content == expected_content, (
            f"File '{path}' content mismatch.\n"
            f"Expected:\n    {repr(expected_content)}\n"
            f"Got:\n    {repr(actual_content)}"
        )