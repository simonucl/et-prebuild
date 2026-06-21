# test_initial_state.py
#
# This test-suite validates the **initial** filesystem state that must be
# present *before* the student performs any actions on the build links.
#
# The assertions below are based on the task description and will fail with
# clear, actionable messages if anything is missing or out of place.
#
# Allowed imports: stdlib + pytest only.
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
BUILD_ROOT = HOME / "builds"
ANDROID_ROOT = BUILD_ROOT / "android"
CHANNELS_DIR = BUILD_ROOT / "channels"
LOG_FILE = BUILD_ROOT / "link_update.log"


# --------------------------------------------------------------------------- #
# Helper data fixtures
# --------------------------------------------------------------------------- #
EXPECTED_BUILD_DIRS = {
    "1.2.0": {
        "channel": "stable",
        "version": "1.2.0",
    },
    "1.3.0-beta": {
        "channel": "beta",
        "version": "1.3.0-beta",
    },
    "1.4.0": {
        "channel": "stable",
        "version": "1.4.0",
    },
    "2.0.0-alpha": {
        "channel": "canary",
        "version": "2.0.0-alpha",
    },
    "2.0.0": {
        "channel": "stable",
        "version": "2.0.0",
    },
}

EXPECTED_CHANNEL_SYMLINKS = {
    "stable": ANDROID_ROOT / "1.4.0",
    "beta": ANDROID_ROOT / "1.3.0-beta",
    # canary is NOT expected to be present yet
}

# --------------------------------------------------------------------------- #
# Tests for Android build directories and VERSION files
# --------------------------------------------------------------------------- #
def test_android_root_exists():
    assert ANDROID_ROOT.is_dir(), (
        f"Expected directory '{ANDROID_ROOT}' is missing."
    )


@pytest.mark.parametrize("version", EXPECTED_BUILD_DIRS.keys())
def test_each_build_directory_exists(version):
    build_dir = ANDROID_ROOT / version
    assert build_dir.is_dir(), f"Build directory '{build_dir}' is missing."


@pytest.mark.parametrize(
    "version,expected",
    [(v, data) for v, data in EXPECTED_BUILD_DIRS.items()],
)
def test_version_file_contents(version, expected):
    build_dir = ANDROID_ROOT / version
    version_file = build_dir / "VERSION"
    assert version_file.is_file(), f"VERSION file missing: {version_file}"

    # Read first two non-empty lines
    with version_file.open() as fh:
        lines = [line.rstrip("\n") for line in fh.readlines()[:2]]

    assert len(lines) >= 2, (
        f"VERSION file '{version_file}' must have at least two lines."
    )

    channel_line, version_line = lines[0], lines[1]

    assert channel_line == f"channel={expected['channel']}", (
        f"{version_file}: expected first line to be "
        f"'channel={expected['channel']}', got '{channel_line}'."
    )
    assert version_line == f"version={expected['version']}", (
        f"{version_file}: expected second line to be "
        f"'version={expected['version']}', got '{version_line}'."
    )


# --------------------------------------------------------------------------- #
# Tests for channels directory and symlinks
# --------------------------------------------------------------------------- #
def test_channels_directory_exists():
    assert CHANNELS_DIR.is_dir(), (
        f"Channels directory '{CHANNELS_DIR}' is missing."
    )


@pytest.mark.parametrize(
    "link_name,target_path",
    [(name, path) for name, path in EXPECTED_CHANNEL_SYMLINKS.items()],
)
def test_expected_symlinks_exist_and_point_correctly(link_name, target_path):
    symlink_path = CHANNELS_DIR / link_name
    assert symlink_path.exists(), (
        f"Expected symlink '{symlink_path}' is missing."
    )
    assert symlink_path.is_symlink(), (
        f"Path '{symlink_path}' exists but is not a symlink."
    )
    resolved = symlink_path.resolve()
    assert resolved == target_path, (
        f"Symlink '{symlink_path}' points to '{resolved}', "
        f"but should point to '{target_path}'."
    )


def test_canary_symlink_absent_initially():
    canary_link = CHANNELS_DIR / "canary"
    assert not canary_link.exists(), (
        "Symlink 'canary' should NOT exist in the initial state."
    )


def test_no_extra_symlinks_in_channels_dir():
    expected_names = set(EXPECTED_CHANNEL_SYMLINKS.keys())
    actual_names = {p.name for p in CHANNELS_DIR.iterdir() if p.is_symlink()}
    unexpected = actual_names - expected_names
    assert not unexpected, (
        f"Unexpected symlinks present in '{CHANNELS_DIR}': {sorted(unexpected)}"
    )


# --------------------------------------------------------------------------- #
# Tests for absence of log file before actions
# --------------------------------------------------------------------------- #
def test_log_file_not_present_initially():
    assert not LOG_FILE.exists(), (
        f"Log file '{LOG_FILE}' should not exist before any update actions."
    )