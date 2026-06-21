# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is still in its pre-task “initial” state *before* the student carries
# out the TLS-credential rotation task described in the assignment.
#
# What we expect to be true right now:
#
# 1. The directory /home/user/.secrets exists.
# 2. Inside that directory:
#    • old_key.pem  – a regular file whose contents equal "OLD_KEY_PLACEHOLDER\n".
#    • new_key.pem  – a regular file whose contents equal "NEW_KEY_PLACEHOLDER\n".
#    • active_key.pem – a symbolic link that ultimately resolves (readlink -f)
#      to /home/user/.secrets/old_key.pem  (NOT to new_key.pem).
# 3. No file called /home/user/rotation.log should exist yet.
#
# If any of the checks below fail, the test output will clearly spell out what
# is missing or incorrect, helping the student understand what needs to be
# fixed *before* they begin their work.

import os
import stat
import pytest

HOME_DIR = "/home/user"
SECRETS_DIR = os.path.join(HOME_DIR, ".secrets")

OLD_KEY = os.path.join(SECRETS_DIR, "old_key.pem")
NEW_KEY = os.path.join(SECRETS_DIR, "new_key.pem")
ACTIVE_LINK = os.path.join(SECRETS_DIR, "active_key.pem")
ROTATION_LOG = os.path.join(HOME_DIR, "rotation.log")


def _assert_regular_file(path: str, msg_prefix: str = "") -> None:
    assert os.path.exists(path), f"{msg_prefix}Expected file {path!r} to exist."
    assert os.path.isfile(path), f"{msg_prefix}{path!r} exists but is not a regular file."


def _assert_symlink(path: str, msg_prefix: str = "") -> None:
    assert os.path.lexists(path), f"{msg_prefix}Expected symlink {path!r} to exist."
    assert os.path.islink(path), f"{msg_prefix}{path!r} exists but is not a symbolic link."


def test_secrets_directory_exists():
    assert os.path.isdir(SECRETS_DIR), (
        f"Required directory {SECRETS_DIR!r} is missing or not a directory."
    )


def test_key_files_and_contents():
    _assert_regular_file(OLD_KEY)
    _assert_regular_file(NEW_KEY)

    with open(OLD_KEY, "r", encoding="utf-8") as f:
        old_contents = f.read()
    with open(NEW_KEY, "r", encoding="utf-8") as f:
        new_contents = f.read()

    assert (
        old_contents == "OLD_KEY_PLACEHOLDER\n"
    ), f"Contents of {OLD_KEY!r} do not match expected placeholder text."
    assert (
        new_contents == "NEW_KEY_PLACEHOLDER\n"
    ), f"Contents of {NEW_KEY!r} do not match expected placeholder text."


def test_active_key_symlink_points_to_old_key():
    _assert_symlink(ACTIVE_LINK)

    # Resolve the symlink completely to its canonical absolute path.
    resolved = os.path.realpath(ACTIVE_LINK)
    assert resolved == OLD_KEY, (
        f"{ACTIVE_LINK!r} is expected to resolve to {OLD_KEY!r} "
        f"before rotation, but it currently resolves to {resolved!r}."
    )


def test_rotation_log_not_present_yet():
    assert not os.path.exists(
        ROTATION_LOG
    ), f"{ROTATION_LOG!r} should NOT exist before rotation starts."