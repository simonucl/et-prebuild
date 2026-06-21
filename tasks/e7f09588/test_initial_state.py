# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating system
# *before* the learner carries out the SSH-key / log-file setup task.
#
# The checks ensure that no artefacts from the upcoming activity are
# already present.  If any of these tests fail, it means the starting
# environment is not clean and predictable.

import os
import stat
import pytest

HOME = "/home/user"
SSH_DIR = os.path.join(HOME, ".ssh")
PRIVATE_KEY = os.path.join(SSH_DIR, "dataset_ed25519")
PUBLIC_KEY = PRIVATE_KEY + ".pub"
AUTH_KEYS = os.path.join(SSH_DIR, "authorized_keys")
LOG_FILE = os.path.join(HOME, "ssh_setup.log")
COMMENT = "researcher_dataset_access"


def _human_permissions(mode: int) -> str:
    """Return a human-readable octal permission string, e.g. '0o600'."""
    return oct(stat.S_IMODE(mode))


@pytest.fixture(scope="module")
def auth_keys_contents():
    """
    Read the authorised_keys file once (if it exists) so that repeated
    tests don't have to open it multiple times.
    """
    if os.path.exists(AUTH_KEYS):
        with open(AUTH_KEYS, "r", encoding="utf-8") as fh:
            return fh.read()
    return ""


def test_private_key_absent():
    assert not os.path.exists(
        PRIVATE_KEY
    ), (
        f"Found unexpected file {PRIVATE_KEY!r}. "
        "The private key should not exist before the task begins."
    )


def test_public_key_absent():
    assert not os.path.exists(
        PUBLIC_KEY
    ), (
        f"Found unexpected file {PUBLIC_KEY!r}. "
        "The public key should not exist before the task begins."
    )


def test_log_file_absent():
    assert not os.path.exists(
        LOG_FILE
    ), (
        f"Found unexpected log file {LOG_FILE!r}. "
        "The log file should not exist before the task begins."
    )


def test_authorized_keys_does_not_contain_comment(auth_keys_contents):
    if not auth_keys_contents:
        # No authorized_keys file present — perfectly fine at this stage.
        pytest.skip("authorized_keys does not exist yet; skipping content checks.")

    occurrences = auth_keys_contents.count(COMMENT)
    assert occurrences == 0, (
        f"The string {COMMENT!r} already appears in {AUTH_KEYS} "
        f"({occurrences} times). The comment must be added exactly once "
        "only after the learner completes the task."
    )