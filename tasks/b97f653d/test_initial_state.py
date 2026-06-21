# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state that must be
# present *before* the student writes any code or runs any deployment commands.
# It deliberately does NOT test for any artefacts that the student is expected
# to create or modify (e.g., deploy_update.sh, last_deploy.info, the updated
# target of /home/user/app/current, etc.).

import os
import pathlib
import stat
import pytest

HOME = pathlib.Path("/home/user")
APP_DIR = HOME / "app"
RELEASES_DIR = APP_DIR / "releases"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _assert_exists(path: pathlib.Path, *, is_dir=False, is_file=False, is_symlink=False):
    """
    Assert that `path` exists and has the requested type.
    """
    assert path.exists(), f"Expected path to exist: {path}"
    if is_dir:
        assert path.is_dir(), f"Expected directory at {path}, but it's not a directory."
    if is_file:
        # For regular files we want to make sure it's not a directory or symlink
        assert path.is_file(), f"Expected regular file at {path}, but it's not a file."
        assert not path.is_dir(), f"Expected regular file at {path}, but found directory."
    if is_symlink:
        assert path.is_symlink(), f"Expected symlink at {path}, but it's not a symlink."


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_releases_directory_structure():
    """
    /home/user/app/releases/ must exist with the expected version sub-directories.
    """
    _assert_exists(RELEASES_DIR, is_dir=True)

    expected_versions = ["v1.0", "v1.1", "v2.0"]
    found_versions = sorted(
        p.name for p in RELEASES_DIR.iterdir() if p.is_dir()
    )

    for ver in expected_versions:
        assert ver in found_versions, (
            f"Missing release directory: {RELEASES_DIR / ver}"
        )


@pytest.mark.parametrize("version", ["v1.0", "v1.1", "v2.0"])
def test_each_release_has_version_file(version):
    """
    Each release directory must contain version.txt with the correct content.
    """
    ver_dir = RELEASES_DIR / version
    _assert_exists(ver_dir, is_dir=True)

    version_file = ver_dir / "version.txt"
    _assert_exists(version_file, is_file=True)

    expected_content = f"{version}\n"
    content = version_file.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"Expected {version_file} to contain {expected_content!r}, "
        f"but found {content!r}"
    )


def test_current_symlink_initial_target():
    """
    /home/user/app/current must be a symlink that *currently* points at v1.0.
    """
    current_link = APP_DIR / "current"
    _assert_exists(current_link, is_symlink=True)

    # Resolve the absolute path (no '..' components, follow all symlinks)
    resolved_target = current_link.resolve()
    expected_target = RELEASES_DIR / "v1.0"
    assert resolved_target == expected_target, (
        f"Symlink {current_link} should point to {expected_target}, "
        f"but points to {resolved_target}"
    )


def test_deploy_log_exists_and_empty():
    """
    /home/user/app/deploy.log must exist and be empty at the start.
    """
    deploy_log = APP_DIR / "deploy.log"
    _assert_exists(deploy_log, is_file=True)

    size = deploy_log.stat().st_size
    assert size == 0, (
        f"Expected {deploy_log} to be empty initially, "
        f"but its size is {size} bytes"
    )