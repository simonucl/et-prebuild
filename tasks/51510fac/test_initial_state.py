# test_initial_state.py
"""
Pytest suite to validate the *initial* state of the operating system / filesystem
before the student performs any tasks for the “Build Diagnostics Report” project.

The environment is expected to be CLEAN—none of the directories, files, or
archives that the student must create later should already exist.

If any of these objects are found, the tests will fail with a clear message,
alerting both the student and the grader that the initial state is incorrect.
"""

import os
import pytest


# Base paths that must NOT exist at the start of the assignment
BASE_DIR = "/home/user/build_artifacts"
DIAG_DIR = os.path.join(BASE_DIR, "diagnostics")
LOG_FILE = os.path.join(DIAG_DIR, "system_diagnostics.log")
TARBALL = os.path.join(BASE_DIR, "build_diagnostics.tar.gz")


@pytest.mark.parametrize(
    "path,kind",
    [
        (DIAG_DIR, "directory"),
        (LOG_FILE, "file"),
        (TARBALL, "file"),
    ],
)
def test_absence_of_expected_outputs(path: str, kind: str):
    """
    Validate that the diagnostics directory, log file, and tarball do NOT exist
    before the student runs their solution script.
    """
    assert not os.path.exists(path), (
        f"The {kind} '{path}' should NOT exist yet. "
        "The working directory must start clean so the student's script can "
        "create it from scratch."
    )