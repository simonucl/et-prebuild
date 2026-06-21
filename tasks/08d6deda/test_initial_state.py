# test_initial_state.py
#
# This test-suite verifies that the machine starts in a *clean* state
# before the student runs the “support_diag” collection script.
#
# Nothing that the student is supposed to create (the directory itself
# and the two log-files) should exist yet.  If anything is already
# present, the environment is “dirty” and the exercise is invalid.
#
# The tests intentionally check for ABSENCE of paths mentioned in the
# task description so that the student must create them.

import os
from pathlib import Path
import pytest


HOME_DIR = Path("/home/user")
SUPPORT_DIR = HOME_DIR / "support_diag"
DIAGNOSTICS_LOG = SUPPORT_DIR / "diagnostics.log"
CPUINFO_SNIPPET = SUPPORT_DIR / "cpuinfo_snippet.log"


def _human(path: Path) -> str:
    """Return a nicer string representation for error messages."""
    return str(path)


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(SUPPORT_DIR, id="support_diag_directory"),
        pytest.param(DIAGNOSTICS_LOG, id="diagnostics.log_file"),
        pytest.param(CPUINFO_SNIPPET, id="cpuinfo_snippet.log_file"),
    ],
)
def test_required_paths_do_not_yet_exist(path: Path):
    """
    None of the artefacts that the student is supposed to create
    should be present before the exercise starts.
    """
    assert not path.exists(), (
        f"The path {_human(path)} already exists, but the exercise "
        "requires starting from a clean slate.  Please remove it "
        "so the student can create it during the task."
    )


def test_home_directory_exists_and_is_directory():
    """
    Basic sanity-check: the home directory that the assignment refers to
    must exist and be a directory, otherwise all subsequent paths will
    be invalid.
    """
    assert HOME_DIR.exists(), f"Expected home directory {_human(HOME_DIR)} does not exist."
    assert HOME_DIR.is_dir(), f"Expected {_human(HOME_DIR)} to be a directory."