# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student begins working on the assignment.
#
# Expected truth:
#   •  /home/user/project/src/main.c         must exist (regular file)
#   •  /home/user/project                    must *not* yet contain:
#        - Makefile
#        - bin/           (or anything inside it)
#        - results/       (or anything inside it)
#   •  Nothing under  /home/user/project/bin/  or  results/  exists, because
#     those directories themselves must be absent.
#
# If any of these assertions fail, the starter repository is in an
# unexpected state and the assignment instructions cannot be trusted.

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
SRC_MAIN_C   = PROJECT_ROOT / "src" / "main.c"
MAKEFILE     = PROJECT_ROOT / "Makefile"
BIN_DIR      = PROJECT_ROOT / "bin"
RESULTS_DIR  = PROJECT_ROOT / "results"


def assert_not_exist(path: Path, why: str) -> None:
    """
    Helper that fails the test with a meaningful message if *path* exists.
    """
    assert not path.exists(), (
        f"{why}: the path '{path}' should NOT exist at the initial state, "
        "but it is present."
    )


def test_initial_source_file_present() -> None:
    """
    Verify the only pre-existing artefact is the lone C source file.
    """
    assert SRC_MAIN_C.is_file(), (
        "Expected the starter source file '/home/user/project/src/main.c' to exist, "
        "but it is missing."
    )


def test_makefile_absent() -> None:
    """
    The student has not yet authored a Makefile.
    """
    assert_not_exist(MAKEFILE, "Makefile already present")


def test_bin_and_results_dirs_absent() -> None:
    """
    No build or result artefacts should be present before the assignment is attempted.
    """
    assert_not_exist(BIN_DIR, "Build directory '/home/user/project/bin' unexpectedly exists")
    assert_not_exist(RESULTS_DIR, "Results directory '/home/user/project/results' unexpectedly exists")


def test_no_prebuilt_artifacts() -> None:
    """
    Guard against stray artefacts if the directories *do* exist for some reason.
    """
    for artefact in [
        PROJECT_ROOT / "bin" / "app",
        PROJECT_ROOT / "results" / "profile.out",
        PROJECT_ROOT / "results" / "benchmark.log",
    ]:
        assert_not_exist(artefact, f"Pre-built artefact '{artefact}' already present")