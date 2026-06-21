# test_initial_state.py
#
# Pytest suite that validates the workstation **before** the
# student starts working on the “Synchronise a release bundle…” task.
#
# DO NOT MODIFY THIS FILE.
#
# What is checked:
#   • The source bundle exists at /home/user/project and contains
#     exactly three files with exact byte contents.
#   • The two “remote” directories already exist and are completely
#     empty (no files, no sub-directories, not even hidden ones).
#
# Nothing about /home/user/deploy or any output artefacts is checked
# here, in accordance with the grading-framework rules.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def assert_file_bytes(path: Path, expected: bytes) -> None:
    """
    Assert that 'path' exists, is a file and its byte content equals 'expected'.
    """
    assert path.exists(), f"Expected file {path!s} is missing."
    assert path.is_file(), f"Path {path!s} exists but is not a regular file."
    actual = path.read_bytes()
    assert actual == expected, (
        f"Content mismatch in {path!s}.\n"
        f"Expected bytes:\n{expected!r}\n\nActual bytes:\n{actual!r}"
    )

def assert_empty_directory(path: Path) -> None:
    """
    Assert that 'path' exists, is a directory and contains no files,
    sub-directories or other directory entries (including hidden ones).
    """
    assert path.exists(), f"Expected directory {path!s} is missing."
    assert path.is_dir(), f"Path {path!s} exists but is not a directory."
    entries = list(path.iterdir())
    assert not entries, (
        f"Directory {path!s} is expected to be empty but contains:\n"
        + "\n".join(str(p) for p in entries)
    )

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_source_bundle_structure_and_content():
    """
    Validate that the source release bundle exists with the exact three files
    and the correct byte-for-byte contents.
    """
    project_dir = HOME / "project"
    assert project_dir.exists(), f"Source directory {project_dir!s} is missing."
    assert project_dir.is_dir(), f"{project_dir!s} exists but is not a directory."

    expected_files = {
        "index.html": b"<h1>Welcome</h1>\n",
        "app.js": b'console.log("version 1.0.0");\n',
        "config.yaml": b"version: 1.0.0\n",
    }

    # Check that only and exactly these files are present
    present_files = {p.name for p in project_dir.iterdir() if p.is_file()}
    assert present_files == set(expected_files), (
        "The source bundle must contain exactly the files "
        f"{sorted(expected_files)}.\n"
        f"Currently present: {sorted(present_files)}"
    )

    # Check contents of each file
    for filename, expected_bytes in expected_files.items():
        assert_file_bytes(project_dir / filename, expected_bytes)


@pytest.mark.parametrize(
    "remote_subpath",
    [
        "remote_servers/web01/var/www/app",
        "remote_servers/web02/var/www/app",
    ],
)
def test_remote_directories_exist_and_are_empty(remote_subpath):
    """
    Ensure the two ‘remote’ application directories exist and are empty.
    """
    remote_dir = HOME / remote_subpath
    assert_empty_directory(remote_dir)