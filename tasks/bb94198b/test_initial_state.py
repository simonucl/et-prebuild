# test_initial_state.py
#
# This pytest suite verifies that the OS / filesystem is in the clean
# “pre-exercise” state.  It should run **before** the student starts
# working, so we explicitly assert that the microservices Makefile
# requested by the assignment is **not** present yet.

from pathlib import Path
import os
import pytest

HOME_DIR = Path("/home/user")
MICROSERVICES_DIR = HOME_DIR / "microservices"
MAKEFILE_PATH = MICROSERVICES_DIR / "Makefile"


def test_home_directory_exists():
    """
    Sanity-check that the base home directory exists.
    If this fails, the VM itself is mis-configured.
    """
    assert HOME_DIR.is_dir(), (
        f"Expected home directory {HOME_DIR} to exist and be a directory."
    )


def test_makefile_does_not_exist_yet():
    """
    The student has not created the Makefile yet, so it must be absent.
    If it is already present, the starting state is incorrect.
    """
    assert not MAKEFILE_PATH.exists(), (
        f"Found unexpected file at {MAKEFILE_PATH}.\n"
        "The Makefile should not exist before the exercise begins."
    )


def test_microservices_directory_state():
    """
    The microservices directory may or may not exist at this point:
    1. If it does NOT exist, that is acceptable (the student will create it).
    2. If it DOES exist, it must be a directory (not a file, socket, etc.)
       and must not already contain the Makefile.
    """
    if MICROSERVICES_DIR.exists():
        assert MICROSERVICES_DIR.is_dir(), (
            f"{MICROSERVICES_DIR} exists but is not a directory."
        )
        # Re-verify Makefile absence inside an existing directory.
        assert not MAKEFILE_PATH.exists(), (
            f"Directory {MICROSERVICES_DIR} already contains {MAKEFILE_PATH.name}; "
            "the exercise requires the student to create it."
        )


def test_no_leftover_partial_files():
    """
    Guard against stray attempts: there should be no files whose names
    start with 'Makefile' (e.g. backups) inside /home/user/microservices/.
    This ensures a pristine workspace.
    """
    if MICROSERVICES_DIR.is_dir():
        leftovers = sorted(
            p for p in MICROSERVICES_DIR.iterdir()
            if p.name.startswith("Makefile")
        )
        assert not leftovers, (
            "Unexpected file(s) starting with 'Makefile' found in "
            f"{MICROSERVICES_DIR}:\n  " + "\n  ".join(str(p) for p in leftovers)
        )