# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state **before**
# the student’s synchronisation script is run.
#
# It asserts that:
#   1. The source directory /home/user/app_configs/ exists and contains
#      exactly the three expected configuration files.
#   2. Each of those three files has the exact, byte-for-byte content
#      specified in the task description.
#   3. The mock “remote” host directory /home/user/remote_host/ exists
#      and is completely empty (no files, no sub-directories).
#   4. The reports directory /home/user/sync_reports/ does *not* yet
#      exist.
#
# Any failure message is written so that the student immediately knows
# which prerequisite is missing or incorrect.

import os
from pathlib import Path

import pytest


SOURCE_DIR = Path("/home/user/app_configs")
REMOTE_HOST_DIR = Path("/home/user/remote_host")
SYNC_REPORTS_DIR = Path("/home/user/sync_reports")

EXPECTED_FILES = {
    "database.yml": (
        "adapter: postgresql\n"
        "encoding: utf8\n"
        "pool: 5\n"
    ),
    "redis.conf": (
        "maxmemory 256mb\n"
        "appendonly yes\n"
    ),
    "app.env": (
        "RAILS_ENV=production\n"
        "SECRET_KEY_BASE=abc123xyz\n"
    ),
}


@pytest.fixture(scope="module")
def source_files():
    """Return a mapping of filename → Path object for the files
    expected in /home/user/app_configs/."""
    return {name: SOURCE_DIR / name for name in EXPECTED_FILES}


def test_source_directory_exists():
    assert SOURCE_DIR.is_dir(), (
        f"Required directory {SOURCE_DIR} is missing. "
        "Create it and populate it with the three configuration files."
    )


def test_source_contains_exactly_three_files(source_files):
    # Collect *all* entries in the source directory (files, dirs, etc.)
    entries = [p for p in SOURCE_DIR.iterdir()]
    entry_names = {p.name for p in entries}

    assert len(entries) == 3 and all(p.is_file() for p in entries), (
        f"{SOURCE_DIR} should contain exactly three regular files "
        f"{list(EXPECTED_FILES)} but contains {sorted(entry_names)}."
    )

    # Verify that the expected filenames are present
    missing = set(EXPECTED_FILES) - entry_names
    unexpected = entry_names - set(EXPECTED_FILES)
    assert not missing and not unexpected, (
        f"{SOURCE_DIR} is expected to contain only {sorted(EXPECTED_FILES)}.\n"
        f"Missing: {sorted(missing)}\n"
        f"Unexpected: {sorted(unexpected)}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_individual_file_contents(source_files, filename, expected_content):
    file_path = source_files[filename]
    assert file_path.is_file(), f"Expected file {file_path} is missing."

    actual_bytes = file_path.read_bytes()
    expected_bytes = expected_content.encode()

    assert (
        actual_bytes == expected_bytes
    ), f"Content of {file_path} does not match the required specification."


def test_remote_host_directory_exists_and_is_empty():
    assert REMOTE_HOST_DIR.is_dir(), (
        f"Mock remote host directory {REMOTE_HOST_DIR} must exist (it should "
        "have been pre-created by the exercise)."
    )

    contents = list(REMOTE_HOST_DIR.iterdir())
    assert not contents, (
        f"{REMOTE_HOST_DIR} is expected to be completely empty before the "
        "sync begins, but it currently contains: "
        f"{[p.name for p in contents]}"
    )


def test_sync_reports_directory_does_not_exist_yet():
    assert not SYNC_REPORTS_DIR.exists(), (
        f"Reports directory {SYNC_REPORTS_DIR} should *not* exist before the "
        "student runs their script; it will be created during execution."
    )