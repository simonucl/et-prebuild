# test_initial_state.py
#
# This pytest suite verifies that the machine is in a **clean, pre-task**
# condition before the student starts working on the “micro-service SSH key”
# exercise.  Nothing the grader will later look for (keys, hand-off directory,
# audit log) should exist yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")

# --- paths the final grader will inspect -------------------------------
SSH_DIR                = HOME / ".ssh"
PRIV_KEY               = SSH_DIR / "microservice_rsa"
PUB_KEY                = SSH_DIR / "microservice_rsa.pub"
MICRO_KEYS_DIR         = HOME / "micro_keys"
AUTHORIZED_KEYS_MICRO  = MICRO_KEYS_DIR / "authorized_keys_micro"
AUDIT_LOG              = HOME / "ssh_setup.log"
# -----------------------------------------------------------------------


@pytest.mark.parametrize(
    "path,desc",
    [
        (PRIV_KEY,              "private key"),
        (PUB_KEY,               "public key"),
        (AUTHORIZED_KEYS_MICRO, "authorized-keys hand-off file"),
        (AUDIT_LOG,             "audit log"),
    ],
)
def test_object_must_not_exist_yet(path: Path, desc: str):
    """
    Before the student performs any action **none** of the artefacts that the
    final grader expects should already be present.

    If any of these files exist the exercise would be in an undefined state
    and could mask student mistakes, hence we fail early with a clear message.
    """
    assert not path.exists(), (
        f"The {desc} ({path}) already exists. "
        "The environment must be clean before the student starts."
    )


def test_micro_keys_dir_is_clean():
    """
    The directory /home/user/micro_keys should not exist at all, but if it
    already exists for some unforeseen reason it must at least be empty so that
    the student does not accidentally append or overwrite files.
    """
    if MICRO_KEYS_DIR.exists():
        assert MICRO_KEYS_DIR.is_dir(), (
            f"{MICRO_KEYS_DIR} exists but is not a directory."
        )
        # Only allow an empty directory; any content is suspicious.
        contents = list(MICRO_KEYS_DIR.iterdir())
        assert not contents, (
            f"{MICRO_KEYS_DIR} is expected to be empty before the exercise "
            f"starts, but contains: {[p.name for p in contents]}"
        )


def test_ssh_dir_does_not_conflict():
    """
    The presence (or absence) of ~/.ssh itself is not important, but if it
    exists there must be no files whose names would collide with what the
    student is about to create.
    """
    if SSH_DIR.exists():
        assert SSH_DIR.is_dir(), f"{SSH_DIR} exists but is not a directory."
        for collision in (PRIV_KEY, PUB_KEY):
            assert not collision.exists(), (
                f"Found unexpected pre-existing file {collision}. "
                "Start with a clean ~/.ssh or remove/rename this file."
            )