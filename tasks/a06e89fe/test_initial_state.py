# test_initial_state.py
#
# This pytest suite verifies that the workspace is clean *before* the student
# carries out the task.  None of the required artifacts should exist yet.

import os
from pathlib import Path

import pytest

# Absolute paths that must NOT exist before the student’s work starts.
EXPERIMENT_DIR = Path("/home/user/mlops_benchmark/experiment_01")
BENCH_SCRIPT   = EXPERIMENT_DIR / "benchmark.py"
SUM_FILE       = EXPERIMENT_DIR / "sum.txt"


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (EXPERIMENT_DIR, "experiment directory"),
        (BENCH_SCRIPT,   "benchmark.py script"),
        (SUM_FILE,       "sum.txt artifact"),
    ],
)
def test_required_items_do_not_exist(path_obj: Path, description: str):
    """
    Ensure that no part of the final answer is already present.
    A pre-existing solution would invalidate the exercise.
    """
    assert not path_obj.exists(), (
        f"The {description} '{path_obj}' already exists. "
        "The workspace must be empty before the student starts."
    )