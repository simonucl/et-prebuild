# test_initial_state.py
#
# This pytest suite validates the *initial* repository state **before**
# the student begins their work.  It checks that the expected placeholder
# Debian packages exist in /home/user/repos/stable with the correct
# content, size, and SHA-256 digests.  Nothing related to any output
# artefacts (e.g. /home/user/manifests) is verified here.

import hashlib
import os
import stat
import pytest

REPO_DIR = "/home/user/repos/stable"

# Expected files with their known size and SHA-256 (empty file digest)
EXPECTED_FILES = {
    "libbar_2.5.1_amd64.deb": {
        "size": 0,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb924"
                  "27ae41e4649b934ca495991b7852b855",
    },
    "libfoo_1.0.0_amd64.deb": {
        "size": 0,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb924"
                  "27ae41e4649b934ca495991b7852b855",
    },
}


def sha256_of_file(path: str) -> str:
    """Return the lowercase hex SHA-256 digest of the given file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_repository_directory_exists():
    assert os.path.isdir(REPO_DIR), (
        f"Expected directory {REPO_DIR!r} is missing. "
        "The initial repository must already be checked out."
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_FILES))
def test_debian_placeholders_exist_and_match_digest(filename):
    file_meta = EXPECTED_FILES[filename]
    full_path = os.path.join(REPO_DIR, filename)

    # Existence & type
    assert os.path.exists(full_path), (
        f"Expected file {full_path!r} is missing."
    )
    assert os.path.isfile(full_path), (
        f"{full_path!r} exists but is not a regular file."
    )

    # Size
    actual_size = os.path.getsize(full_path)
    assert actual_size == file_meta["size"], (
        f"File {full_path!r} has size {actual_size}, "
        f"but {file_meta['size']} bytes were expected."
    )

    # SHA-256 digest
    actual_sha256 = sha256_of_file(full_path)
    assert actual_sha256 == file_meta["sha256"], (
        f"File {full_path!r} has SHA-256 digest {actual_sha256}, "
        f"but expected {file_meta['sha256']}."
    )

    # Read permissions (world-readable)
    mode = os.stat(full_path).st_mode
    assert mode & stat.S_IRUSR, f"{full_path!r} is not readable by owner."
    assert mode & stat.S_IRGRP, f"{full_path!r} is not readable by group."
    assert mode & stat.S_IROTH, f"{full_path!r} is not readable by others."