# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# (before the student performs any packaging actions).
#
# The checks intentionally avoid looking for – or even mentioning –
# the output artefacts that the student is expected to create
# (e.g. the .tar.gz archive and the .log file).  Only the pre-existing
# files/directories are verified.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

# Base paths that must already exist
RELEASE_DIR = HOME / "releases" / "v1.0"
README      = RELEASE_DIR / "README.md"
BIN_DIR     = RELEASE_DIR / "bin"
START_SH    = BIN_DIR / "start.sh"
CONFIG_DIR  = RELEASE_DIR / "config"
SETTINGS_CF = CONFIG_DIR / "settings.conf"

# Directory into which the student will later place new artefacts.
# It must exist *now* but be empty.
PKG_DIR     = HOME / "releases_packages"


def _assert_is_file(path: Path):
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"Path {path} must be a regular file."


def _assert_is_dir(path: Path):
    assert path.exists(), f"Required directory {path} is missing."
    assert path.is_dir(), f"Path {path} must be a directory."


def test_release_directory_structure():
    """Ensure /home/user/releases/v1.0 contains ONLY the expected items."""
    _assert_is_dir(RELEASE_DIR)

    expected_root_items = {"README.md", "bin", "config"}
    actual_root_items = {p.name for p in RELEASE_DIR.iterdir()}
    assert actual_root_items == expected_root_items, (
        f"{RELEASE_DIR} must contain exactly {sorted(expected_root_items)}, "
        f"but contains {sorted(actual_root_items)}"
    )

    # bin/
    _assert_is_dir(BIN_DIR)
    bin_items = {p.name for p in BIN_DIR.iterdir()}
    assert bin_items == {"start.sh"}, (
        f"{BIN_DIR} must contain only 'start.sh', but contains {sorted(bin_items)}"
    )

    # config/
    _assert_is_dir(CONFIG_DIR)
    config_items = {p.name for p in CONFIG_DIR.iterdir()}
    assert config_items == {"settings.conf"}, (
        f"{CONFIG_DIR} must contain only 'settings.conf', but contains {sorted(config_items)}"
    )

    # Individual files
    _assert_is_file(README)
    _assert_is_file(START_SH)
    _assert_is_file(SETTINGS_CF)


def test_readme_contents():
    """README.md should contain the expected single-line release note."""
    with README.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    expected = "Project v1.0 — release notes.\n"
    assert contents == expected, (
        f"{README} has unexpected contents:\n{contents!r}\nExpected:\n{expected!r}"
    )


def test_start_sh_contents():
    """start.sh script must match the provided template exactly."""
    with START_SH.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    expected = "#!/usr/bin/env bash\necho 'Starting v1.0'\n"
    assert contents == expected, (
        f"{START_SH} has unexpected contents:\n{contents!r}\nExpected:\n{expected!r}"
    )


def test_settings_conf_contents():
    """settings.conf must match the expected production settings."""
    with SETTINGS_CF.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    expected = "mode=production\nversion=1.0\n"
    assert contents == expected, (
        f"{SETTINGS_CF} has unexpected contents:\n{contents!r}\nExpected:\n{expected!r}"
    )


def test_releases_packages_dir_empty():
    """
    The directory meant for packaged artefacts must already exist
    and be empty prior to any student action.
    """
    _assert_is_dir(PKG_DIR)
    leftover = [p.name for p in PKG_DIR.iterdir()]
    assert not leftover, (
        f"{PKG_DIR} should be empty before packaging begins; "
        f"found unexpected items: {leftover}"
    )