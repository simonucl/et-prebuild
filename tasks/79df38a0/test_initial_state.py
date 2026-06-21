# test_initial_state.py
#
# Pytest checks that the machine is in the expected **initial** state
# BEFORE the student carries out any instructions.  If any of these
# assertions fail, the environment is not suitable for the task.

import os
import stat
import pwd
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME                 = "/home/user"
SSH_DIR              = os.path.join(HOME, ".ssh")
PRIV_KEY             = os.path.join(SSH_DIR, "engineer_deploy_ed25519")
PUB_KEY              = PRIV_KEY + ".pub"
AUTHORIZED_KEYS      = os.path.join(SSH_DIR, "authorized_keys")
DEPLOY_DIR           = os.path.join(HOME, "deploy")
DEPLOY_LOG           = os.path.join(DEPLOY_DIR, "ssh_key_rollout.log")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _is_writable_by_user(path: str) -> bool:
    """
    Return True if the current effective UID has write permission on *path*.
    """
    return os.access(path, os.W_OK)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_home_directory_exists():
    assert os.path.isdir(HOME), f"Expected directory {HOME!r} to exist."

def test_ssh_directory_exists_and_writable():
    assert os.path.isdir(SSH_DIR), (
        f"Expected directory {SSH_DIR!r} to exist; it is required for key storage."
    )
    assert _is_writable_by_user(SSH_DIR), (
        f"Directory {SSH_DIR!r} must be writable by the current user so that new keys "
        f"can be created there."
    )

@pytest.mark.parametrize(
    "path,desc",
    [
        (PRIV_KEY, "private key"),
        (PUB_KEY, "public key"),
        (DEPLOY_LOG, "deployment log file"),
    ],
)
def test_key_and_log_files_do_not_yet_exist(path, desc):
    assert not os.path.exists(path), (
        f"The {desc} {path!r} already exists, but it should NOT be present before "
        f"the task is performed."
    )

def test_authorized_keys_state():
    """
    If ~/.ssh/authorized_keys already exists, it must NOT yet contain a key
    with the comment 'deploy-key'.  The student task is expected to add such a
    key as the *last* (or only) line.
    """
    if not os.path.exists(AUTHORIZED_KEYS):
        pytest.skip(f"{AUTHORIZED_KEYS!r} does not exist yet – that is acceptable.")
    try:
        with open(AUTHORIZED_KEYS, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except UnicodeDecodeError:
        pytest.fail(
            f"File {AUTHORIZED_KEYS!r} exists but could not be decoded as UTF-8."
        )

    offending_lines = [
        ln.rstrip("\n") for ln in lines if ln.rstrip("\n").endswith(" deploy-key")
    ]
    assert not offending_lines, (
        f"The following line(s) in {AUTHORIZED_KEYS!r} already contain the comment "
        f"'deploy-key', but the student has not performed the task yet:\n"
        + "\n".join(offending_lines)
    )

def test_deploy_directory_optional_but_not_required_yet():
    """
    The /home/user/deploy directory is expected *after* task completion,
    but its absence beforehand is perfectly fine.  If it does exist already,
    ensure it is a directory and writable so the log file can be appended.
    """
    if not os.path.exists(DEPLOY_DIR):
        pytest.skip(f"{DEPLOY_DIR!r} does not exist yet – that is acceptable.")
    assert os.path.isdir(DEPLOY_DIR), f"{DEPLOY_DIR!r} exists but is not a directory."
    assert _is_writable_by_user(DEPLOY_DIR), (
        f"Directory {DEPLOY_DIR!r} must be writable so the log file can be created."
    )