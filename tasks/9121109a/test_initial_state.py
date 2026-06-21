# test_initial_state.py
#
# This pytest suite validates the **initial** condition of the workstation
# before the student has created any of the required artefacts for the
# “health-check” snapshot.  At this point none of the target directories
# or files should exist yet.

import os
import pytest
from pathlib import Path

HOME_DIR = Path("/home/user")
TARGET_DIR = HOME_DIR / "ml_diag"
LOG_FILE = TARGET_DIR / "system_snapshot.log"
CSV_FILE = TARGET_DIR / "top5_mem.csv"


def test_home_directory_present():
    """
    Sanity-check that the base home directory exists; if it does not, the
    execution environment itself is broken.
    """
    assert HOME_DIR.is_dir(), (
        f"Expected base directory {HOME_DIR} to exist, "
        "but it is missing. The test environment is not set up correctly."
    )


def test_ml_diag_directory_absent():
    """
    Before the student starts, the /home/user/ml_diag directory should **not**
    exist.  Its presence would mean the exercise has already been (partially)
    completed.
    """
    assert not TARGET_DIR.exists(), (
        f"Directory {TARGET_DIR} already exists. "
        "It should be created by the student, so it must be absent at the initial state."
    )


@pytest.mark.parametrize(
    "path,label",
    [
        (LOG_FILE, "/home/user/ml_diag/system_snapshot.log"),
        (CSV_FILE, "/home/user/ml_diag/top5_mem.csv"),
    ],
)
def test_target_files_absent(path: Path, label: str):
    """
    Confirm that none of the target files are present yet.
    """
    assert not path.exists(), (
        f"File {label} already exists. "
        "It should be created by the student, so it must be absent at the initial state."
    )