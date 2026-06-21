# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# before the student performs any action for the “world-writable
# security scan” exercise.
#
# Expectations (ground-truth):
#   1. Exactly two world-writable items exist under /home/user:
#        • /home/user/shared_data/suspicious.log   (regular file, mode 0o777)
#        • /home/user/shared_data/public           (directory,    mode 0o777)
#   2. No other regular file or directory anywhere below /home/user
#      is world-writable *at this point in time*.
#
# Notes:
#   • We purposely ignore everything beneath /home/user/security_scan
#     so we do not examine the location where the student will generate
#     their report.
#   • Only the Python standard library and pytest are used.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
IGNORED_SUBTREE = HOME / "security_scan"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def is_world_writable(path: Path) -> bool:
    """
    Return True if `path` (file or directory) has the UNIX “others” write bit set.
    Symlinks are *not* followed.
    """
    try:
        mode = path.lstat().st_mode  # lstat → do not follow symlinks
    except FileNotFoundError:
        # Path disappeared – treat as non-world-writable (will be caught elsewhere)
        return False
    return bool(mode & stat.S_IWOTH)


def collect_world_writable_items(base_dir: Path) -> set[Path]:
    """
    Walk `base_dir` and return a set containing every regular file or directory
    that is world-writable.  Symlinks are skipped.  Anything underneath the
    IGNORED_SUBTREE is ignored (to comply with the grading rules).
    """
    insecure: set[Path] = set()

    for root, dirs, files in os.walk(base_dir, topdown=True):
        root_path = Path(root)

        # Skip the subtree we must not inspect
        if IGNORED_SUBTREE in root_path.parents or root_path == IGNORED_SUBTREE:
            # Prevent os.walk from descending further
            dirs[:] = []
            continue

        # Inspect the directory currently being walked
        if root_path.is_dir() and is_world_writable(root_path):
            insecure.add(root_path)

        # Inspect child directories
        for d in dirs:
            dir_path = root_path / d
            if dir_path.is_dir() and is_world_writable(dir_path):
                insecure.add(dir_path)

        # Inspect regular files
        for f in files:
            file_path = root_path / f
            if file_path.is_symlink():
                continue
            if file_path.is_file() and is_world_writable(file_path):
                insecure.add(file_path)

    return insecure


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
EXPECTED_INSECURE = {
    HOME / "shared_data" / "suspicious.log",
    HOME / "shared_data" / "public",
}


@pytest.mark.parametrize("path", EXPECTED_INSECURE)
def test_expected_world_writable_item_exists_and_has_correct_permissions(path: Path):
    assert path.exists(), f"Required world-writable item is missing: {path}"
    if path.is_dir():
        assert path.is_dir(), f"{path} was expected to be a directory."
    else:
        assert path.is_file(), f"{path} was expected to be a regular file."
    assert is_world_writable(path), f"{path} exists but is *not* world-writable."


def test_no_unexpected_world_writable_items_exist():
    """
    Ensure that there are no additional world-writable regular files or
    directories under /home/user other than the two we expect.
    """
    found_insecure = collect_world_writable_items(HOME)
    missing = EXPECTED_INSECURE - found_insecure
    extra = found_insecure - EXPECTED_INSECURE

    assert not missing, (
        "The following expected world-writable items are missing or lack the "
        f"correct permissions: {sorted(str(p) for p in missing)}"
    )

    assert not extra, (
        "Unexpected world-writable files or directories were found under "
        f"{HOME} before the task started: {sorted(str(p) for p in extra)}"
    )