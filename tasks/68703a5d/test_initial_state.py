# test_initial_state.py
#
# This pytest file verifies the *initial* state of the operating
# system / filesystem *before* the student starts working on the task.
#
# The task eventually requires creation of:
#   1. /home/user/l10n_env          (a Python virtual-environment dir)
#   2. /home/user/l10n_env/bin/activate
#   3. /home/user/l10n_env/polib_version.log
#
# Prior to any student action those artefacts must **not** exist.
# These tests will fail (with clear messages) if any of them are
# already present, thereby guaranteeing a clean slate for the exercise.

import os
from pathlib import Path

HOME = Path("/home/user")
VENV_DIR = HOME / "l10n_env"
ACTIVATE_SCRIPT = VENV_DIR / "bin" / "activate"
LOG_FILE = VENV_DIR / "polib_version.log"


def _assert_absent(path: Path, what: str) -> None:
    """Helper to assert that `path` does NOT exist on the filesystem."""
    assert not path.exists(), (
        f"{what} should NOT exist yet, but was found at:\n  {path}\n"
        "Make sure you are running these tests before creating the "
        "virtual-environment or any related files."
    )


def test_venv_directory_absent():
    """The l10n_env virtual-environment directory must not pre-exist."""
    _assert_absent(VENV_DIR, "Virtual-environment directory '/home/user/l10n_env'")


def test_activate_script_absent():
    """The activate script must not pre-exist (covers partial dir creation)."""
    _assert_absent(
        ACTIVATE_SCRIPT,
        "Virtual-environment activation script '/home/user/l10n_env/bin/activate'",
    )


def test_verification_log_absent():
    """The verification log must not pre-exist."""
    _assert_absent(
        LOG_FILE,
        "Verification log '/home/user/l10n_env/polib_version.log'",
    )