# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state for the
“API integration” deployment exercise **before** the student performs
any action.

This file must be executed *prior* to the student-authored solution.
Any failure here indicates that the provided starting environment is
already out of sync with the specification and therefore the exercise
cannot be graded reliably.
"""
from pathlib import Path
import os
import pytest

# Base paths used throughout the checks
ROOT = Path("/home/user/projects/api_integration").resolve()

RELEASES = ROOT / "releases"
SHARED = ROOT / "shared"
V1 = RELEASES / "v1"
V2 = RELEASES / "v2"
CURRENT_RELEASE = ROOT / "current_release"
LIBS_DIR = ROOT / "libs"
LEGACY_BACKUP = RELEASES / "legacy_libs_backup"
AUDIT_LOG = ROOT / "link_update.log"


def _assert_is_dir(p: Path, msg: str = ""):
    assert p.exists(), f"Expected directory {p} to exist. {msg}"
    assert p.is_dir(), f"Expected {p} to be a directory, but it is not. {msg}"


def test_project_root_layout():
    """
    Verify that the mandatory directory hierarchy exists and has the
    correct types (directory vs. symlink) **before** the update.
    """
    # 1. Root directory
    _assert_is_dir(ROOT, "Project root missing.")

    # 2. releases/v1 and releases/v2
    _assert_is_dir(V1, "Legacy release v1 is missing.")
    _assert_is_dir(V2, "Release v2 (to be promoted) is missing.")

    # 3. shared/config and shared/libs must be *real* directories
    _assert_is_dir(SHARED / "config",
                   "Shared config directory is missing or not a directory.")
    _assert_is_dir(SHARED / "libs",
                   "Shared libs directory is missing or not a directory.")

    # 4. libs is currently a *directory* (not a symlink) and contains sub-folders v1 and v2
    _assert_is_dir(LIBS_DIR,
                   "'libs' should be a real directory prior to the task.")
    assert not LIBS_DIR.is_symlink(), (
        f"{LIBS_DIR} should be a real directory (will be replaced by "
        "a symlink later)."
    )
    for sub in ("v1", "v2"):
        _assert_is_dir(LIBS_DIR / sub,
                       f"Expected sub-folder {LIBS_DIR/sub} to exist.")

    # 5. current_release exists and is a *dangling* symlink
    assert CURRENT_RELEASE.exists() or CURRENT_RELEASE.is_symlink(), (
        f"{CURRENT_RELEASE} should exist as a (dangling) symlink."
    )
    assert CURRENT_RELEASE.is_symlink(), (
        f"{CURRENT_RELEASE} must be a symlink before replacement."
    )
    resolved = CURRENT_RELEASE.resolve(strict=False)
    # If it were *not* dangling, the resolved path would exist.
    assert not resolved.exists(), (
        f"{CURRENT_RELEASE} is expected to be a dangling symlink, "
        f"but it resolves to an existing path ({resolved})."
    )


def test_objects_that_must_not_exist_yet():
    """
    Ensure that artefacts produced *by* the task are not pre-existing.
    This guarantees that the student’s work will be the first to create
    them and the audit log remains authoritative.
    """
    # 1. Backup directory must not exist
    assert not LEGACY_BACKUP.exists(), (
        f"The backup directory {LEGACY_BACKUP} should NOT exist yet."
    )

    # 2. Audit log file must not exist
    assert not AUDIT_LOG.exists(), (
        f"Audit file {AUDIT_LOG} should NOT exist before the task."
    )

    # 3. Inside v2, 'config' symlink may or may not exist; no constraint
    #    because the spec allows replacement.  Therefore we deliberately
    #    do *not* assert on it.


@pytest.mark.parametrize(
    "path",
    [
        RELEASES / "v2" / "libs",
    ],
)
def test_release_v2_contains_required_subdirs(path: Path):
    """
    A sanity check that release v2 already has the sub-directories that
    future symlinks will point to.
    """
    _assert_is_dir(path, f"Expected {path} to exist inside release v2.")