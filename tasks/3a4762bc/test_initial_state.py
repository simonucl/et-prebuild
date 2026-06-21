# test_initial_state.py
#
# This pytest file verifies the **initial** state of the filesystem
# for the “backup-robot” exercise.  Nothing related to the robot’s new
# key-pair or log file should exist yet.  If any of the target artefacts
# are already present, the exercise would be meaningless, so we fail fast
# with an explicit message.

import os
import stat
import pytest

HOME = "/home/user"
SSH_DIR = os.path.join(HOME, ".ssh")

PRIV_KEY = os.path.join(SSH_DIR, "backup_ed25519")
PUB_KEY = os.path.join(SSH_DIR, "backup_ed25519.pub")
AUTH_KEYS = os.path.join(SSH_DIR, "authorized_keys")
LOG_FILE = os.path.join(HOME, "ssh_setup.log")


def _exists(path):
    """Return True iff *path* exists in the filesystem."""
    return os.path.exists(path)


def _mode(path):
    """Return the file mode bits (e.g. 0o700)."""
    return stat.S_IMODE(os.lstat(path).st_mode)


@pytest.mark.parametrize(
    "path,what",
    [
        (PRIV_KEY,  "private key"),
        (PUB_KEY,   "public key"),
        (AUTH_KEYS, "authorized_keys file"),
        (LOG_FILE,  "log file"),
    ],
)
def test_target_files_do_not_exist_yet(path, what):
    """
    None of the artefacts that the student has to create should already
    be present.  If they are, the initial state is invalid.
    """
    assert not _exists(path), f"The {what} at {path!r} already exists."


def test_ssh_directory_clean():
    """
    The .ssh directory may or may not exist at this point.  If it *does*
    exist, make sure it does NOT already contain the files that the
    student is supposed to create.  We do **not** enforce permissions
    here; permission checks belong to the final-state tests.
    """
    if not _exists(SSH_DIR):
        pytest.skip(f"{SSH_DIR!r} does not exist yet – that is fine.")
    else:
        # The directory exists; ensure it does not already contain our
        # target files.
        unexpected = [p for p in (PRIV_KEY, PUB_KEY, AUTH_KEYS) if _exists(p)]
        assert not unexpected, (
            "The following files should NOT exist before the exercise starts: "
            + ", ".join(unexpected)
        )