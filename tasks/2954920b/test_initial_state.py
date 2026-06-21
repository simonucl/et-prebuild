# test_initial_state.py
#
# Pytest suite to verify the **initial** operating-system / filesystem state
# before the student starts working on the “training_pipeline” exercise.
#
# These tests intentionally assert that *nothing* from the final deliverables
# is present yet.  They will fail as soon as the student begins creating the
# required artefacts, which is exactly what we want: the tests are meant to be
# executed only once—right at the very beginning—so that the learner can be
# certain they are starting from a clean slate.
#
# NOTE:  Use *only* the Python standard library plus pytest (no third-party
#        imports).  All failure messages are explicit so that the student knows
#        precisely what pre-existing artefact or process must be removed.

import os
import stat
import subprocess
import pytest
from pathlib import Path

# Constants used throughout the tests
HOME = Path("/home/user")
PIPELINE_DIR = HOME / "training_pipeline"
SCRIPT_FILE = PIPELINE_DIR / "preprocess_data.py"
LOG_FILE = PIPELINE_DIR / "preprocess.log"
SUMMARY_FILE = PIPELINE_DIR / "process_summary.txt"
SCRIPT_BASENAME = "preprocess_data.py"


def _running_pids_for_script() -> list[int]:
    """
    Return a list of PIDs whose command-line contains the target script name.
    Uses the ubiquitous `ps` command to remain within the standard library.
    """
    try:
        ps_output = subprocess.check_output(
            ["ps", "-eo", "pid,cmd"], text=True, encoding="utf-8", errors="ignore"
        )
    except Exception:
        # If ps is not available for some reason, fall back to an empty list.
        return []

    matching_pids: list[int] = []
    for line in ps_output.splitlines():
        # Every line is expected to be "  PID CMD…"
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        pid_str, cmd = parts
        if SCRIPT_BASENAME in cmd:
            try:
                matching_pids.append(int(pid_str))
            except ValueError:
                continue
    return matching_pids


@pytest.mark.describe("Training-pipeline directory should NOT yet exist")
def test_pipeline_directory_absent():
    assert not PIPELINE_DIR.exists(), (
        f"The directory {PIPELINE_DIR} already exists. "
        "Start the exercise in a clean environment where this directory is absent."
    )


@pytest.mark.describe("No artefact files should pre-exist")
@pytest.mark.parametrize(
    "path,description",
    [
        (SCRIPT_FILE, "Python script"),
        (LOG_FILE, "log file"),
        (SUMMARY_FILE, "process summary file"),
    ],
)
def test_artefact_files_absent(path: Path, description: str):
    assert not path.exists(), (
        f"The {description} {path} already exists. "
        "Ensure the initial state contains no leftover files from a previous run."
    )


@pytest.mark.describe("The preprocessing script should NOT be running initially")
def test_no_preprocessing_process_running():
    pids = _running_pids_for_script()
    assert not pids, (
        "Found running process(es) for preprocess_data.py at initial state: "
        f"PIDs {pids}.  Make sure no leftover jobs are running before you begin."
    )