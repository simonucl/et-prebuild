# test_initial_state.py
#
# Pytest suite that validates the INITIAL operating-system / filesystem state
# before the student performs any actions for the “time-zone & locale” task.
#
# The tests assert that:
#   • The required user directories (/home/user/charlie, /home/user/diana)
#     and their individual ~/.bashrc files already exist and are writable.
#   • The administrative directory /home/user/site_admin exists and is writable.
#   • The required export lines for TZ and LANG are NOT YET present in either
#     user’s ~/.bashrc (the student will add them).
#   • The summary log
#       /home/user/site_admin/time_locale_summary.log
#     does NOT yet exist (the student will create it).
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

HOME = "/home/user"

USERS = {
    "charlie": {
        "tz": 'Asia/Kolkata',
        "lang": 'en_IN.UTF-8',
    },
    "diana": {
        "tz": 'America/Los_Angeles',
        "lang": 'en_US.UTF-8',
    },
}

SITE_ADMIN_DIR = os.path.join(HOME, "site_admin")
SUMMARY_LOG = os.path.join(SITE_ADMIN_DIR, "time_locale_summary.log")


def _is_writable(path: str) -> bool:
    """Return True if current process can write to `path`."""
    return os.access(path, os.W_OK)


@pytest.mark.parametrize("user", USERS.keys())
def test_user_directory_exists_and_writable(user):
    """
    Verify that each user directory exists, is a directory,
    and is writable by the current user (non-privileged).
    """
    user_dir = os.path.join(HOME, user)
    assert os.path.isdir(user_dir), (
        f"Expected user directory {user_dir!r} to exist and be a directory."
    )
    assert _is_writable(user_dir), (
        f"User directory {user_dir!r} exists but is not writable—"
        "you will need write access to modify ~/.bashrc."
    )


@pytest.mark.parametrize("user", USERS.keys())
def test_bashrc_exists_and_writable(user):
    """
    Confirm that ~/.bashrc exists for each user and is writable.
    """
    bashrc = os.path.join(HOME, user, ".bashrc")
    assert os.path.isfile(bashrc), (
        f"Expected file {bashrc!r} to exist for user {user!r}."
    )

    # Ensure file is writable.  On most systems, file write permission
    # implies directory write permission; nevertheless we check explicitly.
    assert _is_writable(bashrc), (
        f"File {bashrc!r} exists but is not writable—"
        "you need to be able to edit this file."
    )


@pytest.mark.parametrize("user,vals", USERS.items())
def test_bashrc_does_not_yet_contain_target_exports(user, vals):
    """
    The two exact export lines that the student will add/modify
    must NOT be present yet.
    """
    bashrc = os.path.join(HOME, user, ".bashrc")
    with open(bashrc, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read().splitlines()

    tz_line   = f'export TZ="{vals["tz"]}"'
    lang_line = f'export LANG="{vals["lang"]}"'

    # Neither line should be present before the student acts.
    assert tz_line not in content, (
        f"The line {tz_line!r} is already present in {bashrc!r}. "
        "It should be added only by the student."
    )
    assert lang_line not in content, (
        f"The line {lang_line!r} is already present in {bashrc!r}. "
        "It should be added only by the student."
    )


def test_site_admin_directory_exists_and_writable():
    """
    Ensure /home/user/site_admin exists and is writable.
    """
    assert os.path.isdir(SITE_ADMIN_DIR), (
        f"Expected directory {SITE_ADMIN_DIR!r} to exist."
    )
    assert _is_writable(SITE_ADMIN_DIR), (
        f"Directory {SITE_ADMIN_DIR!r} exists but is not writable."
    )


def test_summary_log_not_present_initially():
    """
    The summary log should NOT exist before the student creates it.
    """
    assert not os.path.exists(SUMMARY_LOG), (
        f"{SUMMARY_LOG!r} already exists. The student should create it."
    )