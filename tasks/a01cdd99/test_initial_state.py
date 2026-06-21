# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student starts working on the deployment task.
#
# These tests purposefully assert that:
#   • The two staged, empty *.tar.gz files are present under
#     /home/user/preloaded_packages/ and have the expected SHA-256.
#   • No delivery artefacts ( /home/user/iot_deploy/ … ) are present yet.
#
# If any of these tests fail, the environment is not in the expected
# “clean” state and the student should not begin the task.

import hashlib
import os
from pathlib import Path

import pytest

# Constants ---------------------------------------------------------------

HOME = Path("/home/user").resolve()
PRELOADED_DIR = HOME / "preloaded_packages"
IOT_DEPLOY_DIR = HOME / "iot_deploy"

EMPTY_SHA256 = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

EXPECTED_FILES = {
    PRELOADED_DIR / "sensor_utils-1.2.3.tar.gz": EMPTY_SHA256,
    PRELOADED_DIR / "edge_comm-0.9.8.tar.gz": EMPTY_SHA256,
}


# Helpers -----------------------------------------------------------------


def sha256_of(path: Path) -> str:
    """Return the hex-encoded SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# Tests -------------------------------------------------------------------


def test_preloaded_directory_exists_and_is_directory():
    assert PRELOADED_DIR.exists(), (
        f"Expected directory '{PRELOADED_DIR}' to exist, "
        "but it is missing."
    )
    assert PRELOADED_DIR.is_dir(), (
        f"'{PRELOADED_DIR}' exists but is not a directory."
    )


def test_preloaded_directory_contains_only_expected_files():
    actual_files = {p for p in PRELOADED_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_FILES.keys())

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    assert not missing, (
        "The following expected staged package(s) are missing:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not extra, (
        "Found unexpected file(s) in the staged packages directory:\n"
        + "\n".join(str(p) for p in sorted(extra))
    )


@pytest.mark.parametrize("path,expected_digest", EXPECTED_FILES.items())
def test_each_staged_package_is_empty_and_has_known_sha256(path, expected_digest):
    assert path.exists(), f"Expected file '{path}' to exist."
    size = path.stat().st_size
    assert size == 0, (
        f"Expected '{path}' to be 0-byte (empty) for reproducibility, "
        f"but it is {size} bytes."
    )

    digest = sha256_of(path)
    assert (
        digest == expected_digest
    ), f"Checksum mismatch for '{path}'. Expected {expected_digest}, got {digest}."


def test_iot_deploy_directory_does_not_yet_exist():
    assert not IOT_DEPLOY_DIR.exists(), (
        f"Delivery directory '{IOT_DEPLOY_DIR}' already exists. "
        "Tests require a clean state before the student creates it."
    )