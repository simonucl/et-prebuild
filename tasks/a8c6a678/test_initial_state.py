# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before** the
# student starts working on the task “myapp version bump”.
#
# IMPORTANT:  These tests purposefully FAIL if any of the “expected-final”
# artefacts already exist or if the initial files were modified.  The goal is
# to guarantee that the environment starts from a clean, known baseline.

import os
from pathlib import Path

import pytest

# Base paths
MYAPP_DIR = Path("/home/user/infra-tools/myapp")
VERSION_FILE = MYAPP_DIR / "VERSION"
CHANGELOG_FILE = MYAPP_DIR / "CHANGELOG.md"
LOG_FILE = MYAPP_DIR / "version_bump.log"


def _read_lines(path):
    """
    Return file content as a list of lines **without** trailing newlines.
    Raises a clear pytest.fail message when the file cannot be read.
    """
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        pytest.fail(f"Expected file '{path}' to be present but it is missing.")


def test_myapp_directory_exists():
    assert MYAPP_DIR.is_dir(), (
        f"Directory '{MYAPP_DIR}' must exist before the task begins."
    )


def test_version_file_initial_state():
    assert VERSION_FILE.is_file(), (
        f"File '{VERSION_FILE}' is missing; it must exist with the initial version."
    )

    content = VERSION_FILE.read_text(encoding="utf-8")
    # Allow exactly "2.3.4" plus a single trailing newline.
    assert content in ("2.3.4\n", "2.3.4"), (
        "VERSION file must contain exactly the single line '2.3.4' "
        "before the version bump."
    )


def test_changelog_has_expected_top_entry():
    assert CHANGELOG_FILE.is_file(), (
        f"File '{CHANGELOG_FILE}' is missing; it must exist for the task."
    )

    lines = _read_lines(CHANGELOG_FILE)

    expected_first_block = [
        "## [2.3.4] - 2023-09-15",
        "### Added",
        " - Initial deployment of system-wide SELinux policies.",
        "",
    ]

    assert lines[:4] == expected_first_block, (
        "CHANGELOG.md does not start with the expected entry for version 2.3.4.\n"
        "First four lines found were:\n"
        + "\n".join(repr(l) for l in lines[:4])
    )


def test_version_bump_log_not_yet_present():
    assert not LOG_FILE.exists(), (
        f"File '{LOG_FILE}' should NOT exist before the student performs the task."
    )