# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student performs any action.  If any of these tests fail,
# the environment is not in the expected starting condition and the
# exercise itself is invalid.
#
# • Only stdlib + pytest are used.
# • Failure messages are explicit so that missing or mis-configured
#   items are obvious.

import os
import stat
from pathlib import Path

SECRETS_DIR = Path("/home/user/secrets")
API_TOKEN_FILE = SECRETS_DIR / "api_token.txt"
ROTATION_DIR = Path("/home/user/rotation")
CREDENTIALS_LOG = ROTATION_DIR / "credentials_rotation.log"

EXPECTED_API_CONTENT = b"SECRET_TOKEN_DO_NOT_SHARE\n"
DIR_MODE = 0o700
API_FILE_MODE = 0o644


def _mode(path: Path) -> int:
    """
    Return the permission bits (e.g., 0o755) for a path.
    """
    return stat.S_IMODE(path.stat().st_mode)


def test_secrets_directory_exists_with_correct_permissions():
    assert SECRETS_DIR.exists(), (
        f"Required directory {SECRETS_DIR} is missing."
    )
    assert SECRETS_DIR.is_dir(), (
        f"{SECRETS_DIR} exists but is not a directory."
    )
    assert _mode(SECRETS_DIR) == DIR_MODE, (
        f"{SECRETS_DIR} permissions are "
        f"{oct(_mode(SECRETS_DIR))}; expected {oct(DIR_MODE)} (0700)."
    )


def test_api_token_file_exists_with_correct_content_and_permissions():
    assert API_TOKEN_FILE.exists(), (
        f"Token file {API_TOKEN_FILE} is missing."
    )
    assert API_TOKEN_FILE.is_file(), (
        f"{API_TOKEN_FILE} exists but is not a file."
    )
    assert _mode(API_TOKEN_FILE) == API_FILE_MODE, (
        f"{API_TOKEN_FILE} permissions are "
        f"{oct(_mode(API_TOKEN_FILE))}; expected {oct(API_FILE_MODE)} (0644)."
    )

    content = API_TOKEN_FILE.read_bytes()
    assert content == EXPECTED_API_CONTENT, (
        f"{API_TOKEN_FILE} contents differ from expected. "
        "File must contain exactly 'SECRET_TOKEN_DO_NOT_SHARE' followed by "
        "a newline."
    )


def test_rotation_directory_exists_with_correct_permissions():
    assert ROTATION_DIR.exists(), (
        f"Required directory {ROTATION_DIR} is missing."
    )
    assert ROTATION_DIR.is_dir(), (
        f"{ROTATION_DIR} exists but is not a directory."
    )
    assert _mode(ROTATION_DIR) == DIR_MODE, (
        f"{ROTATION_DIR} permissions are "
        f"{oct(_mode(ROTATION_DIR))}; expected {oct(DIR_MODE)} (0700)."
    )


def test_credentials_rotation_log_state_if_present():
    """
    The rotation log file may or may not exist initially.  If it exists,
    it must end with a newline so that a new line can be appended cleanly.
    """
    if not CREDENTIALS_LOG.exists():
        # Absence is acceptable; pass the test.
        return

    assert CREDENTIALS_LOG.is_file(), (
        f"{CREDENTIALS_LOG} exists but is not a file."
    )

    data = CREDENTIALS_LOG.read_bytes()
    # An empty file or one ending in '\n' is acceptable.
    assert (not data) or data.endswith(b"\n"), (
        f"{CREDENTIALS_LOG} must end with a newline so that the next "
        "rotation entry can be appended on its own line."
    )