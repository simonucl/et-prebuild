# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any action for the “release-audit” task.
#
# This file checks that:
#   • The expected release directories and files already exist.
#   • Each expected file has the exact byte-size stated in the task
#     description.
#   • The /home/user/release_audit directory (and anything inside it)
#     does NOT yet exist.
#
# No assertions are made about any artefacts that the student must
# create (e.g. disk_usage_report.csv).  Those are intentionally absent
# from this initial-state test suite.
#
# Only Python’s standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
RELEASES_DIR = os.path.join(HOME, "releases")
AUDIT_DIR = os.path.join(HOME, "release_audit")

# Expected directory structure and per-file byte-sizes.
# Keys are release names; values are dicts mapping relative file path
# (inside the release) → expected size in bytes.
EXPECTED_STRUCTURE = {
    "app_v1.0": {
        "README.txt": 512,
        "bin/app.bin": 1536,
    },
    "app_v1.1": {
        "README.txt": 1024,
        "bin/app.bin": 2048,
        "docs/CHANGELOG.md": 3072,
    },
    "app_v2.0": {
        "README.txt": 2048,
        "bin/app.bin": 3072,
        "scripts/migrate.sh": 2048,
    },
}


def _full_path(release: str, relative_path: str) -> str:
    """Return the absolute path for a file within a release."""
    return os.path.join(RELEASES_DIR, release, *relative_path.split("/"))


def test_releases_directory_exists_and_is_dir():
    assert os.path.exists(RELEASES_DIR), (
        f"Expected '{RELEASES_DIR}' to exist, but it does not."
    )
    assert os.path.isdir(RELEASES_DIR), (
        f"Expected '{RELEASES_DIR}' to be a directory."
    )


@pytest.mark.parametrize("release", EXPECTED_STRUCTURE.keys())
def test_each_release_directory_exists(release):
    path = os.path.join(RELEASES_DIR, release)
    assert os.path.exists(path), (
        f"Missing release directory: '{path}'."
    )
    assert os.path.isdir(path), (
        f"Expected '{path}' to be a directory."
    )


@pytest.mark.parametrize(
    "release,relative_path,expected_size",
    [
        (rel, rel_path, size)
        for rel, files in EXPECTED_STRUCTURE.items()
        for rel_path, size in files.items()
    ],
)
def test_expected_files_exist_with_correct_size(release, relative_path, expected_size):
    path = _full_path(release, relative_path)

    assert os.path.exists(path), f"Missing expected file: '{path}'."
    assert os.path.isfile(path), f"Expected '{path}' to be a regular file."

    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"File '{path}' has size {actual_size} bytes; expected {expected_size} bytes."
    )

    # Optional: check basic read permission for the current user
    st_mode = os.stat(path).st_mode
    assert bool(st_mode & stat.S_IRUSR), (
        f"File '{path}' is not readable by the current user."
    )


def test_release_audit_directory_does_not_exist_yet():
    assert not os.path.exists(AUDIT_DIR), (
        f"Directory '{AUDIT_DIR}' should NOT exist before the student runs their code."
    )