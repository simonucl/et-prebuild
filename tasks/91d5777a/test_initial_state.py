# test_initial_state.py
#
# This pytest suite validates that the machine is in the *initial* (pre-task)
# state expected by the “SSH-key-as-code” exercise.  In short, the artefacts
# the student is supposed to create *must not already exist*; otherwise the
# environment would be contaminated and the learning objective defeated.
#
# NOTE: These tests run *before* the student performs any action.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SSH_DIR = HOME / ".ssh"
PRIV_KEY = SSH_DIR / "devsecops_policy_ed25519"
PUB_KEY = SSH_DIR / "devsecops_policy_ed25519.pub"
AUTH_KEYS = SSH_DIR / "authorized_keys"
COMPLIANCE_JSON = HOME / "devsecops/compliance/ssh_key_report.json"
LOG_FILE = HOME / "ssh_key_task.log"


@pytest.mark.describe("Pre-task filesystem sanity")
class TestInitialState:
    def test_home_directory_exists(self):
        assert HOME.is_dir(), f"Expected {HOME} to exist. The base user directory is missing."

    def test_private_key_absent(self):
        assert not PRIV_KEY.exists(), (
            f"Pre-condition failure: {PRIV_KEY} already exists. "
            "The student must generate this key during the task."
        )

    def test_public_key_absent(self):
        assert not PUB_KEY.exists(), (
            f"Pre-condition failure: {PUB_KEY} already exists. "
            "The student must generate this key during the task."
        )

    def test_compliance_report_absent(self):
        assert not COMPLIANCE_JSON.exists(), (
            f"Pre-condition failure: {COMPLIANCE_JSON} already exists. "
            "The student must create this compliance artefact."
        )

    def test_execution_log_absent(self):
        assert not LOG_FILE.exists(), (
            f"Pre-condition failure: {LOG_FILE} already exists. "
            "The student must produce this log as part of the task."
        )

    def test_authorized_keys_clean_or_absent(self):
        """
        The file may legitimately not exist yet.  If it *does* exist, ensure it
        does not already contain a line whose trailing comment is
        'policy-enforced', which would indicate someone has already performed
        (part of) the task.
        """
        if not AUTH_KEYS.exists():
            pytest.skip(f"{AUTH_KEYS} does not exist yet; nothing to validate.")
        else:
            with AUTH_KEYS.open("r", encoding="utf-8") as fh:
                for lineno, line in enumerate(fh, start=1):
                    if line.strip().endswith("policy-enforced"):
                        pytest.fail(
                            f"Pre-condition failure: {AUTH_KEYS} line {lineno} "
                            "already contains a key with comment 'policy-enforced'."
                        )