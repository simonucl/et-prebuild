# test_initial_state.py
#
# This pytest file validates the *initial* operating-system / filesystem
# state **before** the student starts the “credential-rotation” task.
#
# Expected initial facts (taken from the task description):
#   1. Directory  : /home/user/credentials          must exist.
#   2. File       : /home/user/credentials/app_secrets_2023-09-15.txt
#                  must exist and be readable.
#
# Everything else mentioned in the “Target end state” MUST **NOT** yet exist.
# If any artefact from the final state is already present, the test should
# fail and clearly indicate what is wrong.
#
# Only stdlib + pytest are used.

import os
import stat
import pytest
from pathlib import Path

CRED_DIR = Path("/home/user/credentials")
OLD_SECRET = CRED_DIR / "app_secrets_2023-09-15.txt"

# Paths that must *not* exist yet
ARCHIVE_DIR          = CRED_DIR / "archive"
OLD_SECRET_BAK       = ARCHIVE_DIR / "app_secrets_2023-09-15.txt.bak"
OLD_SECRET_BAK_TGZ   = ARCHIVE_DIR / "app_secrets_2023-09-15.txt.bak.tar.gz"
NEW_SECRET           = CRED_DIR / "app_secrets_2023-10-01.txt"
ROTATION_HISTORY_LOG = CRED_DIR / "rotation_history.log"


def _assert_path_abs(path: Path) -> None:
    """
    Helper to ensure we never test relative paths by mistake.
    """
    assert path.is_absolute(), f"BUG in test: {path} is not an absolute path."


def test_credentials_directory_exists():
    _assert_path_abs(CRED_DIR)
    assert CRED_DIR.exists(), (
        "Required directory '/home/user/credentials' does not exist. "
        "Create it before proceeding with the rotation."
    )
    assert CRED_DIR.is_dir(), (
        f"'/home/user/credentials' exists but is not a directory "
        f"(found type: {CRED_DIR.stat().st_mode:o})."
    )


def test_old_secret_file_exists_and_readable():
    _assert_path_abs(OLD_SECRET)
    assert OLD_SECRET.exists(), (
        "The original credential file "
        "'/home/user/credentials/app_secrets_2023-09-15.txt' is missing."
    )
    assert OLD_SECRET.is_file(), (
        "'/home/user/credentials/app_secrets_2023-09-15.txt' exists but is "
        "not a regular file."
    )
    # Try opening the file to confirm readability
    try:
        with OLD_SECRET.open("r") as fp:
            fp.read(1)  # read a single byte; content itself is irrelevant
    except Exception as exc:  # noqa: BLE001
        pytest.fail(
            "The original credential file exists but is not readable "
            f"by the current user: {exc}"
        )


@pytest.mark.parametrize(
    "path",
    [
        ARCHIVE_DIR,
        OLD_SECRET_BAK,
        OLD_SECRET_BAK_TGZ,
        NEW_SECRET,
        ROTATION_HISTORY_LOG,
    ],
)
def test_rotation_outputs_do_not_exist_yet(path: Path):
    _assert_path_abs(path)
    assert not path.exists(), (
        "Found artefact that should NOT exist before rotation: "
        f"'{path}'.\n"
        "Make sure you start from the pristine initial state. "
        "Remove this file/directory before performing the rotation steps."
    )