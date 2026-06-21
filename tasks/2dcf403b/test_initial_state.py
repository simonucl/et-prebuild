# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the OS / filesystem
_before_ the learner executes any commands for the “artifact-manager” task.

Truth we are checking against (before the student’s action):
1. The student’s home directory (/home/user) must already exist.
2. The configuration file that the student is going to create,
   /home/user/repo_manager/env.conf, must **not** exist yet.
3. The directory /home/user/repo_manager may or may not exist, but if it
   does it should be a directory (not a file) and must not yet contain
   env.conf.

If any of these conditions are not met, the tests will fail with clear
messages so the student (or course author) can fix the base image before
proceeding.
"""

import os
import stat
import pwd
import pytest

HOME = "/home/user"
REPO_DIR = "/home/user/repo_manager"
ENV_CONF = "/home/user/repo_manager/env.conf"


def _get_username() -> str:
    """Return the current user’s login name."""
    return pwd.getpwuid(os.geteuid()).pw_name


def test_home_directory_exists_and_is_directory():
    """Verify that /home/user exists and is a directory."""
    assert os.path.exists(HOME), (
        f"Expected base home directory {HOME!r} to exist before the exercise "
        "begins, but it does not."
    )
    assert os.path.isdir(HOME), (
        f"{HOME!r} exists but is not a directory; fix the base image."
    )


def test_env_conf_does_not_exist_yet():
    """The configuration file must not be present prior to the exercise."""
    assert not os.path.exists(
        ENV_CONF
    ), (
        f"The file {ENV_CONF!r} already exists, but the exercise requires the "
        "student to create it. Remove this file from the base image."
    )


def test_repo_manager_path_is_ok_to_create():
    """
    If /home/user/repo_manager exists already, it must be a directory that the
    current user owns so the student can safely write into it. If it doesn’t
    exist, that is also fine (the student will create it).
    """
    if not os.path.exists(REPO_DIR):
        pytest.skip(f"{REPO_DIR!r} does not yet exist — this is acceptable.")
        return

    # It exists: ensure it is a directory
    assert os.path.isdir(REPO_DIR), (
        f"{REPO_DIR!r} exists but is not a directory. Remove it or change it "
        "to a directory so the student can use it."
    )

    # Ensure current user owns it and can write into it
    dir_stat = os.stat(REPO_DIR)
    current_uid = os.geteuid()
    assert (
        dir_stat.st_uid == current_uid
    ), (
        f"{REPO_DIR!r} is not owned by the current user "
        f"{_get_username()!r}; please fix ownership so the student can write."
    )

    # The target config file must still not exist
    assert not os.path.exists(
        ENV_CONF
    ), (
        f"{ENV_CONF!r} should not exist yet, but it is already present. "
        "Remove this file from the base image."
    )


def test_env_conf_filename_not_shadowed_by_nonregular_file():
    """
    Guard against rare cases where something (symlink, directory, pipe, etc.)
    named env.conf might pre-exist. It must either not exist at all or, if it
    does, the earlier test would already have failed.
    """
    if not os.path.exists(ENV_CONF):
        return

    # If we are here, test_env_conf_does_not_exist_yet has failed, but we add
    # extra clarity on *why*.
    st_mode = os.lstat(ENV_CONF).st_mode
    assert stat.S_ISREG(st_mode), (
        f"{ENV_CONF!r} exists and is not a regular file "
        f"(mode: {oct(st_mode)}). Remove it so the student can create the "
        "expected regular file."
    )