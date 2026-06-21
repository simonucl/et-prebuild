# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state for the “backup-restore” exercise _before_ the student performs any
# actions.

import os
import tarfile
import pytest

# CONSTANTS -------------------------------------------------------------------

ARCHIVE_PATH = "/home/user/backup_repo/system_backup_2023-10-05.tar.gz"

# Mapping: {tar_path: expected_bytes_contents}
EXPECTED_FILES = {
    "etc/hostname": b"backup-test-host\n",
    "etc/ssh/sshd_config": (
        b"# SSH Daemon Config for testing\n"
        b"Port 2222\n"
        b"PermitRootLogin no\n"
        b"PasswordAuthentication yes\n"
    ),
    "var/log/test.log": b"This is a test log for restore validation.\n",
}

# TESTS -----------------------------------------------------------------------


def test_archive_exists_and_is_readable():
    """
    Verify that the backup archive exists and is readable **before** the
    student starts the task.
    """
    assert os.path.isfile(
        ARCHIVE_PATH
    ), f"Required archive not found: {ARCHIVE_PATH!r}"
    assert os.access(
        ARCHIVE_PATH, os.R_OK
    ), f"Archive exists but is not readable: {ARCHIVE_PATH!r}"


@pytest.mark.depends(on=["test_archive_exists_and_is_readable"])
def test_archive_has_expected_contents_and_only_those():
    """
    Open the .tar.gz and ensure that …

      1. Every expected file is present.
      2. Each file’s byte-for-byte contents match the truth.
      3. No unexpected **regular files** are present in the archive.
         (Directories are ignored.)
    """
    with tarfile.open(ARCHIVE_PATH, mode="r:gz") as tf:
        # Build a mapping of {normalized_name: TarInfo}
        members = {
            _normalize_tar_name(m.name): m
            for m in tf.getmembers()
            if m.isfile()
        }

        # 1. All expected files must be present.
        missing = [name for name in EXPECTED_FILES if name not in members]
        assert (
            not missing
        ), f"Archive is missing expected file(s): {', '.join(missing)}"

        # 2. Contents and size checks.
        for name, expected_bytes in EXPECTED_FILES.items():
            tarinfo = members[name]
            with tf.extractfile(tarinfo) as fh:
                actual = fh.read()

            assert (
                actual == expected_bytes
            ), f"Contents of {name!r} in archive differ from expected."
            assert (
                len(actual) == tarinfo.size == len(expected_bytes)
            ), f"Size mismatch for {name!r} (archive says {tarinfo.size} bytes, expected {len(expected_bytes)})."

        # 3. No unexpected regular files.
        extra_files = [name for name in members if name not in EXPECTED_FILES]
        assert (
            not extra_files
        ), f"Archive contains unexpected file(s): {', '.join(extra_files)}"


# HELPERS ---------------------------------------------------------------------


def _normalize_tar_name(name: str) -> str:
    """
    Tar files sometimes store paths with a leading "./".
    Normalize them so that, e.g., "./etc/hostname" becomes "etc/hostname".
    """
    return name.lstrip("./")