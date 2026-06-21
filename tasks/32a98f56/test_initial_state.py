# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system
# BEFORE the learner begins the exercise.  These tests guarantee that no
# solution artefacts are already present so the learner starts from a clean
# slate.
#
# IMPORTANT:  If any of these tests fail, either the template repository or
# the execution environment was pre-populated with files/directories that the
# learner is supposed to create.  Remove them before releasing the exercise.

import os
from pathlib import Path
import pytest

# Absolute paths that must *not* exist at the beginning of the exercise.
PERF_ROOT   = Path("/home/user/perf")
INPUT_DIR   = PERF_ROOT / "input"
DB_DIR      = PERF_ROOT / "db"
OUTPUT_DIR  = PERF_ROOT / "output"

CSV_PATH    = INPUT_DIR / "app_metrics.csv"
DB_PATH     = DB_DIR / "metrics.db"
LOG_PATH    = OUTPUT_DIR / "analysis.log"


@pytest.mark.parametrize(
    "path_obj,kind",
    [
        (INPUT_DIR,  "directory"),
        (DB_DIR,     "directory"),
        (OUTPUT_DIR, "directory"),
    ],
)
def test_subdirectories_absent(path_obj: Path, kind: str):
    """
    The three required sub-directories must *not* exist yet.  Learners are
    expected to create them as part of the task.
    """
    assert not path_obj.exists(), (
        f"The {kind} '{path_obj}' already exists, but the learner is supposed "
        "to create it.\n"
        "Remove it from the starter repository or fix the provisioning script."
    )


@pytest.mark.parametrize(
    "file_path,description",
    [
        (CSV_PATH, "input CSV file"),
        (DB_PATH,  "SQLite database"),
        (LOG_PATH, "output analysis log"),
    ],
)
def test_solution_files_absent(file_path: Path, description: str):
    """
    None of the deliverable files should be present in the initial state.
    """
    assert not file_path.exists(), (
        f"The {description} '{file_path}' already exists, but learners must "
        "generate it themselves.  Please delete it from the template."
    )