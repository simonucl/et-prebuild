# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# for the “backup-operator” exercise **before** the student executes any
# commands.  If any of these tests fail, the lab has not been set up
# correctly or the student has already modified the system.
#
# Only Python’s stdlib + pytest are used.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SRC_DIR = HOME / "backup_source"
BACKUPS_DIR = HOME / "backups"
RESTORE_DIR = HOME / "restore_test"
ARCHIVE = BACKUPS_DIR / "full_backup_2023-09-15.tar.gz"

FILES_INFO = {
    SRC_DIR / "test.txt": {
        "content": b"test",
        "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    },
    SRC_DIR / "hello.txt": {
        "content": b"hello",
        "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
    },
    SRC_DIR / "empty.dat": {
        "content": b"",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
}


def sha256sum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Expected file does not exist: {path}", pytrace=False)


class TestInitialFilesystemState:
    # ------------------------------------------------------------------ #
    # Positive assertions: what *must* be present when the lab starts.
    # ------------------------------------------------------------------ #

    def test_source_directory_exists_and_is_directory(self):
        assert SRC_DIR.exists(), f"Required directory missing: {SRC_DIR}"
        assert SRC_DIR.is_dir(), f"{SRC_DIR} exists but is not a directory."

    @pytest.mark.parametrize("file_path", FILES_INFO.keys())
    def test_required_files_exist(self, file_path: Path):
        assert file_path.exists(), f"Missing required file: {file_path}"
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    def test_no_extra_items_in_source_directory(self):
        present = sorted(p.name for p in SRC_DIR.iterdir())
        expected = sorted(p.name for p in FILES_INFO)
        assert present == expected, (
            f"{SRC_DIR} should contain only {expected} but found {present}"
        )

    @pytest.mark.parametrize("file_path, info", FILES_INFO.items())
    def test_file_contents_and_hashes(self, file_path: Path, info: dict):
        data = _read_bytes(file_path)
        assert data == info["content"], (
            f"Content mismatch in {file_path}. "
            f"Expected {info['content']!r} but got {data!r}"
        )
        digest = sha256sum(data)
        assert digest == info["sha256"], (
            f"SHA-256 mismatch for {file_path}. "
            f"Expected {info['sha256']} but got {digest}"
        )

    # ------------------------------------------------------------------ #
    # Negative assertions: what *must NOT* exist before student actions.
    # ------------------------------------------------------------------ #

    def test_backups_directory_absent(self):
        assert not BACKUPS_DIR.exists(), (
            f"{BACKUPS_DIR} should NOT exist at the start of the exercise."
        )

    def test_restore_directory_absent(self):
        assert not RESTORE_DIR.exists(), (
            f"{RESTORE_DIR} should NOT exist at the start of the exercise."
        )

    def test_archive_absent(self):
        assert not ARCHIVE.exists(), (
            f"{ARCHIVE} should NOT exist before the backup is created."
        )