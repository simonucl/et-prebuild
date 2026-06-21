# test_initial_state.py
#
# Pytest suite that validates the initial state of the workstation **before**
# the student runs any solution code.  It checks that the expected directory
# hierarchy and the known world-writable files are present and that no other
# regular files beneath /home/user are world-writable.
#
# NOTE:
# • The output artefact `/home/user/security_scan/world_writable_files.txt`
#   is deliberately **not** tested for here, because it must not exist yet.
# • Only stdlib modules are used, in accordance with the grading rules.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()

# Expected world-writable regular files (absolute paths)
EXPECTED_WW_FILES = {
    HOME / "scripts" / "run.sh",
    HOME / "shared" / "public.txt",
}


def is_world_writable(path: Path) -> bool:
    """Return True if `path` is a regular file that is world-writable."""
    try:
        st = path.stat(follow_symlinks=False)
    except FileNotFoundError:
        return False
    return stat.S_ISREG(st.st_mode) and bool(st.st_mode & stat.S_IWOTH)


def test_required_directories_exist():
    """Verify that the required directory structure is present."""
    required_dirs = [
        HOME / "shared",
        HOME / "scripts",
        HOME / "security_scan",
    ]

    for d in required_dirs:
        assert d.exists(), f"Required directory missing: {d}"
        assert d.is_dir(), f"Expected {d} to be a directory"


def test_world_writable_files_present_and_correct():
    """Ensure the known world-writable files exist and have correct permissions."""
    for ww_file in EXPECTED_WW_FILES:
        assert ww_file.exists(), f"Expected world-writable file is missing: {ww_file}"
        assert ww_file.is_file(), f"Expected {ww_file} to be a regular file"

        st_mode = ww_file.stat().st_mode
        assert st_mode & stat.S_IWOTH, (
            f"{ww_file} is expected to be world-writable but is not "
            f"(mode: {oct(st_mode & 0o777)})"
        )


def test_no_unexpected_world_writable_files():
    """
    Walk the entire /home/user tree and ensure that no *additional* regular
    files are world-writable.
    """
    found_ww_files = set()

    for root, dirs, files in os.walk(HOME, followlinks=False):
        for name in files:
            path = Path(root) / name
            if is_world_writable(path):
                found_ww_files.add(path.resolve())

    assert found_ww_files == EXPECTED_WW_FILES, (
        "Mismatch in world-writable files detected.\n"
        f"Expected:\n  {', '.join(sorted(map(str, EXPECTED_WW_FILES)))}\n"
        f"Found:\n  {', '.join(sorted(map(str, found_ww_files)))}"
    )