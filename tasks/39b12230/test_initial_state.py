# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the operating system / filesystem
_before_ the student carries out the “Grafana SSH key-pair” exercise.

If any of these tests fail, it means the student (or some other process)
has already created one or more artefacts that are supposed to be produced
only *after* the exercise is completed.

Do NOT modify these tests.
"""

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
PRIV_KEY = SSH_DIR / "grafana_sync_rsa"
PUB_KEY = SSH_DIR / "grafana_sync_rsa.pub"
SSH_CONFIG = SSH_DIR / "config"

SETUP_DIR = HOME / "ssh_setup"
JSON_LOG = SETUP_DIR / "grafana_sync_key_log.json"
README = SETUP_DIR / "README_keysetup.txt"

STANZA_FIRST_LINE = "Host grafana-prod"


@pytest.mark.parametrize("path_to_check", [PRIV_KEY, PUB_KEY, JSON_LOG, README])
def test_key_and_log_files_do_not_exist_yet(path_to_check):
    """
    None of the files that the student is supposed to create should exist yet.
    """
    assert not path_to_check.exists(), (
        f"{path_to_check} already exists, but no work should have been done yet."
    )


def test_setup_directory_absent_or_empty():
    """
    The /home/user/ssh_setup directory should not exist yet.
    If it does exist for some reason, it must be completely empty so that
    the student starts from a clean slate.
    """
    if SETUP_DIR.exists():
        contents = list(SETUP_DIR.iterdir())
        assert not contents, (
            f"{SETUP_DIR} already exists and is not empty: {contents}. "
            "The setup directory must be created by the student."
        )


def test_private_and_public_key_absent():
    """
    Both key files must be absent at the outset.
    """
    assert not PRIV_KEY.exists(), f"Private key {PRIV_KEY} already exists."
    assert not PUB_KEY.exists(), f"Public key {PUB_KEY} already exists."


def test_ssh_config_has_no_grafana_prod_stanza():
    """
    If ~/.ssh/config exists, it must NOT already contain a stanza that starts
    with 'Host grafana-prod'.  The student will append it later.
    """
    if SSH_CONFIG.exists():
        try:
            config_text = SSH_CONFIG.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"Could not read {SSH_CONFIG}: {exc}")

        # Fast negative check: the specific first line of the stanza
        assert STANZA_FIRST_LINE not in config_text, (
            f"{SSH_CONFIG} already contains a 'Host grafana-prod' stanza, "
            "but none should be present before the exercise starts."
        )