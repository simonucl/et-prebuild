# test_initial_state.py
#
# Pytest suite that validates the pre-existing operating-system/ filesystem
# state before the student begins any work on the rotation task.

import os
import stat
import pytest

SECURE_API_DIR = "/home/user/secure_api"
TOKEN_FILE = "/home/user/secure_api/token.json"
EXPECTED_TOKEN_CONTENT = b'{"new_token":"xyz789","expires_in":3600}'
DIR_PERMS_EXPECTED = 0o755
FILE_PERMS_EXPECTED = 0o644


def _get_perm_bits(path):
    """
    Return the permission bits (e.g. 0o755) of the given path.
    """
    return stat.S_IMODE(os.stat(path).st_mode)


@pytest.mark.describe("Pre-existing credential directory is present and correct")
def test_secure_api_directory_exists_and_has_correct_permissions():
    # Directory exists?
    assert os.path.isdir(SECURE_API_DIR), (
        f"Required directory {SECURE_API_DIR!s} is missing."
    )

    # Permissions?
    actual_perms = _get_perm_bits(SECURE_API_DIR)
    assert actual_perms == DIR_PERMS_EXPECTED, (
        f"Directory {SECURE_API_DIR!s} should have permissions "
        f"{oct(DIR_PERMS_EXPECTED)}, but has {oct(actual_perms)}."
    )


@pytest.mark.describe("Pre-existing token file is present and correct")
def test_token_file_exists_has_correct_permissions_and_content():
    # File exists?
    assert os.path.isfile(TOKEN_FILE), (
        f"Required file {TOKEN_FILE!s} is missing."
    )

    # Permissions?
    actual_perms = _get_perm_bits(TOKEN_FILE)
    assert actual_perms == FILE_PERMS_EXPECTED, (
        f"File {TOKEN_FILE!s} should have permissions "
        f"{oct(FILE_PERMS_EXPECTED)}, but has {oct(actual_perms)}."
    )

    # Content?
    with open(TOKEN_FILE, "rb") as fp:
        content = fp.read()

    assert content == EXPECTED_TOKEN_CONTENT, (
        f"Content of {TOKEN_FILE!s} is not as expected.\n"
        f"Expected: {EXPECTED_TOKEN_CONTENT!r}\n"
        f"Found   : {content!r}"
    )