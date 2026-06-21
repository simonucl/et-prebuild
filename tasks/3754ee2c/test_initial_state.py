# test_initial_state.py
#
# This pytest file validates the *initial* state of the workspace
# before the student updates anything.  It checks that:
#
# 1. The Android build-tools directory hierarchy exists.
# 2. The two version directories v33/ and v34/ are present.
# 3. The symbolic link “current” exists and still points to v33/
#
# It deliberately does *not* look for the log file
# /home/user/build-tools/link_update.log nor require the “current”
# symlink to point to v34/, because those are artefacts that the
# student is expected to create/modify.

import os
import stat
from pathlib import Path

ANDROID_ROOT = Path("/home/user/build-tools/android")
V33_DIR      = ANDROID_ROOT / "v33"
V34_DIR      = ANDROID_ROOT / "v34"
CURRENT_LINK = ANDROID_ROOT / "current"


def _assert_directory(path: Path):
    assert path.exists(), f"Expected directory {path} to exist."
    assert path.is_dir(), f"{path} exists but is not a directory (mode: {oct(path.lstat().st_mode)})"


def _assert_symlink(path: Path):
    assert path.exists(), f"Expected symlink {path} to exist."
    mode = path.lstat().st_mode
    assert stat.S_ISLNK(mode), (
        f"{path} exists but is not a symbolic link "
        f"(mode: {oct(mode)})"
    )


def test_android_root_directory_exists():
    """
    The base directory /home/user/build-tools/android must be present.
    """
    _assert_directory(ANDROID_ROOT)


def test_version_directories_exist():
    """
    Both v33 and v34 version directories must already exist.
    """
    _assert_directory(V33_DIR)
    _assert_directory(V34_DIR)


def test_current_symlink_points_to_v33():
    """
    The 'current' symlink must exist and *initially* resolve to v33.
    """
    _assert_symlink(CURRENT_LINK)

    # Path pointed to by the symlink (not resolved further)
    target = os.readlink(CURRENT_LINK)
    expected_target_suffix = "v33"
    assert target.endswith(expected_target_suffix), (
        f"Symlink {CURRENT_LINK} should point to '*{expected_target_suffix}', "
        f"but instead points to '{target}'."
    )

    # Fully-resolved absolute path should also end with /v33
    resolved = CURRENT_LINK.resolve()
    expected_resolved = V33_DIR
    assert resolved == expected_resolved, (
        f"Symlink {CURRENT_LINK} resolves to {resolved}, "
        f"but it should resolve to {expected_resolved}."
    )