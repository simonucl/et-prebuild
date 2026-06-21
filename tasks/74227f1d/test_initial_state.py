# test_initial_state.py
#
# This pytest suite validates that the system **before** the student’s action
# is clean: no virtual-environment artefacts already exist at the target
# locations.  A failing test means the workspace is not in the expected
# initial state and would give the student an unfair advantage (or create
# ambiguity) when they attempt the task.

import os
from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Paths that must *not* exist yet
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
BASE_DIR = HOME / "artifact-curator"
VENV_DIR = BASE_DIR / "venv-curator"
PYTHON_BIN = VENV_DIR / "bin" / "python"
PYVENV_CFG = VENV_DIR / "pyvenv.cfg"


def _human(path: Path) -> str:  # helper for nicer error messages
    return str(path)


def test_venv_directory_absent():
    """
    The virtual-environment directory must not pre-exist.
    """
    assert not VENV_DIR.exists(), (
        "The directory {p} already exists, but the student is "
        "supposed to create it from scratch.".format(p=_human(VENV_DIR))
    )


def test_pyvenv_cfg_absent():
    """
    No `pyvenv.cfg` file may be present yet.
    """
    assert not PYVENV_CFG.exists(), (
        "Found unexpected file {p}.  The virtual environment appears to have "
        "been created already.".format(p=_human(PYVENV_CFG))
    )


def test_python_executable_absent():
    """
    The virtual-environment Python interpreter must not pre-exist.
    """
    assert not PYTHON_BIN.exists(), (
        "Found unexpected Python executable at {p}.  The environment should "
        "not be in place before the student runs their command.".format(
            p=_human(PYTHON_BIN)
        )
    )