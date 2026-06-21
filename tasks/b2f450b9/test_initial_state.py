# test_initial_state.py
"""
Pytest suite to validate the initial filesystem state *before* the student
performs any actions for the “portable, non-privileged firewall utility bundle”.

EXPECTED INITIAL CONDITIONS
------------------------------------------------------------
1. The directory /home/user/scripts must NOT yet exist.
2. Consequently, the files
     /home/user/scripts/firewall_rules.v4    and
     /home/user/scripts/firewall_rules_creation.log
   must also NOT exist.

If any of these artefacts are already present, the environment is not in the
required pristine state and the tests will fail with an informative message.
"""
from pathlib import Path
import pytest


SCRIPTS_DIR = Path("/home/user/scripts")
RULES_FILE = SCRIPTS_DIR / "firewall_rules.v4"
LOG_FILE = SCRIPTS_DIR / "firewall_rules_creation.log"


def _format_exists(path: Path, exists: bool) -> str:
    """Helper to format existence in messages."""
    return f"{'exists' if exists else 'does NOT exist'} (path: {path})"


def test_scripts_directory_absent():
    """
    The /home/user/scripts directory must NOT exist before the task begins.
    """
    exists = SCRIPTS_DIR.exists()
    assert not exists, (
        "Pre-condition failed: /home/user/scripts should not exist at the start. "
        f"Currently it {_format_exists(SCRIPTS_DIR, exists)}."
    )


@pytest.mark.parametrize("file_path", [RULES_FILE, LOG_FILE])
def test_firewall_files_absent(file_path: Path):
    """
    Neither firewall_rules.v4 nor firewall_rules_creation.log should be present
    before the student creates them.
    """
    exists = file_path.exists()
    assert not exists, (
        "Pre-condition failed: No deliverable files should exist at the start. "
        f"{file_path} {_format_exists(file_path, exists)}."
    )