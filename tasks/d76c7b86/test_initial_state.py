# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the correct *initial* state before the student starts working.
#
# Expected INITIAL state:
#   • /home/user/projects/simple_app/            → must already exist.
#   • /home/user/projects/simple_app/.venv/      → must NOT exist yet.
#   • /home/user/projects/simple_app/requirements.txt
#                                               → must NOT exist yet.
#   • /home/user/projects/simple_app/logs/       → must NOT exist yet.
#   • /home/user/projects/simple_app/logs/package_list.log
#                                               → must NOT exist yet.
#
# Any deviation from this state indicates that the exercise environment
# is not clean and will cause the tests to fail with a clear explanation.

import os
from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/projects/simple_app")
VENV_DIR = BASE_DIR / ".venv"
REQ_FILE = BASE_DIR / "requirements.txt"
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "package_list.log"


def _human(path: Path) -> str:
    """Return a human-readable absolute path for error messages."""
    return str(path.resolve())


def test_base_directory_exists():
    """The starting project directory must already be present."""
    assert BASE_DIR.is_dir(), (
        f"Expected base directory {_human(BASE_DIR)} to exist, "
        "but it is missing. The exercise requires this directory as the "
        "working root."
    )


def test_virtualenv_does_not_exist_yet():
    """No virtual-environment should be present before the student creates it."""
    assert not VENV_DIR.exists(), (
        f"Found unexpected virtual-environment directory {_human(VENV_DIR)}. "
        "The exercise begins without any venv; the student must create it."
    )


def test_requirements_file_absent():
    """requirements.txt should NOT exist at the start."""
    assert not REQ_FILE.exists(), (
        f"Found unexpected file {_human(REQ_FILE)}. "
        "requirements.txt must be created by the student."
    )


def test_logs_directory_absent():
    """logs/ directory should NOT exist at the start."""
    assert not LOGS_DIR.exists(), (
        f"Found unexpected directory {_human(LOGS_DIR)}. "
        "The logs/ directory will be created by the student."
    )


def test_log_file_absent():
    """package_list.log should NOT exist at the start (no logs directory either)."""
    assert not LOG_FILE.exists(), (
        f"Found unexpected file {_human(LOG_FILE)}. "
        "package_list.log must be produced by the student after creating the logs/ directory."
    )