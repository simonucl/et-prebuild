# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system state
# before the student performs the credential-rotation exercise.
#
# It checks that:
#   • The /home/user/secops/ directory and the original CSV exist.
#   • The original CSV’s bytes exactly match the specification.
#   • No archive/ or rotation_logs/ directories (nor any of the
#     post-rotation deliverables) are present yet.
#
# If any assertion fails the message will clearly describe what is
# missing or unexpectedly present.

import hashlib
from pathlib import Path
import pytest

SECOPS_DIR = Path("/home/user/secops")
ORIGINAL_CSV = SECOPS_DIR / "credentials_2023-12-01.csv"

ARCHIVE_DIR = SECOPS_DIR / "archive"
BACKUP_CSV = ARCHIVE_DIR / "credentials_2023-12-01.csv.bak"

NEW_CSV = SECOPS_DIR / "credentials_2024-06-01.csv"

LOG_DIR = SECOPS_DIR / "rotation_logs"
LOG_FILE = LOG_DIR / "rotate_2024-06-01.log"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def sha256_of(path: Path) -> str:
    """Return the hex-encoded SHA256 of a file."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_secops_directory_exists():
    assert SECOPS_DIR.is_dir(), (
        "Required directory /home/user/secops/ is missing. "
        "It must exist before rotation begins."
    )


def test_original_credentials_file_present_and_correct():
    assert ORIGINAL_CSV.is_file(), (
        "Original credential file "
        "/home/user/secops/credentials_2023-12-01.csv is missing."
    )

    expected_lines = [
        "username,service,credential_id,created_at,expires_at\n",
        "alice,db,credA1,2023-12-01,2024-06-01\n",
        "bob,web,credB2,2023-12-01,2024-06-01\n",
        "carol,api,credC3,2023-12-01,2024-06-01\n",
    ]
    expected_bytes = "".join(expected_lines).encode("utf-8")

    actual_bytes = ORIGINAL_CSV.read_bytes()

    assert actual_bytes == expected_bytes, (
        "The contents of credentials_2023-12-01.csv do not match the expected "
        "pre-rotation data. Ensure the file is unmodified and byte-perfect."
    )


def test_no_archive_or_backup_yet():
    assert not ARCHIVE_DIR.exists(), (
        "Directory /home/user/secops/archive/ should NOT exist before rotation."
    )
    assert not BACKUP_CSV.exists(), (
        "Backup file credentials_2023-12-01.csv.bak should NOT exist before rotation."
    )


def test_no_new_credentials_file_yet():
    assert not NEW_CSV.exists(), (
        "File /home/user/secops/credentials_2024-06-01.csv should NOT exist before rotation."
    )


def test_no_rotation_logs_yet():
    assert not LOG_DIR.exists(), (
        "Directory /home/user/secops/rotation_logs/ should NOT exist before rotation."
    )
    assert not LOG_FILE.exists(), (
        "Log file rotate_2024-06-01.log should NOT exist before rotation."
    )