# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the filesystem **before** the
student performs any credential-rotation actions.

It asserts that:
1. /home/user/credentials exists and is a directory.
2. settings.yml and settings.toml both exist with the *old* credential values
   exactly as described in the task.
3. No rotation.log file exists yet.
4. File permissions for the two existing files are 0644.

Any deviation from this baseline state means the exercise is starting from an
unexpected point and will raise a clear, actionable failure message.
"""

import os
import stat
import pytest

CRED_DIR = "/home/user/credentials"
YML_PATH = os.path.join(CRED_DIR, "settings.yml")
TOML_PATH = os.path.join(CRED_DIR, "settings.toml")
LOG_PATH = os.path.join(CRED_DIR, "rotation.log")

EXPECTED_YML = (
    "aws:\n"
    "  access_key_id: OLD_ACCESS_KEY\n"
    "  secret_access_key: OLD_SECRET_KEY\n"
    "database:\n"
    "  user: dbuser\n"
    "  password: verysecret\n"
)

EXPECTED_TOML = (
    "[aws]\n"
    "access_key_id = \"OLD_ACCESS_KEY\"\n"
    "secret_access_key = \"OLD_SECRET_KEY\"\n"
    "\n"
    "[database]\n"
    "user = \"dbuser\"\n"
    "password = \"verysecret\"\n"
)


def _assert_mode_0644(path: str):
    """
    Helper that asserts a file has mode 0644.
    Provides a meaningful message on failure.
    """
    st_mode = os.stat(path).st_mode
    perms = stat.S_IMODE(st_mode)
    assert perms == 0o644, (
        f"File '{path}' should have permissions 0644 (octal), "
        f"but has {oct(perms)} instead."
    )


def test_credentials_directory_exists():
    assert os.path.isdir(CRED_DIR), (
        f"Expected credentials directory '{CRED_DIR}' to exist, "
        "but it was not found or is not a directory."
    )


@pytest.mark.parametrize("path, expected_content", [
    (YML_PATH, EXPECTED_YML),
    (TOML_PATH, EXPECTED_TOML),
])
def test_settings_files_exist_with_expected_content(path, expected_content):
    # File existence
    assert os.path.isfile(path), f"Required file '{path}' does not exist."

    # Permissions 0644
    _assert_mode_0644(path)

    # Exact content check
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()

    assert actual == expected_content, (
        f"File '{path}' content does not match the expected initial state.\n"
        "---- Expected ----\n"
        f"{expected_content}\n"
        "---- Actual ----\n"
        f"{actual}\n"
        "------------------"
    )

    # Sanity: ensure the *new* keys are not already present
    assert "NEW_ACCESS_KEY_2023" not in actual, (
        f"File '{path}' should NOT yet contain the new access key."
    )
    assert "NEW_SECRET_KEY_2023" not in actual, (
        f"File '{path}' should NOT yet contain the new secret key."
    )


def test_rotation_log_does_not_exist_yet():
    assert not os.path.exists(LOG_PATH), (
        f"Log file '{LOG_PATH}' should NOT exist before the rotation task begins."
    )