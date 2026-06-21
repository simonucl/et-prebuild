# test_initial_state.py
#
# This pytest suite verifies that the workspace is in the *initial* state
# expected *before* the student begins the assignment.  In this context
# “initial” means that none of the artefacts the student is supposed to
# create already exist.  If any of them are found, we fail fast with a
# helpful explanation so that the learner (or the automated runner) knows
# the environment is contaminated.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
BENCHMARKS_DIR = HOME / "benchmarks"
SAMPLE_TXT = BENCHMARKS_DIR / "sample.txt"
RESULTS_CSV = HOME / "benchmark_results.csv"


@pytest.mark.parametrize(
    "path,kind",
    [
        (BENCHMARKS_DIR, "directory"),
        (SAMPLE_TXT, "file"),
        (RESULTS_CSV, "file"),
    ],
)
def test_expected_items_do_not_exist_yet(path: Path, kind: str):
    """
    Ensure the artefacts the student must create are *absent* before work starts.

    If any of these items are found, the initial state is considered invalid
    because the learner would not be starting from a clean slate.
    """
    assert not path.exists(), (
        f"Initial-state violation: expected the {kind} `{path}` to *not* exist yet, "
        "but it is already present.  Please reset the workspace before running "
        "the task."
    )