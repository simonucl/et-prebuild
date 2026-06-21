# test_initial_state.py
"""
Pytest suite to validate the initial state of the operating system **before**
the student creates any artefacts for the “observability-docs” exercise.

We explicitly avoid touching (or even mentioning) any of the files/directories
that the student is supposed to create later, in accordance with the grading
rules.  Instead, we make sure the base environment is sane and provides the
utilities the student will need to succeed.
"""

import os
import stat
import subprocess
from pathlib import Path

HOME = Path("/home/user")


def test_home_directory_exists_and_is_directory():
    """
    The canonical home directory must exist and be a directory so that the
    student can create new content under it.
    """
    assert HOME.exists(), f"Expected home directory {HOME} to exist."
    assert HOME.is_dir(), f"Expected {HOME} to be a directory."


def test_home_directory_permissions_are_reasonable():
    """
    Basic sanity-check on directory permissions:
    • Owner must have read & write access so the student can create files.
    • Directory should not be world-writable (security hygiene).
    """
    mode = HOME.stat().st_mode
    owner_readable = bool(mode & stat.S_IRUSR)
    owner_writable = bool(mode & stat.S_IWUSR)
    world_writable = bool(mode & stat.S_IWOTH)

    assert owner_readable, f"{HOME} is not readable by its owner."
    assert owner_writable, f"{HOME} is not writable by its owner."
    assert not world_writable, f"{HOME} should not be world-writable."


def test_basic_unix_utilities_available():
    """
    The upcoming instructions suggest using tools such as `grep` to perform a
    trailing-space lint.  We verify that at least `grep` is on PATH and
    runnable.
    """
    try:
        completed = subprocess.run(
            ["grep", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:  # pragma: no cover
        assert False, (
            "`grep` is not installed or not found in PATH; it is required for "
            "the lint step described in the assignment."
        )

    # `grep --version` should return exit code 0 and produce some output
    assert (
        completed.returncode == 0
    ), "`grep` is present but running `grep --version` failed."
    assert completed.stdout.strip(), "`grep --version` produced no output."