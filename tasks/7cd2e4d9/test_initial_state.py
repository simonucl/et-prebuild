# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem is in the
# *pristine* state expected *before* the student carries out the assignment.
#
# We intentionally check for the ABSENCE of the files that the student is
# supposed to create as well as the absence of the specific public-key entry
# in ~/.ssh/authorized_keys.  Any pre-existing artefact would indicate that
# the environment is contaminated and would invalidate the exercise.
#
# NOTE:  All paths are fully-qualified as required.
#
# Only the Python stdlib and pytest are used.

import subprocess
from pathlib import Path
import re
import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"

PRIV_KEY = SSH_DIR / "id_ed25519_loganalyst"
PUB_KEY = SSH_DIR / "id_ed25519_loganalyst.pub"
AUTHORIZED_KEYS = SSH_DIR / "authorized_keys"

AUDIT_DIR = HOME / "ssh_setup"
AUDIT_LOG = AUDIT_DIR / "ssh_key_setup.log"

PUBLIC_KEY_COMMENT = "log_analyst@localhost"


@pytest.fixture(scope="session")
def authorized_keys_contents():
    """
    Return the decoded text of ~/.ssh/authorized_keys if it exists,
    otherwise return an empty string.
    """
    if AUTHORIZED_KEYS.exists():
        try:
            return AUTHORIZED_KEYS.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            pytest.fail(
                f"Unable to read {AUTHORIZED_KEYS} even though it exists: {exc}"
            )
    return ""


def test_private_key_does_not_exist():
    assert not PRIV_KEY.exists(), (
        f"The private key {PRIV_KEY} already exists. "
        "The assignment requires the student to generate it."
    )


def test_public_key_does_not_exist():
    assert not PUB_KEY.exists(), (
        f"The public key {PUB_KEY} already exists. "
        "The assignment requires the student to generate it."
    )


def test_audit_dir_and_log_do_not_exist_yet():
    if AUDIT_DIR.exists():
        # Directory might legitimately exist from a previous exercise; only the
        # audit log file must be absent.
        assert not AUDIT_LOG.exists(), (
            f"The audit log {AUDIT_LOG} already exists. "
            "The student must create it as part of the current exercise."
        )
    else:
        assert not AUDIT_LOG.exists(), (
            f"The audit log {AUDIT_LOG} exists without its parent directory. "
            "Environment is inconsistent."
        )


def test_authorized_keys_does_not_contain_new_key(authorized_keys_contents):
    """
    Even if authorized_keys exists, it must NOT already contain a line that
    ends with the required comment or specifically matches the to-be-created
    public key.
    """
    if not authorized_keys_contents:
        pytest.skip(f"{AUTHORIZED_KEYS} does not exist yet; key certainly absent.")

    # Match lines that contain the comment exactly; avoid false positives.
    pattern = re.compile(rf"^\s*ssh-ed25519\s+[A-Za-z0-9+/=]+\s+{PUBLIC_KEY_COMMENT}\s*$")
    offending_lines = [
        ln for ln in authorized_keys_contents.splitlines() if pattern.match(ln)
    ]
    assert (
        len(offending_lines) == 0
    ), (
        f"{AUTHORIZED_KEYS} already contains the public key meant for this task:\n"
        f"{offending_lines}\n"
        "The student must append this key during the exercise, "
        "so it should not be present beforehand."
    )