# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student performs any actions.  It checks that the
# pre-existing “pseudo-/etc/ssl” tree and its three files are in
# place and readable/writable by the current user.
#
# IMPORTANT:  The tests deliberately *do not* look for any of the
# artefacts that the student is supposed to create later
# (backup archive, restore directory, log file, …).

import os
import stat
import pytest

HOME = "/home/user"

# ---------------------------------------------------------------------------
# Paths that must already exist when the exercise begins
# ---------------------------------------------------------------------------
DIRS = [
    f"{HOME}/etc/ssl/private",
    f"{HOME}/etc/ssl/certs",
]

FILES_WITH_CONTENT = {
    f"{HOME}/etc/ssl/private/server.key":
        "-----BEGIN KEY-----\nfoo\n-----END KEY-----\n",
    f"{HOME}/etc/ssl/certs/server.crt":
        "-----BEGIN CERTIFICATE-----\nbar\n-----END CERTIFICATE-----\n",
    f"{HOME}/etc/ssl/certs/ca.pem":
        "-----BEGIN CERTIFICATE-----\nbaz\n-----END CERTIFICATE-----\n",
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _is_read_write(path: str) -> bool:
    """Return True if the current user has read *and* write access."""
    return os.access(path, os.R_OK) and os.access(path, os.W_OK)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("directory", DIRS)
def test_required_directories_exist_and_are_writeable(directory):
    assert os.path.exists(directory), f"Required directory missing: {directory}"
    assert os.path.isdir(directory), f"Path exists but is not a directory: {directory}"
    assert _is_read_write(directory), (
        f"Current user needs read & write access to directory: {directory}"
    )


@pytest.mark.parametrize("file_path,expected_content", FILES_WITH_CONTENT.items())
def test_required_files_exist_with_correct_content_and_permissions(file_path, expected_content):
    assert os.path.exists(file_path), f"Required file missing: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a regular file: {file_path}"
    assert _is_read_write(file_path), (
        f"Current user needs read & write access to file: {file_path}"
    )

    # Verify file content exactly matches the canonical starting data.
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == expected_content, (
        f"File content for {file_path} does not match the expected starter material."
    )