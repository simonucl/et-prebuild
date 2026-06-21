# test_initial_state.py
#
# This test-suite verifies that the machine starts from the exact, known
# filesystem state required by the assignment *before* the student performs
# any action.  If any test here fails, the environment is not correctly
# provisioned and the student will be unable to complete the task as
# described.

import os
import stat
import pytest

HOME = "/home/user"
CRED_DIR = os.path.join(HOME, "credentials")

OLD_KEY = os.path.join(CRED_DIR, "api_key_2023.pem")
NEW_KEY = os.path.join(CRED_DIR, "api_key_2024.pem")
CUR_LINK = os.path.join(CRED_DIR, "api_key_current.pem")
ROTATION_LOG = os.path.join(CRED_DIR, "rotation.log")


def _assert_is_regular_file(path: str) -> None:
    """Fail the test if path is not an existing regular file (not a symlink)."""
    assert os.path.exists(path), f"Expected file '{path}' is missing."
    assert not os.path.islink(path), f"'{path}' must be a regular file, but it is a symlink."
    st_mode = os.stat(path).st_mode
    assert stat.S_ISREG(st_mode), f"'{path}' exists but is not a regular file."
    # We purposefully do not assert permissions; only presence and type matter.


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def test_credentials_directory_exists():
    assert os.path.isdir(CRED_DIR), (
        f"Credentials directory '{CRED_DIR}' is missing or not a directory."
    )


def test_old_and_new_key_files_exist_and_have_expected_content():
    # Old key
    _assert_is_regular_file(OLD_KEY)
    content_old = _read_file(OLD_KEY)
    assert content_old == "OLD KEY 2023\n", (
        f"Unexpected contents in '{OLD_KEY}'. Expected exactly 'OLD KEY 2023\\n'."
    )

    # New key
    _assert_is_regular_file(NEW_KEY)
    content_new = _read_file(NEW_KEY)
    assert content_new == "NEW KEY 2024\n", (
        f"Unexpected contents in '{NEW_KEY}'. Expected exactly 'NEW KEY 2024\\n'."
    )


def test_current_symlink_points_to_old_key():
    assert os.path.islink(CUR_LINK), (
        f"Expected symlink '{CUR_LINK}' is missing or not a symlink."
    )
    target = os.readlink(CUR_LINK)
    expected_target = OLD_KEY
    assert target == expected_target, (
        f"Symlink '{CUR_LINK}' should point to '{expected_target}', "
        f"but currently points to '{target}'."
    )


def test_rotation_log_does_not_exist_yet():
    assert not os.path.exists(ROTATION_LOG), (
        f"'{ROTATION_LOG}' should NOT exist before rotation, but it does."
    )