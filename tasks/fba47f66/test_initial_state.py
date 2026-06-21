# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must
# exist **before** the student runs any commands.  If any of these tests
# fail the grading harness itself is mis-configured rather than the
# student’s solution being wrong.

import os
import stat
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
WORKSPACE = HOME / "workspace"
BUILDS = WORKSPACE / "builds"
ARTIFACTS = BUILDS / "artifacts"
ARCHIVE = BUILDS / "archive"
TRANSFER_LOG = BUILDS / "transfer.log"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def assert_mode(path: Path, expected: int):
    """Assert that a path has the given permission bits (e.g. 0o755)."""
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode == expected, f"{path} permissions {oct(mode)} != expected {oct(expected)}"

def assert_mtime_older_than(path: Path, seconds: int):
    """Assert that file modification time is at least `seconds` seconds ago."""
    now = time.time()
    delta = now - path.stat().st_mtime
    assert delta > seconds, (
        f"{path} should be older than {seconds/86400:.1f} days "
        f"but is only {delta/86400:.2f} days old"
    )

def assert_mtime_newer_than(path: Path, seconds: int):
    """Assert that file modification time is not older than `seconds` seconds."""
    now = time.time()
    delta = now - path.stat().st_mtime
    assert delta < seconds, (
        f"{path} should be newer than {seconds/3600:.1f} hours "
        f"but is {delta/3600:.2f} hours old"
    )

# --------------------------------------------------------------------------- #
# Directory structure                                                         #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "directory",
    [WORKSPACE, BUILDS, ARTIFACTS, ARCHIVE],
)
def test_required_directories_exist(directory: Path):
    assert directory.is_dir(), f"Required directory missing: {directory}"
    assert_mode(directory, 0o755)


def test_archive_initially_empty():
    contents = list(ARCHIVE.iterdir())
    assert not contents, f"Archive directory must start empty, found: {[p.name for p in contents]}"

# --------------------------------------------------------------------------- #
# Files inside artifacts/                                                     #
# --------------------------------------------------------------------------- #
OLD_JARS = {
    "app-core-1.0.0.jar": b"dummy jar 1.0.0\n",
    "app-core-1.1.0.jar": b"dummy jar 1.1.0\n",
    "lib-util-2.0.0.jar": b"dummy jar 2.0.0\n",
}

FRESH_JAR = ("fresh-feature-9999.jar", b"dummy jar latest\n")
README_TXT = (
    "README.txt",
    (
        "Build Drop Area\n"
        "---------------\n"
        "Anything that is not a *.jar file\n"
        "will stay here.\n"
    ).encode(),
)

EXPECTED_ARTIFACT_FILES = set(OLD_JARS) | {FRESH_JAR[0], README_TXT[0]}


def test_artifacts_directory_contains_expected_files_only():
    present_files = {p.name for p in ARTIFACTS.iterdir() if p.is_file()}
    missing = EXPECTED_ARTIFACT_FILES - present_files
    extra = present_files - EXPECTED_ARTIFACT_FILES
    assert not missing, f"Missing expected files in artifacts/: {sorted(missing)}"
    assert not extra, f"Unexpected extra files in artifacts/: {sorted(extra)}"


@pytest.mark.parametrize("filename, content", OLD_JARS.items())
def test_old_jars_exist_and_are_older_than_7_days(filename, content):
    path = ARTIFACTS / filename
    assert path.is_file(), f"Old JAR missing: {path}"
    assert_mode(path, 0o644)
    # Content check
    data = path.read_bytes()
    assert data == content, f"Content mismatch in {path}"
    # mtime check (must be older than 7*24h = 604800 seconds)
    assert_mtime_older_than(path, 7 * 24 * 60 * 60)


def test_fresh_jar_exists_and_is_recent():
    fname, expected_content = FRESH_JAR
    path = ARTIFACTS / fname
    assert path.is_file(), f"Fresh JAR missing: {path}"
    assert_mode(path, 0o644)
    assert path.read_bytes() == expected_content, f"Content mismatch in {path}"
    # Must be newer than 2 days (172800 seconds)
    assert_mtime_newer_than(path, 2 * 24 * 60 * 60)


def test_readme_file_exists_and_is_recent():
    fname, expected_content = README_TXT
    path = ARTIFACTS / fname
    assert path.is_file(), f"README.txt missing: {path}"
    assert_mode(path, 0o644)
    assert path.read_bytes() == expected_content, f"Content mismatch in {path}"
    # Should also be recent (newer than 2 days)
    assert_mtime_newer_than(path, 2 * 24 * 60 * 60)

# --------------------------------------------------------------------------- #
# Files that must NOT exist initially                                         #
# --------------------------------------------------------------------------- #
def test_transfer_log_not_present_initially():
    assert not TRANSFER_LOG.exists(), f"{TRANSFER_LOG} should not exist before the student runs any commands"