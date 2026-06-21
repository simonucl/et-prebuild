# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating system
# before the student performs any restore actions.

import os
import tarfile
import pytest
from pathlib import Path

# Constants -------------------------------------------------------------------

BACKUP_DIR          = Path("/home/user/backup_server/home_snapshots")
BACKUP_FILE         = BACKUP_DIR / "projectA_2023-08-01.tar.gz"
RESTORE_DIR         = Path("/home/user/restore_test")

EXPECTED_MEMBERS = {
    "projectA/file1.txt": b"Alpha\n",
    "projectA/file2.txt": b"Beta\n",
    "projectA/notes.md": (
        b"# Project A Notes\n"
        b"Restored successfully.\n"
    ),
}


# Helper ----------------------------------------------------------------------

def _read_member_bytes(tar: tarfile.TarFile, member_name: str) -> bytes:
    """Return the full byte content of a member inside the opened tarfile."""
    member = tar.getmember(member_name)
    fileobj = tar.extractfile(member)
    assert fileobj is not None, f"Tar member {member_name!r} could not be read."
    data = fileobj.read()
    fileobj.close()
    return data


# Tests -----------------------------------------------------------------------

def test_backup_share_and_file_exist():
    """Verify that the backup share and the snapshot archive exist."""
    assert BACKUP_DIR.is_dir(), (
        f"Expected backup directory {BACKUP_DIR} does not exist."
    )
    assert BACKUP_FILE.is_file(), (
        f"Expected snapshot archive {BACKUP_FILE} is missing."
    )


def test_restore_directory_absent():
    """The restore target directory must NOT exist at the beginning."""
    assert not RESTORE_DIR.exists(), (
        f"Directory {RESTORE_DIR} should not exist before the task starts."
    )


def test_tar_contains_exact_expected_members():
    """The tar archive must contain exactly the expected files with correct content."""
    # Open the tar archive as gzip.
    with tarfile.open(BACKUP_FILE, mode="r:gz") as tar:

        # Collect all file names that are *regular files* (skip directories, etc.)
        actual_files = {
            m.name for m in tar.getmembers() if m.isfile()
        }

        expected_files = set(EXPECTED_MEMBERS.keys())

        # Check that the set of files matches exactly.
        missing = expected_files - actual_files
        extra   = actual_files  - expected_files

        assert not missing, (
            f"The archive is missing the following expected file(s): {sorted(missing)}"
        )
        assert not extra, (
            f"The archive contains unexpected extra file(s): {sorted(extra)}"
        )

        # For each expected file, verify its size and contents.
        for rel_path, expected_bytes in EXPECTED_MEMBERS.items():
            member = tar.getmember(rel_path)

            # Size check
            assert member.size == len(expected_bytes), (
                f"Size mismatch for {rel_path!r}: expected {len(expected_bytes)} "
                f"bytes but found {member.size} bytes in the archive."
            )

            # Content check
            data = _read_member_bytes(tar, rel_path)
            assert data == expected_bytes, (
                f"Content mismatch for {rel_path!r} inside the archive."
            )