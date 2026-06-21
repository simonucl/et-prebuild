# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating-system
# filesystem before the student script runs.  It makes sure the directory
# /home/user/secure_data/ contains exactly the expected files with the
# correct permissions and nothing else.  It deliberately avoids looking at
# any of the *output* paths (/home/user/audit/ or its contents), in
# accordance with the grading rules.

import os
import stat
from pathlib import Path

import pytest

SECURE_DATA_DIR = Path("/home/user/secure_data")

# Mapping of filename -> expected octal permission bits (lowest three digits).
EXPECTED_FILES = {
    "secret.conf": 0o640,
    "public.txt": 0o666,   # world-writable
    "notes.log": 0o606,    # world-writable
    "readme.md": 0o644,
    "archive.tar.gz": 0o600,
}


def _octal_777(mode: int) -> int:
    """Return the lowest three octal digits of an st_mode."""
    return stat.S_IMODE(mode) & 0o777


@pytest.fixture(scope="module")
def secure_path():
    assert SECURE_DATA_DIR.exists(), (
        f"Required directory {SECURE_DATA_DIR} is missing."
    )
    assert SECURE_DATA_DIR.is_dir(), (
        f"{SECURE_DATA_DIR} exists but is not a directory."
    )
    return SECURE_DATA_DIR


def test_expected_file_set(secure_path):
    """The directory must contain exactly the expected filenames and no others."""
    actual_files = sorted(
        p.name for p in secure_path.iterdir() if p.is_file()
    )
    expected_files = sorted(EXPECTED_FILES.keys())

    extra = set(actual_files) - set(expected_files)
    missing = set(expected_files) - set(actual_files)

    msg_parts = []
    if missing:
        msg_parts.append(f"Missing files: {', '.join(sorted(missing))}")
    if extra:
        msg_parts.append(f"Unexpected extra files: {', '.join(sorted(extra))}")

    assert not missing and not extra, (
        "secure_data directory contents do not match expectation. "
        + " ; ".join(msg_parts)
    )


@pytest.mark.parametrize("filename,expected_perm", EXPECTED_FILES.items())
def test_file_permissions_and_type(secure_path, filename, expected_perm):
    """Each file must be a regular file with the exact expected permissions."""
    file_path = secure_path / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    actual_perm = _octal_777(file_path.stat().st_mode)
    assert actual_perm == expected_perm, (
        f"{file_path} has permission {oct(actual_perm)[2:]}, "
        f"but expected {oct(expected_perm)[2:]}."
    )


def test_world_writable_flags(secure_path):
    """
    Verify that only notes.log and public.txt are world-writable, and that
    the other files are *not* world-writable.
    """
    world_writable_files = []
    for path in secure_path.iterdir():
        if not path.is_file():
            continue
        mode = _octal_777(path.stat().st_mode)
        if mode & 0o002:
            world_writable_files.append(path.name)

    expected_world_writable = {"public.txt", "notes.log"}
    assert set(world_writable_files) == expected_world_writable, (
        "World-writable file set is incorrect.\n"
        f"Expected: {sorted(expected_world_writable)}\n"
        f"Found   : {sorted(world_writable_files)}"
    )