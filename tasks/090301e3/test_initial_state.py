# test_initial_state.py
"""
Pytest suite that verifies the filesystem is pristine *before*
the student carries out the setup instructions for projectA.

If any of these tests fail it means the exercise is starting from an
already-configured (or otherwise polluted) state, which would invalidate
the assessment.
"""

import os
from pathlib import Path

import pytest

# Base directory that will eventually be created by the student.
BASE_DIR = Path("/home/user/test_envs/projectA")

# All directories that are expected to be created during the task.
EXPECTED_DIRECTORIES = [
    BASE_DIR,
    BASE_DIR / "configs",
    BASE_DIR / "logs",
    BASE_DIR / "scripts",
    BASE_DIR / "venv",
]

# All files that are expected to be created during the task.
EXPECTED_FILES = [
    BASE_DIR / "scripts" / "env_init.sh",
    BASE_DIR / "configs" / "runtime_config.json",
    BASE_DIR / "logs" / "setup.log",
]

# Union of all artefacts.
ALL_EXPECTED_PATHS = EXPECTED_DIRECTORIES + EXPECTED_FILES


def _idfn(path: Path) -> str:  # Helper for nice parametrised-test names.
    return str(path)


@pytest.mark.parametrize("path", ALL_EXPECTED_PATHS, ids=_idfn)
def test_expected_paths_do_not_exist(path: Path) -> None:
    """
    Assert that none of the directories/files the student is supposed
    to create are present yet.
    """
    assert not path.exists(), (
        f"The path {path} already exists, but the test environment must "
        f"start clean. Remove this path (file or directory) before "
        f"proceeding with the setup exercise."
    )