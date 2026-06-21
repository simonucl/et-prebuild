# test_initial_state.py
#
# Pytest test-suite that validates the *initial* operating-system / filesystem
# state **before** the student performs any actions.  It confirms that the
# provided backup files and checksum reference are present and 100 % correct.
#
# The tests purposefully do *not* look for any artefacts that the student is
# supposed to create later (e.g. verification_logs/).

import hashlib
import os
import pathlib

import pytest

HOME = pathlib.Path("/home/user")
BACKUP_DIR = HOME / "site_backups"
EXPECTED_CHECKSUM_FILE = BACKUP_DIR / "expected_checksums.txt"

BACKUP_FILES = {
    "alice": BACKUP_DIR / "alice.txt",
    "bob": BACKUP_DIR / "bob.txt",
    "charlie": BACKUP_DIR / "charlie.txt",
}

HELLO_BYTES = b"hello"
HELLO_SHA256 = (
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
)

EXPECTED_CHECKSUMS_TEXT = (
    "alice,2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824\n"
    "bob,2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824\n"
    "charlie,2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824\n"
)


def sha256_of_file(path: pathlib.Path) -> str:
    """Return the hex-encoded SHA-256 digest of a file (lower-case)."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_backup_directory_exists():
    assert BACKUP_DIR.is_dir(), (
        f"Directory {BACKUP_DIR!s} is missing. "
        "The initial backup directory must exist."
    )


@pytest.mark.parametrize("user", ["alice", "bob", "charlie"])
def test_backup_files_exist_and_content(user):
    path = BACKUP_FILES[user]
    assert path.is_file(), f"Expected backup file {path!s} is missing."

    size = path.stat().st_size
    assert size == len(HELLO_BYTES), (
        f"File {path!s} should be exactly {len(HELLO_BYTES)} bytes "
        f"but is {size} bytes."
    )

    with path.open("rb") as fh:
        content = fh.read()
    assert content == HELLO_BYTES, (
        f"File {path!s} should contain ASCII 'hello' without a newline. "
        f"Found content: {content!r}"
    )


def test_expected_checksum_file_exists_and_content():
    assert EXPECTED_CHECKSUM_FILE.is_file(), (
        f"Checksum reference file {EXPECTED_CHECKSUM_FILE!s} is missing."
    )

    with EXPECTED_CHECKSUM_FILE.open("r", encoding="utf-8") as fh:
        content = fh.read()

    assert content == EXPECTED_CHECKSUMS_TEXT, (
        "Content of expected_checksums.txt does not match the required text.\n"
        "Expected:\n"
        f"{EXPECTED_CHECKSUMS_TEXT!r}\n"
        "Found:\n"
        f"{content!r}"
    )


@pytest.mark.parametrize("user", ["alice", "bob", "charlie"])
def test_actual_checksums_match_reference(user):
    """
    Compute the SHA-256 of each backup file and make sure it equals the digest
    listed in expected_checksums.txt.
    """
    path = BACKUP_FILES[user]
    actual_digest = sha256_of_file(path)
    assert (
        actual_digest == HELLO_SHA256
    ), f"SHA-256 for {path!s} should be {HELLO_SHA256} but is {actual_digest}."