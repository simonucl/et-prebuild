# test_initial_state.py
#
# This test-suite validates that the workstation is still in its pristine
# state *before* the student carries out the exercise.  Nothing related to
# the required artefacts should exist yet.

import os
from pathlib import Path

import pytest

# Canonical paths that must NOT exist at this stage
BASE_DIR = Path("/home/user/monitoring_logs")
LOG_FILE = BASE_DIR / "pre_clean_diag.log"
SUMMARY_FILE = BASE_DIR / "pre_clean_diag_summary.txt"


def _human(path: Path) -> str:
    """
    Return a user-friendly string representation of a Path object that plays
    nicely with pytest’s assertion-rewriting.
    """
    return f"'{str(path)}'"


def test_monitoring_logs_directory_does_not_exist():
    """
    The directory /home/user/monitoring_logs must NOT exist yet.  It will be
    created by the student’s solution.  If it is already present the starting
    state is polluted.
    """
    assert not BASE_DIR.exists(), (
        f"Unexpected directory found: {_human(BASE_DIR)}. "
        "The exercise expects this directory to be created by the student; "
        "it must not be pre-existing."
    )


@pytest.mark.parametrize(
    "path",
    [LOG_FILE, SUMMARY_FILE],
    ids=lambda p: str(p),
)
def test_output_files_do_not_exist(path: Path):
    """
    Neither of the required output files should be present before the student
    runs their commands.
    """
    assert not path.exists(), (
        f"Unexpected file found: {_human(path)}. "
        "This file must be created by the student's code, not supplied in the "
        "initial environment."
    )