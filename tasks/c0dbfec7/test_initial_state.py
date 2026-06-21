# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the learner updates the “latest” symlink.
#
# Expected pre-exercise structure:
# /home/user/builds/                       (directory)
# ├── build_v1.0.0/                        (directory)
# ├── build_v1.1.0/                        (directory)
# ├── build_v1.2.0/                        (directory)
# └── latest  -> build_v1.1.0              (symlink pointing to build_v1.1.0)
#
# Only the standard library and pytest are used.

import os
from pathlib import Path

ROOT = Path("/home/user/builds")
DIRS = {
    "build_v1.0.0",
    "build_v1.1.0",
    "build_v1.2.0",
}
LATEST_LINK = ROOT / "latest"
EXPECTED_LATEST_TARGET = ROOT / "build_v1.1.0"  # the link _should_ point here *before* the task


def test_builds_root_exists_and_is_directory():
    assert ROOT.exists(), f"Required directory {ROOT} does not exist."
    assert ROOT.is_dir(), f"{ROOT} exists but is not a directory."


def test_expected_build_directories_exist_and_are_dirs():
    for dirname in DIRS:
        dpath = ROOT / dirname
        assert dpath.exists(), f"Expected build directory {dpath} is missing."
        assert dpath.is_dir(), f"{dpath} exists but is not a directory."


def test_latest_symlink_points_to_build_v1_1_0():
    assert LATEST_LINK.exists(), (
        f"Symlink {LATEST_LINK} is missing. "
        "It should exist and point to the previous latest build."
    )
    assert LATEST_LINK.is_symlink(), (
        f"{LATEST_LINK} exists but is not a symbolic link."
    )

    # os.readlink returns the link’s *stored* value (could be relative).
    link_target_raw = os.readlink(LATEST_LINK)
    link_target = (LATEST_LINK.parent / link_target_raw).resolve()

    assert link_target == EXPECTED_LATEST_TARGET, (
        f"{LATEST_LINK} should resolve to {EXPECTED_LATEST_TARGET}, "
        f"but instead points to {link_target}."
    )