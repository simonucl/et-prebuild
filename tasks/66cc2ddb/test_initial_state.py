# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student rotates credentials.  It checks that:
#   1. /home/user/app-container exists and is a directory.
#   2. Only one file is present inside it: secrets.env
#   3. The secrets.env file contains the expected “old” credentials.
#   4. The backup and log files do NOT yet exist.
#
# These guarantees ensure the student starts from a clean slate and that
# subsequent grading of their work is unambiguous.

import hashlib
from pathlib import Path
import pytest

APP_DIR = Path("/home/user/app-container")
SECRETS_FILE = APP_DIR / "secrets.env"
BACKUP_FILE = APP_DIR / "secrets.env.bak"
LOG_FILE = APP_DIR / "credential_rotation.log"

EXPECTED_SECRETS_CONTENT = (
    "API_KEY=OLD-KEY-ABC\n"
    "DB_PASSWORD=OldPass123"
)


def _normalized_file_content(path: Path) -> str:
    """
    Read the file, normalizing line endings to '\n' and stripping a single
    trailing newline (if present) so comparisons are robust.
    """
    data = path.read_bytes()
    # Force universal newline handling then strip one trailing newline
    text = data.decode("utf-8").replace("\r\n", "\n")
    return text[:-1] if text.endswith("\n") else text


def test_app_directory_exists():
    assert APP_DIR.exists(), f"Required directory {APP_DIR} is missing."
    assert APP_DIR.is_dir(), f"{APP_DIR} exists but is not a directory."


def test_only_secrets_file_present():
    files = sorted(p.name for p in APP_DIR.iterdir())
    assert files == ["secrets.env"], (
        f"{APP_DIR} should initially contain only 'secrets.env' but contains: {files}"
    )


def test_secrets_file_content_is_old_credentials():
    assert SECRETS_FILE.exists(), "Expected secrets.env file is missing."
    content = _normalized_file_content(SECRETS_FILE)
    assert (
        content == EXPECTED_SECRETS_CONTENT
    ), (
        "secrets.env does not contain the expected old credentials.\n"
        "Expected:\n"
        f"{EXPECTED_SECRETS_CONTENT!r}\n\n"
        "Found:\n"
        f"{content!r}"
    )


def test_backup_and_log_do_not_exist():
    assert not BACKUP_FILE.exists(), (
        f"Backup file {BACKUP_FILE} should NOT exist before rotation."
    )
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should NOT exist before rotation."
    )