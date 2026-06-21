# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student performs any task.  If any of these tests
# fail, the exercise environment itself is wrong and the student should not
# be penalised.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
REPO = HOME / "repo"
RELEASES = REPO / "releases"
STABLE = REPO / "stable"
OLD_VERSION = "4.7.0"
NEW_VERSION = "4.8.1"

OLD_BIN_NAME = f"binary_{OLD_VERSION}.bin"
NEW_BIN_NAME = f"binary_{NEW_VERSION}.bin"

OLD_BIN_PATH = RELEASES / OLD_BIN_NAME
NEW_BIN_PATH = RELEASES / NEW_BIN_NAME

STABLE_LINK = STABLE / "binary.bin"
UPDATE_LOG = REPO / "update.log"


def _assert_regular_file(path: Path):
    assert path.exists(), f"Expected regular file {path} to exist, but it does not."
    st = path.stat()
    assert stat.S_ISREG(st.st_mode), f"Expected {path} to be a regular file, but it is not."


def test_releases_directory_and_binaries_exist_and_are_regular_files():
    # releases directory exists
    assert RELEASES.is_dir(), f"Directory {RELEASES} is missing."

    # binary_4.7.0.bin exists and is a regular file
    _assert_regular_file(OLD_BIN_PATH)

    # binary_4.8.1.bin exists and is a regular file
    _assert_regular_file(NEW_BIN_PATH)


def test_stable_directory_exists():
    assert STABLE.is_dir(), f"Directory {STABLE} is missing."


def test_stable_binary_symlink_points_to_old_version():
    # The symlink itself must exist
    assert STABLE_LINK.exists(), (
        f"Expected the symlink {STABLE_LINK} to exist, but it does not."
    )
    assert STABLE_LINK.is_symlink(), (
        f"{STABLE_LINK} exists but is not a symbolic link."
    )

    # The stored link text must be '../releases/binary_4.7.0.bin'
    link_text = os.readlink(STABLE_LINK)
    expected_link_text = f"../releases/{OLD_BIN_NAME}"
    assert link_text == expected_link_text, (
        f"{STABLE_LINK} should currently point to {expected_link_text!r}, "
        f"but instead points to {link_text!r}."
    )

    # The canonical (absolute) resolution must end up at the old binary
    resolved_path = STABLE_LINK.resolve(strict=True)
    assert resolved_path == OLD_BIN_PATH, (
        f"Expected {STABLE_LINK} to resolve to {OLD_BIN_PATH}, "
        f"but it resolves to {resolved_path}."
    )


def test_update_log_does_not_exist_yet():
    # At the very start of the exercise, update.log should *not* exist.
    assert not UPDATE_LOG.exists(), (
        f"{UPDATE_LOG} already exists, but the initial state should not "
        f"contain this file."
    )