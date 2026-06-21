# test_initial_state.py
"""
Pytest suite that verifies the machine is in a **clean initial state**
_before_ the student starts working on the “deploy_demo” exercise.

The student will be asked to create:

    /home/user/deploy_demo/                (directory)
    /home/user/deploy_demo/venv/           (virtual-env)
    /home/user/deploy_demo/deployment.log  (one-line log file)

To make sure the exercise is fair, none of those artefacts should exist yet.
These tests fail loudly if any of them are already present.
Only the Python stdlib and pytest are used.
"""

from pathlib import Path
import os
import stat

BASE_DIR = Path("/home/user/deploy_demo")
VENV_DIR = BASE_DIR / "venv"
PYTHON_BIN = VENV_DIR / "bin" / "python"
LOG_FILE = BASE_DIR / "deployment.log"


def _describe_path(path: Path) -> str:
    """
    Return a human-readable description of the current state of `path`.
    Helps produce clearer assertion messages.
    """
    if not path.exists():
        return f"{path} does not exist"
    if path.is_symlink():
        target = os.readlink(path)
        return f"{path} is a symlink → {target!r}"
    if path.is_dir():
        return f"{path} is a directory"
    if path.is_file():
        # Show size and mode for extra debugging info
        size = path.stat().st_size
        mode = stat.filemode(path.stat().st_mode)
        return f"{path} is a file ({size} bytes, mode {mode})"
    return f"{path} exists but is of unknown type"


def test_base_directory_absent():
    """
    The top-level directory /home/user/deploy_demo must **not** exist yet.
    """
    assert not BASE_DIR.exists(), (
        "Pre-existing artefact found! The working directory for this exercise "
        "already exists but it should not. "
        f"Current state: {_describe_path(BASE_DIR)}"
    )


def test_virtualenv_absent():
    """
    The virtual-env directory /home/user/deploy_demo/venv must **not** exist.
    """
    assert not VENV_DIR.exists(), (
        "A virtual-environment directory is already present.  "
        "The student must create it themselves.  "
        f"Current state: {_describe_path(VENV_DIR)}"
    )
    assert not PYTHON_BIN.exists(), (
        "A Python interpreter for the virtual-env already exists at "
        f"{PYTHON_BIN}.  "
        "The filesystem should be clean before the exercise starts."
    )


def test_log_file_absent():
    """
    The deployment log file /home/user/deploy_demo/deployment.log must **not** exist.
    """
    assert not LOG_FILE.exists(), (
        "The deployment log file already exists but the student must generate it.  "
        f"Current state: {_describe_path(LOG_FILE)}"
    )