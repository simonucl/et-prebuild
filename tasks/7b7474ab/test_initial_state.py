# test_initial_state.py
#
# This pytest suite verifies the “clean-slate” conditions **before** the
# student runs any command.  Nothing relevant to the task should already
# exist; otherwise the subsequent grading steps could yield false
# positives.  In particular, neither of the target files may be present.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONFIG_DIR = HOME / "service_configs"

TARGET_FILES = [
    CONFIG_DIR / "backup_schedule.yaml",
    CONFIG_DIR / "backup_schedule.toml",
]


@pytest.mark.parametrize("path", TARGET_FILES)
def test_target_files_do_not_exist(path: Path):
    """
    Ensure the two configuration files are completely absent before the
    student performs the task.

    Rationale:
    1. A pre-existing file could make the final tests pass without the
       student having executed the required command.
    2. If such a file exists, the student must remove or overwrite it;
       thus we fail early to signal a contaminated workspace.
    """
    assert not path.exists(), (
        f"Unexpected pre-existing file: {path}. "
        "The workspace must start clean; please remove this file before running your solution."
    )