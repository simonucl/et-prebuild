# test_initial_state.py
"""
Pre-exercise validation for the “policy-as-code” assignment.

These tests assert that the system is still in its original, untouched state
BEFORE the learner creates the virtual environment under
/home/user/security_scan.

If any of these tests fail, the workspace is **not** clean and the learner
would start from an unexpected state.  Fix the environment (or reset it) and
run the tests again until they all pass.
"""
from pathlib import Path

SECURITY_SCAN_DIR = Path("/home/user/security_scan")
VENV_ACTIVATE = SECURITY_SCAN_DIR / "bin" / "activate"
FREEZE_FILE = SECURITY_SCAN_DIR / "initial_requirements.txt"


def test_security_scan_directory_absent():
    """
    The directory /home/user/security_scan should NOT exist yet.
    """
    assert not SECURITY_SCAN_DIR.exists(), (
        f"The directory {SECURITY_SCAN_DIR} already exists. "
        "Start from a clean state before performing the exercise."
    )


def test_virtual_env_activate_script_absent():
    """
    Because the security_scan directory must not exist yet, its virtual-env
    activation script must also not exist.
    """
    assert not VENV_ACTIVATE.exists(), (
        f"Found an unexpected virtual-environment activation script at "
        f"{VENV_ACTIVATE}. The environment should not be created yet."
    )


def test_initial_requirements_file_absent():
    """
    No requirements snapshot should exist before the learner runs `pip freeze`.
    """
    assert not FREEZE_FILE.exists(), (
        f"Found an unexpected file {FREEZE_FILE}. "
        "The freeze snapshot must be created only after setting up the venv."
    )