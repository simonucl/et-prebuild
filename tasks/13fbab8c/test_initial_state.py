# test_initial_state.py
#
# This pytest suite validates the **initial** state of the developer
# container *before* the student has carried out any of the required
# provisioning steps.  If any of the assertions in this file fail,
# the container is **not clean** and will likely cause the real
# grading tests (run *after* the student’s actions) to behave
# unpredictably.

import os
from pathlib import Path

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
LOG_DIR = HOME / "logs"

PRIVATE_KEY = SSH_DIR / "id_microservice_ed25519"
PUBLIC_KEY = SSH_DIR / "id_microservice_ed25519.pub"
AUTHORIZED_KEYS = SSH_DIR / "authorized_keys"
LOG_FILE = LOG_DIR / "ssh_setup.log"


def _fmt(path: Path) -> str:
    """Nicely format a Path for assertion messages."""
    return str(path)


def test_private_key_absent():
    """
    The dedicated private key must NOT exist yet.  If it does, the
    container isn’t fresh or somebody already ran the provisioning
    script, which violates the required workflow.
    """
    assert not PRIVATE_KEY.exists(), (
        f"Pre-existing private key found at {_fmt(PRIVATE_KEY)} — "
        "the environment must start without this file."
    )


def test_public_key_absent():
    """
    The dedicated public key must NOT exist yet for the same reasons
    given for the private key above.
    """
    assert not PUBLIC_KEY.exists(), (
        f"Pre-existing public key found at {_fmt(PUBLIC_KEY)} — "
        "the environment must start without this file."
    )


def test_log_file_absent():
    """
    The log file that the student is expected to create must be absent.
    A pre-existing log would make it impossible to verify whether the
    student’s script actually performed the work.
    """
    assert not LOG_FILE.exists(), (
        f"Pre-existing log file found at {_fmt(LOG_FILE)} — "
        "the container must not contain this file yet."
    )


def test_no_leftover_microservice_keys_anywhere():
    """
    Make sure there are no *other* files that look like left-overs of a
    previous run.  Anything named id_microservice_ed25519* anywhere in
    the user’s .ssh directory is disallowed at this stage.
    """
    if not SSH_DIR.exists():
        # Directory absent → certainly no offending files.
        return

    offenders = [
        p for p in SSH_DIR.iterdir()
        if p.name.startswith("id_microservice_ed25519")
    ]
    assert not offenders, (
        "Unexpected files found in ~/.ssh before setup:\n"
        + "\n".join(map(_fmt, offenders))
        + "\nPlease start from a clean container."
    )


def test_authorized_keys_not_already_contains_the_key():
    """
    If ~/.ssh/authorized_keys exists, verify that it **does not already
    contain** a key with comment 'micro@containers'.  The student will
    have to append it later; seeing it now would indicate prior work.
    """
    if not AUTHORIZED_KEYS.exists():
        return

    with AUTHORIZED_KEYS.open("r", encoding="utf-8") as fh:
        for line_num, line in enumerate(fh, start=1):
            if line.strip().endswith(" micro@containers"):
                assert False, (
                    f"Line {line_num} of {_fmt(AUTHORIZED_KEYS)} already "
                    "contains a key with comment 'micro@containers'.  "
                    "This should only appear **after** the student runs "
                    "the provisioning steps."
                )