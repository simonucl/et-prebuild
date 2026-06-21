# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state that must be
# present **before** the student performs any actions for the deployment task.
#
# It checks:
#   • The expected directory structure for versions v1.0.0 and v1.1.0.
#   • The absence of the new v1.2.0 directory.
#   • The correctness of the existing `current` symlink.
#   • That `/home/user/deployment/deploy.log` is either missing or completely
#     empty.
#
# If any of these tests fail, the environment is not in the expected starting
# condition.

import os
from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/deployment")
RELEASES_DIR = BASE_DIR / "releases"
V100_DIR = RELEASES_DIR / "v1.0.0"
V110_DIR = RELEASES_DIR / "v1.1.0"
V120_DIR = RELEASES_DIR / "v1.2.0"
CURRENT_LINK = BASE_DIR / "current"
DEPLOY_LOG = BASE_DIR / "deploy.log"


def test_base_directories_exist():
    assert BASE_DIR.is_dir(), f"Missing base directory: {BASE_DIR}"
    assert RELEASES_DIR.is_dir(), f"Missing releases directory: {RELEASES_DIR}"


@pytest.mark.parametrize(
    "path", [V100_DIR, V110_DIR]
)
def test_existing_release_dirs_present(path: Path):
    assert path.is_dir(), f"Expected release directory {path} to exist"


def test_new_release_dir_absent():
    assert not V120_DIR.exists(), (
        f"Directory {V120_DIR} should NOT exist yet; it will be created by the student."
    )


def test_current_symlink_points_to_v1_1_0():
    assert CURRENT_LINK.exists(), f"Symlink {CURRENT_LINK} is missing"
    assert CURRENT_LINK.is_symlink(), f"{CURRENT_LINK} exists but is not a symlink"

    # Read the raw target of the symlink (do not resolve through the FS)
    target = os.readlink(CURRENT_LINK)
    expected_target = str(V110_DIR)

    assert target == expected_target, (
        f"Symlink {CURRENT_LINK} should point to {expected_target} "
        f"but points to {target}"
    )


def test_deploy_log_absent_or_empty():
    if DEPLOY_LOG.exists():
        assert DEPLOY_LOG.is_file(), f"{DEPLOY_LOG} exists but is not a regular file"
        size = DEPLOY_LOG.stat().st_size
        assert size == 0, (
            f"{DEPLOY_LOG} should be empty at the start; found {size} bytes"
        )
    else:
        # File legitimately does not exist yet
        assert not DEPLOY_LOG.exists(), (
            f"{DEPLOY_LOG} should not exist before the student's actions"
        )