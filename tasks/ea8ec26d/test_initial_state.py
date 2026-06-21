# test_initial_state.py
#
# Pytest suite that verifies the **initial** on-disk state *before*
# the student performs any actions for the “dataset sync” exercise.
#
# What we check:
# • The two dataset directories exist at their full absolute paths.
# • The local authoritative copy already contains sample1–3.csv
#   with the exact expected contents.
# • The remote copy contains only sample1.csv and sample3.csv,
#   both byte-for-byte identical to their local counterparts.
#   sample2.csv must be ABSENT on the remote side.
# • The verification log /home/user/dataset_sync.log must NOT exist yet.
#
# These tests purposefully do *not* check the final state that will
# result from the student’s solution; they only confirm that the
# starting filesystem state matches the specification.

import hashlib
from pathlib import Path

import pytest


# ---------- Helper utilities -------------------------------------------------
LOCAL_DIR = Path("/home/user/workspace/datasets")
REMOTE_DIR = Path("/home/user/remote_share/datasets")
SYNC_LOG = Path("/home/user/dataset_sync.log")

EXPECTED_LOCAL_CONTENT = {
    "sample1.csv": "id,value\n1,10\n2,20\n",
    "sample2.csv": "id,value\n3,30\n4,40\n",
    "sample3.csv": "id,value\n5,50\n6,60\n",
}


def sha1sum(path: Path) -> str:
    """Return the SHA-1 hex digest of a file."""
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- Tests ------------------------------------------------------------


def test_directories_exist_and_are_writable():
    """Both dataset directories must exist and be writable by the user."""
    for directory in (LOCAL_DIR, REMOTE_DIR):
        assert directory.exists(), f"Directory missing: {directory}"
        assert directory.is_dir(), f"Expected a directory, found something else: {directory}"
        # Touch a temporary file to confirm write permission, then remove it.
        try:
            tmp = directory / ".pytest_write_check"
            tmp.touch()
            tmp.unlink()
        except Exception as exc:
            pytest.fail(f"Directory not writable by user: {directory}\n{exc}")


def test_local_files_exist_with_expected_contents():
    """Local authoritative folder must have the three CSVs with exact contents."""
    for filename, expected_content in EXPECTED_LOCAL_CONTENT.items():
        path = LOCAL_DIR / filename
        assert path.exists(), f"Missing local file: {path}"
        assert path.is_file(), f"Expected a regular file, found something else: {path}"
        actual = path.read_text(encoding="utf-8")
        assert (
            actual == expected_content
        ), f"Content mismatch in {path}.\nExpected:\n{expected_content!r}\nFound:\n{actual!r}"


def test_remote_contains_only_sample1_and_sample3():
    """Remote folder should initially have only sample1.csv and sample3.csv."""
    expected_files = {"sample1.csv", "sample3.csv"}
    remote_files = {p.name for p in REMOTE_DIR.iterdir() if p.is_file()}
    missing = expected_files - remote_files
    unexpected = remote_files - expected_files

    assert not missing, f"Remote dataset is missing expected files: {sorted(missing)}"
    assert not unexpected, f"Remote dataset has unexpected extra files: {sorted(unexpected)}"
    assert not (REMOTE_DIR / "sample2.csv").exists(), (
        "sample2.csv must NOT exist in the remote directory at the initial state."
    )


def test_remote_files_are_identical_to_local_copies():
    """sample1.csv and sample3.csv must be byte-for-byte identical between local and remote."""
    for filename in ("sample1.csv", "sample3.csv"):
        local_path = LOCAL_DIR / filename
        remote_path = REMOTE_DIR / filename
        assert local_path.exists() and remote_path.exists(), (
            f"Expected both local and remote copies of {filename} to exist."
        )

        local_hash = sha1sum(local_path)
        remote_hash = sha1sum(remote_path)
        assert (
            local_hash == remote_hash
        ), f"File {filename} differs between local and remote.\nLocal SHA-1:  {local_hash}\nRemote SHA-1: {remote_hash}"


def test_sync_log_not_yet_present():
    """The verification log should NOT exist before the student runs their commands."""
    assert not SYNC_LOG.exists(), (
        f"{SYNC_LOG} should not exist at the initial state. "
        "It must be created by the student's solution."
    )