# test_initial_state.py
#
# Pytest suite to validate that the operating-system / filesystem is
# still in its pristine state *before* the student starts working on the
# “perf_venv” task.  The presence of any of the target artefacts would
# indicate that the exercise has already (partially) been performed and
# therefore constitutes a test failure.
#
# Do **not** modify this file.

import os
from pathlib import Path

ROOT_DIR = Path("/home/user/perf_venv")
ENV_DIR = ROOT_DIR / "env"
PYTHON_BIN = ENV_DIR / "bin" / "python"
PYVENV_CFG = ENV_DIR / "pyvenv.cfg"
SETUP_LOG = ROOT_DIR / "setup.log"


def _human(path: Path) -> str:
    """Return a human-readable representation of a filesystem path."""
    return f"‘{path}’"


def test_root_directory_absent():
    """
    The top-level directory /home/user/perf_venv/ must NOT exist yet.
    Its presence would mean the student has already begun the setup.
    """
    assert not ROOT_DIR.exists(), (
        f"{_human(ROOT_DIR)} already exists. "
        "The working directory should be created *by the student*, "
        "so it must be absent at the beginning."
    )


def test_env_directory_absent():
    """
    The virtual-environment directory must NOT exist before the task is started.
    """
    assert not ENV_DIR.exists(), (
        f"{_human(ENV_DIR)} already exists. "
        "The virtual environment must be created by the student."
    )


def test_virtualenv_artifacts_absent():
    """
    Neither the python executable nor the pyvenv.cfg file should exist.
    """
    assert not PYTHON_BIN.exists(), (
        f"Unexpected file {_human(PYTHON_BIN)} found. "
        "The virtual environment has apparently already been created."
    )
    assert not PYVENV_CFG.exists(), (
        f"Unexpected file {_human(PYVENV_CFG)} found. "
        "The virtual environment has apparently already been created."
    )


def test_setup_log_absent():
    """
    The verification log file must NOT be present yet.
    """
    assert not SETUP_LOG.exists(), (
        f"Unexpected file {_human(SETUP_LOG)} found. "
        "The setup log should be produced only after completing the task."
    )