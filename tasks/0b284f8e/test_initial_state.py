# test_initial_state.py
#
# This test-suite verifies the initial filesystem state that must be present
# BEFORE the student performs any action.  In particular we check the
# existence, permissions, and exact contents of the input file
#   /home/user/releases/services_2023-10.txt
#
# Do **NOT** add any assertions about the output artefact
# `/home/user/releases/service_frequency.log` here – that file should not
# exist yet.

import os
from pathlib import Path
import stat
import pytest

# Constants for quick reference
RELEASES_DIR = Path("/home/user/releases")
INPUT_FILE = RELEASES_DIR / "services_2023-10.txt"

EXPECTED_LINES = [
    "auth",
    "billing",
    "auth",
    "reports",
    "auth",
    "billing",
    "search",
    "search",
    "analytics",
]


def test_releases_directory_exists():
    """The parent releases directory must exist and be a directory."""
    assert RELEASES_DIR.exists(), (
        f"Expected directory {RELEASES_DIR} to exist, but it does not."
    )
    assert RELEASES_DIR.is_dir(), (
        f"Expected {RELEASES_DIR} to be a directory, "
        f"but it is a {'file' if RELEASES_DIR.is_file() else 'non-directory'}."
    )


def test_input_file_exists_and_is_regular():
    """Validate that the input file exists and is a regular file."""
    assert INPUT_FILE.exists(), (
        f"Input file {INPUT_FILE} is missing. "
        "The exercise requires this file with the list of service names."
    )
    assert INPUT_FILE.is_file(), (
        f"{INPUT_FILE} exists but is not a regular file."
    )


def test_input_file_permissions():
    """
    The file should have mode 644 (rw-r--r--).  More permissive bits
    (e.g. world-write) are acceptable but execute bits are not.
    """
    mode = INPUT_FILE.stat().st_mode & 0o777
    assert mode & stat.S_IXUSR == 0, (
        f"{INPUT_FILE} must not be executable; got mode {oct(mode)}."
    )
    assert mode & stat.S_IXGRP == 0, (
        f"{INPUT_FILE} must not be executable; got mode {oct(mode)}."
    )
    assert mode & stat.S_IXOTH == 0, (
        f"{INPUT_FILE} must not be executable; got mode {oct(mode)}."
    )
    expected_min_mode = 0o644
    assert mode >= expected_min_mode, (
        f"{INPUT_FILE} permissions too restrictive: expected at least "
        f"{oct(expected_min_mode)}, got {oct(mode)}."
    )


def test_input_file_contents_exact():
    """
    The file must contain exactly the expected 9 lines (LF endings),
    in the precise order shown in the task description.
    """
    contents = INPUT_FILE.read_text(encoding="utf-8").splitlines()
    assert contents == EXPECTED_LINES, (
        "The contents of {file} do not match the expected list.\n"
        "Expected:\n{exp}\n\nFound:\n{found}".format(
            file=INPUT_FILE, exp="\n".join(EXPECTED_LINES), found="\n".join(contents)
        )
    )


@pytest.mark.parametrize("duplicate_service", ["auth", "billing", "search"])
def test_duplicates_are_present(duplicate_service):
    """
    Sanity-check that services known to have duplicates (auth, billing, search)
    appear more than once in the list.  This guards against accidental edits
    that might leave only unique entries.
    """
    contents = INPUT_FILE.read_text(encoding="utf-8").splitlines()
    count = contents.count(duplicate_service)
    assert count > 1, (
        f"Expected {duplicate_service!r} to appear multiple times in "
        f"{INPUT_FILE}; found it {count} time(s)."
    )