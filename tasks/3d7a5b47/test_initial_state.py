# test_initial_state.py
"""
Pytest suite that verifies the *initial* operating-system / filesystem state
*before* the student carries out the credential-rotation task.

If any of the artefacts already exist or look “complete”, the test suite will
fail and clearly indicate what should **not** be present yet.
"""

import os
import subprocess
import sys
from pathlib import Path

HOME = Path("/home/user")

# ---- Paths that must NOT exist (yet) ---------------------------------------

VENV_DIR = HOME / "cred_rotator_env"
VENV_CFG = VENV_DIR / "pyvenv.cfg"
VENV_BIN_PIP = VENV_DIR / "bin" / "pip"

REQUIREMENTS_FILE = VENV_DIR / "requirements.txt"
DOTENV_FILE = HOME / "rotated_credentials.env"
LOG_FILE = HOME / "rotation_success.log"


def _read_path_content(path: Path) -> str:
    """
    Helper that returns the full textual content of `path`
    (or an empty string if the path does not exist).
    """
    if not path.exists():
        return ""
    with path.open("r", encoding="utf-8") as fp:
        return fp.read()


# --------------------------------------------------------------------------- #
# Virtual-environment checks
# --------------------------------------------------------------------------- #
def test_virtualenv_not_yet_created():
    """
    The dedicated virtual-environment directory must not be fully set up yet.

    Rules:
    1. The directory may *not* exist at all, OR
    2. If it does exist (perhaps from a previous failed run), it must *not*
       already contain a functional venv (indicated by a `pyvenv.cfg` file
       and a working `pip` inside `bin/`).

    Having a ready-to-go venv at this point would mean the rotation has
    already been performed, which is outside the “initial state” scope.
    """
    if not VENV_DIR.exists():
        # Ideal: directory completely absent
        assert True
        return

    # Directory is present — ensure it is NOT a ready venv
    assert not VENV_CFG.is_file(), (
        f"Found '{VENV_CFG}' but the environment should NOT exist yet."
    )

    # If bin/pip exists, it must *not* successfully show python-dotenv==1.0.0
    if VENV_BIN_PIP.is_file():
        try:
            completed = subprocess.run(
                [str(VENV_BIN_PIP), "show", "python-dotenv"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )
        except Exception as exc:  # pragma: no cover
            # If pip cannot even run, that's acceptable for the initial state.
            return

        assert (
            "Version: 1.0.0" not in completed.stdout
        ), "python-dotenv==1.0.0 is already installed inside the venv, but it should not be."


# --------------------------------------------------------------------------- #
# requirements.txt checks
# --------------------------------------------------------------------------- #
def test_requirements_file_absent():
    """
    requirements.txt must *not* be present yet.
    """
    assert not REQUIREMENTS_FILE.exists(), (
        f"Unexpected file detected: '{REQUIREMENTS_FILE}'. "
        "The student has not yet generated requirements.txt."
    )


# --------------------------------------------------------------------------- #
# Dotenv credentials file checks
# --------------------------------------------------------------------------- #
def test_dotenv_file_absent():
    """
    The rotated credentials file must not exist in the initial state.
    """
    assert not DOTENV_FILE.exists(), (
        f"Unexpected file detected: '{DOTENV_FILE}'. "
        "The credentials rotation has not been executed yet."
    )


# --------------------------------------------------------------------------- #
# Rotation log checks
# --------------------------------------------------------------------------- #
def test_rotation_log_absent():
    """
    The rotation_success.log file must not be present yet.
    """
    assert not LOG_FILE.exists(), (
        f"Unexpected file detected: '{LOG_FILE}'. "
        "The rotation log should not exist before the student performs the task."
    )


# --------------------------------------------------------------------------- #
# Guidance helper (not an actual test) – can be invoked manually if needed
# --------------------------------------------------------------------------- #
if __name__ == "__main__":  # pragma: no cover
    # Allow maintainers to run the module directly to see a quick summary
    print("== Initial-state checker ==")
    for p in [VENV_DIR, REQUIREMENTS_FILE, DOTENV_FILE, LOG_FILE]:
        print(f"{p}: {'present' if p.exists() else 'absent'}")