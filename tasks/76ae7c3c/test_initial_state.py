# test_initial_state.py
"""
PyTest suite that verifies the **initial** state of the operating system /
filesystem before the student begins the exercise.

Nothing that the student is expected to create *later* should already exist.
If any of the required artefacts are found now, the test suite will fail with
a clear, actionable message.

IMPORTANT:  Do NOT modify this file.
"""

import os
from pathlib import Path

import pytest

# Base path the student will work under
BASE_DIR = Path("/home/user/microservices")

# --------------------------------------------------------------------------- #
# Helper lists of paths that must NOT exist yet                               #
# --------------------------------------------------------------------------- #

# Full directory paths that the student will have to create later
EXPECTED_DIRS = [
    BASE_DIR,                           # /home/user/microservices
    BASE_DIR / "auth",
    BASE_DIR / "billing",
    BASE_DIR / "gateway",
]

# Full file paths that the student will have to create later
EXPECTED_FILES = [
    BASE_DIR / "auth" / ".env",
    BASE_DIR / "billing" / ".env",
    BASE_DIR / "gateway" / ".env",
    BASE_DIR / "config_summary.log",
]

# --------------------------------------------------------------------------- #
# Parametrised tests                                                          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("path", EXPECTED_DIRS, ids=[str(p) for p in EXPECTED_DIRS])
def test_expected_directories_do_not_exist_yet(path: Path):
    """
    Ensure that none of the directories the student has to create
    already exist in the starting environment.
    """
    assert not path.exists(), (
        f"Unexpected pre-existing directory: {path}\n"
        "The exercise requires the student to create this directory. "
        "Remove it so the test starts from a clean slate."
    )


@pytest.mark.parametrize("path", EXPECTED_FILES, ids=[str(p) for p in EXPECTED_FILES])
def test_expected_files_do_not_exist_yet(path: Path):
    """
    Ensure that none of the files the student has to create
    already exist in the starting environment.
    """
    assert not path.exists(), (
        f"Unexpected pre-existing file: {path}\n"
        "The exercise requires the student to create this file. "
        "Remove it so the test starts from a clean slate."
    )