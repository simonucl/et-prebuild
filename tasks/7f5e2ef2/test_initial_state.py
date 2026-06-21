# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem
# is in the expected *clean* state BEFORE the student performs any
# actions for the “Binary-Curation” task.

import os
from pathlib import Path

VENV_DIR = Path("/home/user/.venvs")
ENV_PATH = VENV_DIR / "curation_env"
CURATION_DIR = Path("/home/user/curation")
OUTPUT_DIR = CURATION_DIR / "output"
LOCK_FILE = OUTPUT_DIR / "locked_requirements.txt"
REPORT_FILE = OUTPUT_DIR / "curation_report.log"


def _absent(path: Path) -> None:
    """
    Helper: assert that ``path`` does NOT exist in the filesystem.

    Parameters
    ----------
    path : Path
        The absolute path that must be absent.

    Raises
    ------
    AssertionError
        If the path exists.
    """
    assert not path.exists(), (
        f"Pre-condition failed: '{path}' already exists, "
        "but the exercise expects the student to create it."
    )


def test_venvs_directory_absent():
    """
    The directory /home/user/.venvs must *not* exist yet.
    """
    _absent(VENV_DIR)


def test_curation_env_absent():
    """
    The virtual-environment directory /home/user/.venvs/curation_env
    must *not* exist yet.
    """
    _absent(ENV_PATH)


def test_curation_output_files_absent():
    """
    No output directory or files (locked_requirements.txt,
    curation_report.log) should exist yet.
    """
    _absent(LOCK_FILE)
    _absent(REPORT_FILE)
    # The parent output directory itself should also not exist.
    _absent(OUTPUT_DIR)