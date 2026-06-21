# test_initial_state.py
#
# Pytest suite that validates the *initial* condition of the filesystem
# before the student runs any command.  It checks that the directory tree
# under /home/user/public_data and /home/user/audit matches the specification
# in the assignment statement.

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
PUBLIC = HOME / "public_data"
AUDIT_DIR = HOME / "audit"

EXPECTED_DIRS = [
    PUBLIC,
    PUBLIC / "bin",
    PUBLIC / "scripts",
    AUDIT_DIR,
]

EXPECTED_FILES = {
    PUBLIC / "clean_readme.txt": 0o644,
    PUBLIC / "bin/tool": 0o755,
    PUBLIC / "scripts/run.sh": 0o775,
    PUBLIC / "scripts/unsafe.sh": 0o777,
}

WORLD_WRITABLE_EXECUTABLE = PUBLIC / "scripts/unsafe.sh"


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def octal_mode(path: Path) -> int:
    """Return the permission bits (e.g. 0o755) of a path."""
    return stat.S_IMODE(path.stat().st_mode)


def is_world_writable_exec(path: Path) -> bool:
    """True if path is a regular, world-writable file that is also executable."""
    if not path.is_file():
        return False
    mode = octal_mode(path)
    world_writable = bool(mode & stat.S_IWOTH)
    executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    return world_writable and executable


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_expected_directories_exist():
    missing = [str(d) for d in EXPECTED_DIRS if not d.is_dir()]
    assert not missing, (
        "The following expected directories are missing:\n  - " + "\n  - ".join(missing)
    )


def test_audit_directory_permissions_and_empty():
    assert AUDIT_DIR.is_dir(), f"Audit directory {AUDIT_DIR} is missing."

    mode = octal_mode(AUDIT_DIR)
    assert mode == 0o755, (
        f"Audit directory {AUDIT_DIR} should have mode 755, found {oct(mode)}."
    )

    contents = [p for p in AUDIT_DIR.iterdir() if p.name not in (".", "..")]
    assert (
        not contents
    ), f"Audit directory {AUDIT_DIR} should be empty initially, found: {contents}"


@pytest.mark.parametrize("path, expected_mode", EXPECTED_FILES.items())
def test_expected_files_exist_with_correct_permissions(path: Path, expected_mode: int):
    assert path.is_file(), f"Expected file {path} does not exist."
    mode = octal_mode(path)
    assert (
        mode == expected_mode
    ), f"File {path} should have mode {oct(expected_mode)}, found {oct(mode)}."


def test_only_one_world_writable_executable():
    found = []
    for root, _dirs, files in os.walk(PUBLIC):
        for fname in files:
            fpath = Path(root) / fname
            if is_world_writable_exec(fpath):
                found.append(fpath)

    assert found, "No world-writable executable files detected; at least one was expected."
    assert len(found) == 1 and found[0] == WORLD_WRITABLE_EXECUTABLE, (
        "Exactly one world-writable executable file should exist:\n"
        f"  Expected: {WORLD_WRITABLE_EXECUTABLE}\n"
        f"  Found: {found}"
    )