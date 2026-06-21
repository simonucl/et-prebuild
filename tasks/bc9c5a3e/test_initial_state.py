# test_initial_state.py
#
# Pytest suite that validates the host *before* the student performs any
# actions for the “re-runable performance benchmark” assignment.
#
# ────────────────────────────────────────────────────────────────────────────
# What we check (and why):
#
# 1. /home/user must exist                      → the working area is present.
# 2. /home/user must be writable                → the script must be able to
#    create its own sub-directories and files.
# 3. A concise set of mandatory, *built-in*     → the assignment explicitly
#    command-line tools must be available          forbids installing extras
#    somewhere on $PATH:                           yet requires these tools.
#       ─ lscpu, nproc, free, dd, ping, date,
#         cat, rm, mktemp, grep, awk, cut,
#         tr, head, tail, sync
#
# NOTE:  We deliberately do *not* look for the output directory
#        /home/user/audit or any artefact files, in accordance with the
#        grading-framework instructions:
#          “DO NOT test for any of the output files or directories.”
#
# Only Python’s standard library and pytest are used.

import os
import shutil
import tempfile
import pytest

HOME_DIR = "/home/user"

REQUIRED_COMMANDS = [
    # System / CPU
    "lscpu",
    "nproc",
    # Memory
    "free",
    # Disk I/O
    "dd",
    "sync",
    "mktemp",
    "rm",
    # Network
    "ping",
    # Timestamps / output
    "date",
    "cat",
    # Text processing utilities frequently used for parsing
    "grep",
    "awk",
    "cut",
    "tr",
    "head",
    "tail",
]


def _command_available(cmd: str) -> bool:
    """
    Return True if *cmd* can be found on the current $PATH.

    Uses shutil.which() for clarity and correctness.
    """
    return shutil.which(cmd) is not None


@pytest.mark.dependency(name="home_exists")
def test_home_directory_exists():
    """
    Ensure the canonical home directory /home/user is present and is
    recognised as a directory by the OS.
    """
    assert os.path.isdir(
        HOME_DIR
    ), f"Expected {HOME_DIR} to exist and be a directory, but it is missing."


@pytest.mark.dependency(depends=["home_exists"], name="home_writable")
def test_home_directory_writable():
    """
    The student’s automation must be able to create sub-directories and
    files.  We attempt to create and immediately delete a temporary file
    in /home/user to verify write permissions.
    """
    try:
        with tempfile.NamedTemporaryFile(dir=HOME_DIR, delete=True) as tmp:
            tmp.write(b"probe")
            tmp.flush()
            assert os.path.isfile(tmp.name), (
                f"Temp file {tmp.name} was not created as expected in {HOME_DIR}."
            )
    except PermissionError as exc:
        pytest.fail(
            f"The directory {HOME_DIR} is not writable for the current user: {exc}"
        )


@pytest.mark.dependency(depends=["home_exists"], name="commands_available")
def test_required_commands_exist():
    """
    Verify that every command the student might reasonably rely on is
    already present in the minimal Linux environment.  This prevents
    situations where the grader penalises the submission for installing
    additional packages.
    """
    missing = [cmd for cmd in REQUIRED_COMMANDS if not _command_available(cmd)]

    assert not missing, (
        "The following required command-line utilities are missing from $PATH:\n"
        + "\n".join(f"  - {cmd}" for cmd in missing)
        + "\nAll of them must be available in a minimal Linux installation."
    )