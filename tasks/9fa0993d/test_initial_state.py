# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “network-health check” workflow **before** the student
# creates anything.
#
# What must NOT exist yet:
#   1. Directory  : /home/user/network_diag
#   2. File       : /home/user/network_diag/ping_localhost_raw.log
#   3. File       : /home/user/network_diag/diagnostic_results.log
#
# If any of the above are present, the tests will fail with a clear,
# actionable message so that the learner starts from a clean state.
#
# Only Python’s stdlib and pytest are used, as required.

import os
import pytest
from pathlib import Path

# Absolute paths that should be absent before the learner runs their solution
BASE_DIR = Path("/home/user/network_diag")
PING_LOG = BASE_DIR / "ping_localhost_raw.log"
RESULTS_LOG = BASE_DIR / "diagnostic_results.log"


@pytest.mark.parametrize(
    "path, kind",
    [
        (BASE_DIR, "directory"),
        (PING_LOG, "file"),
        (RESULTS_LOG, "file"),
    ],
)
def test_path_absence(path: Path, kind: str):
    """
    Ensure that none of the target artefacts exist yet.

    Rationale
    ---------
    Students are expected to create the directory and files as part of the task.
    If any of them are already present before the automation runs, it means the
    workspace is not in the required pristine state.
    """
    assert not path.exists(), (
        f"Unexpected {kind} found at {path}. "
        "The workspace must start clean: please remove this artefact before running the task."
    )