# test_initial_state.py
#
# Pytest suite that verifies the **initial** operating-system / filesystem
# conditions _before_ the student begins the exercise described in the
# prompt.  NOTHING that the student is supposed to create should exist yet.
#
# The tests purposely **fail** if any artefact from the target solution
# is already present.  This guards against polluted or pre-baked images and
# ensures the learner really has to perform every step themselves.
#
# Only Python’s standard library plus pytest are used.

from pathlib import Path
import os
import subprocess
import sys
import pytest


# Constants for the artefacts that must **not** exist at the outset.
WORK_DIR = Path("/home/user/cloud_finops")
REQUIREMENTS_FILE = WORK_DIR / "requirements.txt"
VENV_DIR = WORK_DIR / "finops_env"
VENV_ACTIVATE = VENV_DIR / "bin" / "activate"          # Linux container assumed.
FREEZE_LOG = WORK_DIR / "installation_log.txt"


def _assert_absent(path: Path, kind: str):
    """
    Helper that asserts a file or directory does NOT exist.

    Parameters
    ----------
    path : Path
        Absolute path to the artefact that should be absent.
    kind : str
        Human-readable description, e.g. "directory", "file".

    Raises
    ------
    AssertionError
        If the artefact exists.
    """
    assert not path.exists(), (
        f"The {kind} {path} already exists, but this environment is supposed "
        f"to be clean.  Please start from a fresh workspace so the learner "
        f"can create the artefact themselves."
    )


def test_work_directory_absent_initially():
    """/home/user/cloud_finops must NOT exist before the exercise starts."""
    _assert_absent(WORK_DIR, "directory")


def test_requirements_file_absent_initially():
    """/home/user/cloud_finops/requirements.txt must NOT pre-exist."""
    _assert_absent(REQUIREMENTS_FILE, "file")


def test_virtualenv_absent_initially():
    """/home/user/cloud_finops/finops_env must NOT exist yet."""
    _assert_absent(VENV_DIR, "directory")


def test_virtualenv_activate_script_absent_initially():
    """The venv’s activate script must also be absent (implied by venv absence)."""
    _assert_absent(VENV_ACTIVATE, "file")


def test_freeze_log_absent_initially():
    """/home/user/cloud_finops/installation_log.txt must NOT exist yet."""
    _assert_absent(FREEZE_LOG, "file")


def test_packages_not_preinstalled_system_wide():
    """
    The exact versions requested in the task should NOT already be installed
    system-wide.  Having them globally could mask mistakes in virtual-env
    creation later on.  We allow versions to be absent entirely or present
    with **different** versions; we only forbid an exact match.
    """
    required = {
        "boto3": "1.34.105",
        "numpy": "1.26.4",
        "pandas": "2.2.2",
    }

    # Query currently active interpreter’s pip for installed packages.
    try:
        # Use `python -m pip freeze` so that it works even if pip is a module.
        completed = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Unable to run pip freeze in the initial environment: {exc}")

    frozen = {
        line.strip().split("==", maxsplit=1)[0]: line.strip().split("==", maxsplit=1)[1]
        for line in completed.stdout.splitlines()
        if "==" in line
    }

    offending = [
        f"{name}=={ver}"
        for name, ver in required.items()
        if frozen.get(name) == ver
    ]
    assert not offending, (
        "The following required package versions are already installed "
        "system-wide, which could mask errors in the learner’s forthcoming "
        f"virtual-environment setup: {', '.join(offending)}.  Please start "
        "from a cleaner base image or uninstall these versions."
    )