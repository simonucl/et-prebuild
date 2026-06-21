# test_initial_state.py
"""
Pytest suite verifying the *initial* operating-system / filesystem state
before the student has started working on the “diagnostics kit” task.

According to the specification, **nothing related to the kit should
exist yet** – in particular, the /home/user/diag/ directory and its
Makefile must be absent.  These checks purposefully do *not* reference
any path inside /home/user/diag/output/, because those are considered
“output” artefacts and are excluded by the authoring rules.
"""

import os
import stat
import pytest
from pathlib import Path

HOME = Path("/home/user")
DIAG_DIR = HOME / "diag"
MAKEFILE = DIAG_DIR / "Makefile"


def _pretty_path(path: Path) -> str:
    """Return a human-readable, absolute path string."""
    return str(path.resolve())


def test_home_directory_exists_and_is_directory():
    """
    Sanity-check that the expected home directory (/home/user)
    is present and is actually a directory.
    """
    assert HOME.exists(), (
        f"Expected the home directory {_pretty_path(HOME)} to exist, "
        "but it is missing.  The exercise assumes this directory."
    )
    assert HOME.is_dir(), (
        f"Expected {_pretty_path(HOME)} to be a directory, "
        "but something else occupies that path."
    )

    # Optional: ensure we have read/write permissions in HOME.
    mode = HOME.stat().st_mode
    assert bool(mode & stat.S_IWUSR), (
        f"The test runner needs write permission in {_pretty_path(HOME)}."
    )


def test_diag_directory_absent():
    """
    The diagnostics-kit directory (/home/user/diag) must *not* exist yet.
    The student is supposed to create it as part of the assignment.
    """
    assert not DIAG_DIR.exists(), (
        f"Found unexpected directory {_pretty_path(DIAG_DIR)}.  "
        "The initial state should be clean – this directory must "
        "be created later by the student."
    )


def test_makefile_absent():
    """
    Even if the directory were (erroneously) present, the Makefile
    inside it must not already exist in the initial state.
    """
    assert not MAKEFILE.exists(), (
        f"Found unexpected Makefile at {_pretty_path(MAKEFILE)}.  "
        "No project artefacts should be present before the student "
        "begins the task."
    )