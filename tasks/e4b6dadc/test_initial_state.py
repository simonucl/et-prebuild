# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state for the
# “artifact-project” exercise *before* any student actions are taken.
#
# Expectations / “truth”:
#   • The directory /home/user/artifact-project *exists*.
#   • It is completely *empty* (no files, no sub-directories).
#   • Specifically, the following must **NOT** exist yet:
#       – /home/user/artifact-project/Makefile
#       – /home/user/artifact-project/build/
#       – /home/user/artifact-project/reports/
#       – /home/user/artifact-project/dist/
#
# Any deviation from these expectations should cause the test(s) to fail
# with a clear, actionable error message.

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/artifact-project").resolve()

def test_project_directory_exists():
    """The project directory must be present."""
    assert PROJECT_ROOT.exists(), (
        f"Expected directory {PROJECT_ROOT} is missing."
    )
    assert PROJECT_ROOT.is_dir(), (
        f"{PROJECT_ROOT} exists but is not a directory."
    )

def test_project_directory_is_empty():
    """The project directory must be completely empty to begin with."""
    contents = list(PROJECT_ROOT.iterdir())
    assert contents == [], (
        f"{PROJECT_ROOT} is expected to be empty, but contains: "
        f"{', '.join(map(str, contents))}"
    )

def test_no_preexisting_makefile():
    """Makefile must *not* exist before the student creates it."""
    makefile = PROJECT_ROOT / "Makefile"
    assert not makefile.exists(), (
        f"Unexpected Makefile found at {makefile}; the repository should "
        f"start empty."
    )

def _assert_path_absent(relpath: str):
    """Helper asserting that a given path under PROJECT_ROOT is absent."""
    path = PROJECT_ROOT / relpath
    assert not path.exists(), (
        f"Unexpected path {path} already exists; initial state must be empty."
    )

def test_no_build_reports_dist_directories():
    """build/, reports/, and dist/ must not exist yet."""
    for dirname in ("build", "reports", "dist"):
        _assert_path_absent(dirname)