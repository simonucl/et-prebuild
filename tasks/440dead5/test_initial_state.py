# test_initial_state.py
#
# This pytest suite verifies that the workspace is in a *pristine* state
# before the student begins the exercise.  NONE of the paths that the
# assignment is going to create should exist yet.

import os
from pathlib import Path

HOME = Path("/home/user")
BUILD_ARTIFACTS_DIR = HOME / "build_artifacts"
ARCHIVE_PATH = HOME / "build_2023-10-31.tar.gz"
RELEASE_CANDIDATE_DIR = HOME / "release_candidate"
MANIFEST_PATH = RELEASE_CANDIDATE_DIR / "manifest.sha256"
VERIFICATION_LOG = RELEASE_CANDIDATE_DIR / "verification.log"


def _assert_absent(path: Path):
    """Helper that asserts a path does not exist with a clear message."""
    assert not path.exists(), (
        f"Pre-flight check failed: {path} already exists, "
        "but it should not be present before the student starts the task."
    )


def test_home_directory_exists():
    """Sanity check: the home directory itself must exist."""
    assert HOME.is_dir(), "Expected directory /home/user to exist on the test system."


def test_build_artifacts_directory_absent():
    """The build_artifacts directory should NOT exist yet."""
    _assert_absent(BUILD_ARTIFACTS_DIR)


def test_archive_absent():
    """The compressed archive should NOT exist yet."""
    _assert_absent(ARCHIVE_PATH)


def test_release_candidate_directory_absent():
    """The release_candidate directory should NOT exist yet."""
    _assert_absent(RELEASE_CANDIDATE_DIR)


def test_manifest_absent():
    """manifest.sha256 should NOT exist yet (release_candidate dir absent)."""
    _assert_absent(MANIFEST_PATH)


def test_verification_log_absent():
    """verification.log should NOT exist yet (release_candidate dir absent)."""
    _assert_absent(VERIFICATION_LOG)