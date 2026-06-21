# test_initial_state.py
"""
Pytest suite that validates the *initial* on-disk state **before** the student
solution is run.  It verifies that the directory tree, files, and reference
manifest exactly match the specification given in the assignment.

Only the standard library and pytest are used.
"""

import os
import stat
import hashlib
import textwrap
import pytest

HOME = "/home/user"
BACKUPS_DIR = os.path.join(HOME, "backups")

# Helper ---------------------------------------------------------------------


def sha256_of_file(path: str) -> str:
    """Return the hex-encoded SHA-256 digest of the given file."""
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def file_mode(path: str) -> int:
    """Return the permission bits of the file (e.g. 0o644)."""
    return stat.S_IMODE(os.lstat(path).st_mode)


# Expected reference data -----------------------------------------------------

EXPECTED_REFERENCE_LINES = [
    "daily/db.sql.gz|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    "daily/files.tar.gz|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    "weekly/full.tar.gz|3|ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
]

FILES_AND_CONTENTS = {
    "daily/db.sql.gz": b"abc",
    "daily/files.tar.gz": b"abc",
    "weekly/full.tar.gz": b"def",
}

EXPECTED_DIRS = [
    BACKUPS_DIR,
    os.path.join(BACKUPS_DIR, "daily"),
    os.path.join(BACKUPS_DIR, "weekly"),
]


# Tests -----------------------------------------------------------------------


def test_directories_exist_and_permissions():
    """
    Required directories must exist with 0755 permissions.
    """
    for dpath in EXPECTED_DIRS:
        assert os.path.isdir(dpath), f"Directory missing: {dpath}"
        mode = file_mode(dpath)
        assert mode == 0o755, f"Directory {dpath} should be 755, found {oct(mode)}"


@pytest.mark.parametrize("relpath,expected_content", FILES_AND_CONTENTS.items())
def test_regular_files_exist_size_and_contents(relpath, expected_content):
    """
    Each regular file must exist, be 3 bytes long, and contain the expected data.
    """
    fpath = os.path.join(BACKUPS_DIR, relpath)
    assert os.path.isfile(fpath), f"File missing: {fpath}"
    size = os.path.getsize(fpath)
    assert size == 3, f"Expected size 3 for {fpath}, got {size}"
    with open(fpath, "rb") as fp:
        data = fp.read()
    assert (
        data == expected_content
    ), f"Unexpected content in {fpath!r}. Expected {expected_content!r}, got {data!r}"


def test_sha256s_match_expectations_for_daily_files():
    """
    The two daily files should match the hash in the reference manifest.
    """
    expected_hash = (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
    for relpath in ("daily/db.sql.gz", "daily/files.tar.gz"):
        fpath = os.path.join(BACKUPS_DIR, relpath)
        actual = sha256_of_file(fpath)
        assert (
            actual == expected_hash
        ), f"Hash mismatch for {fpath}: expected {expected_hash}, got {actual}"


def test_sha256_mismatch_for_weekly_file():
    """
    The weekly backup must *not* match the hash in the reference manifest, by design.
    """
    ref_hash = (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
    fpath = os.path.join(BACKUPS_DIR, "weekly/full.tar.gz")
    actual = sha256_of_file(fpath)
    assert (
        actual != ref_hash
    ), f"weekly/full.tar.gz unexpectedly matches the reference hash; it should differ."


def test_reference_manifest_exists_mode_and_format():
    """
    Validate the presence, permissions, newline termination, and exact content
    of /home/user/backups/reference-manifest.log
    """
    manifest_path = os.path.join(BACKUPS_DIR, "reference-manifest.log")
    assert os.path.isfile(manifest_path), "reference-manifest.log is missing"
    mode = file_mode(manifest_path)
    assert mode == 0o644, f"reference-manifest.log should be 644, found {oct(mode)}"

    with open(manifest_path, "rb") as fp:
        data = fp.read()

    # Must end with a single LF
    assert data.endswith(
        b"\n"
    ), "reference-manifest.log must end with exactly one newline character"

    # Split into lines (strip final LF first to avoid empty last element)
    lines = data.rstrip(b"\n").split(b"\n")
    decoded_lines = [ln.decode("utf-8") for ln in lines]

    assert (
        decoded_lines == EXPECTED_REFERENCE_LINES
    ), textwrap.dedent(
        f"""
        reference-manifest.log contents do not match expectation.
        Expected:
        {EXPECTED_REFERENCE_LINES}
        Got:
        {decoded_lines}
        """
    )